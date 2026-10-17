import os
from pathlib import Path
import secrets
from threading import RLock
import time

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from .armazenamento import RepositorioJSON
from .cadastro import Inventario
from .modelos import criar_equipamento
from .risco import AnaliseRisco


class ServicoInventario:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.trava = RLock()

    def executar(self, operacao):
        with self.trava:
            inventario = self.repositorio.carregar()
            resultado = operacao(inventario)
            self.repositorio.salvar(inventario)
            return resultado


def criar_app(caminho=None, token=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
    caminho = caminho or os.getenv("INVENTARIO_ARQUIVO", "dados/equipamentos.json")
    token = os.getenv("INVENTARIO_TOKEN", "") if token is None else token
    servico = ServicoInventario(RepositorioJSON(caminho))
    app.extensions["inventario"] = servico
    inicio = time.monotonic()
    web = Path(__file__).resolve().parents[1] / "sprint3" / "web"

    def dados():
        conteudo = request.get_json(silent=True)
        if not isinstance(conteudo, dict):
            raise ValueError("Envie um objeto JSON com os campos da operação.")
        return conteudo

    def ativo_existente(inventario, id_ativo):
        ativo = inventario.buscar_ativo(id=id_ativo)
        if ativo is None:
            raise LookupError("Ativo não encontrado.")
        return ativo

    def vulnerabilidade_existente(inventario, id_vulnerabilidade):
        item = inventario.localizar_vulnerabilidade(id_vulnerabilidade)
        if item is None:
            raise LookupError("Vulnerabilidade não encontrada.")
        return item

    @app.before_request
    def autorizar():
        if request.path.startswith("/api/") and request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
        }:
            recebido = request.headers.get("X-Token", "")
            if token and not secrets.compare_digest(token.encode(), recebido.encode()):
                return jsonify(erro="A operação exige uma credencial válida."), 401
        return None

    @app.after_request
    def cabecalhos(resposta):
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["Referrer-Policy"] = "same-origin"
        resposta.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "img-src 'self' data:; "
            "connect-src 'self' https://servicodados.ibge.gov.br; "
            "frame-ancestors 'none'"
        )
        if request.path.startswith("/api/"):
            resposta.headers["Cache-Control"] = "no-store"
        return resposta

    @app.errorhandler(Exception)
    def tratar_erro(erro):
        if isinstance(erro, LookupError):
            return jsonify(erro=str(erro)), 404
        if isinstance(erro, ValueError):
            codigo = 409 if "Já existe" in str(erro) else 400
            return jsonify(erro=str(erro)), codigo
        if isinstance(erro, HTTPException):
            return jsonify(erro=erro.description), erro.code
        if isinstance(erro, OSError):
            app.logger.exception("Falha no armazenamento")
            return jsonify(erro="Não foi possível acessar a base de dados."), 503
        app.logger.exception("Falha na operação")
        return jsonify(erro="Não foi possível concluir a operação."), 500

    @app.get("/")
    def pagina():
        return send_from_directory(web, "index.html")

    @app.get("/web/<path:nome>")
    def arquivo_web(nome):
        return send_from_directory(web, nome)

    @app.get("/api/saude")
    def saude():
        servico.repositorio.carregar()
        return jsonify(status="ok", segundos_ativo=round(time.monotonic() - inicio, 2))

    @app.get("/api/ativos")
    def listar_ativos():
        inventario = servico.repositorio.carregar()
        itens = inventario.listar_ativos(
            nome=request.args.get("nome", ""),
            tipo=request.args.get("tipo") or None,
            criticidade=request.args.get("criticidade") or None,
            status=request.args.get("status") or None,
        )
        return jsonify([ativo.dados() for ativo in itens])

    @app.post("/api/ativos")
    def cadastrar_ativo():
        conteudo = dados()
        obrigatorios = {"id", "nome", "responsavel", "setor", "tipo"}
        if not obrigatorios <= conteudo.keys():
            raise ValueError("Informe ID, nome, responsável, setor e tipo.")
        resultado = servico.executar(
            lambda inventario: inventario.cadastrar_ativo(**conteudo).dados()
        )
        return jsonify(resultado), 201

    @app.get("/api/ativos/<int:id_ativo>")
    def consultar_ativo(id_ativo):
        return jsonify(
            ativo_existente(servico.repositorio.carregar(), id_ativo).dados()
        )

    @app.route("/api/ativos/<int:id_ativo>", methods=["PUT", "PATCH"])
    def atualizar_ativo(id_ativo):
        conteudo = dados()
        if "id" in conteudo:
            raise ValueError("O ID do ativo não pode ser alterado.")
        if (
            request.method == "PUT"
            and not {"nome", "responsavel", "setor", "tipo"} <= conteudo.keys()
        ):
            raise ValueError("PUT exige nome, responsável, setor e tipo.")
        resultado = servico.executar(
            lambda inventario: inventario.atualizar_ativo(id_ativo, **conteudo).dados()
        )
        return jsonify(resultado)

    @app.delete("/api/ativos/<int:id_ativo>")
    def excluir_ativo(id_ativo):
        if dados().get("confirmar") is not True:
            raise ValueError("Confirme a exclusão com confirmar: true.")
        servico.executar(
            lambda inventario: inventario.excluir_ativo(id_ativo, confirmar=True)
        )
        return "", 204

    @app.route("/api/ativos/<int:id_ativo>/vulnerabilidades", methods=["GET", "POST"])
    def vulnerabilidades_ativo(id_ativo):
        inventario = servico.repositorio.carregar()
        ativo_existente(inventario, id_ativo)
        if request.method == "GET":
            return jsonify(
                [
                    item.dados()
                    for _, item in inventario.listar_vulnerabilidades(ativo_id=id_ativo)
                ]
            )
        conteudo = dados()
        obrigatorios = {"id", "descricao", "categoria", "severidade"}
        if not obrigatorios <= conteudo.keys():
            raise ValueError("Informe ID, descrição, categoria e severidade.")
        permitidos = obrigatorios | {
            "status",
            "cve",
            "cvss",
            "referencia",
            "recomendacao",
        }
        if not conteudo.keys() <= permitidos:
            raise ValueError("Campos desconhecidos no cadastro da vulnerabilidade.")
        resultado = servico.executar(
            lambda inv: inv.cadastrar_vulnerabilidade(id_ativo, **conteudo).dados()
        )
        return jsonify(resultado), 201

    @app.get("/api/vulnerabilidades")
    def listar_vulnerabilidades():
        itens = servico.repositorio.carregar().listar_vulnerabilidades(
            ativo_id=request.args.get("ativo_id") or None,
            cve_codigo=request.args.get("cve", ""),
            severidade=request.args.get("severidade") or None,
            status=request.args.get("status") or None,
        )
        return jsonify(
            [{**item.dados(), "ativo_id": ativo.id} for ativo, item in itens]
        )

    @app.get("/api/vulnerabilidades/<int:id_vulnerabilidade>")
    def consultar_vulnerabilidade(id_vulnerabilidade):
        ativo, item = vulnerabilidade_existente(
            servico.repositorio.carregar(), id_vulnerabilidade
        )
        return jsonify(**item.dados(), ativo_id=ativo.id)

    @app.patch("/api/vulnerabilidades/<int:id_vulnerabilidade>")
    def atualizar_vulnerabilidade(id_vulnerabilidade):
        conteudo = dados()
        if "id" in conteudo:
            raise ValueError("O ID da vulnerabilidade não pode ser alterado.")

        def alterar(inventario):
            vulnerabilidade_existente(inventario, id_vulnerabilidade)
            return inventario.atualizar_vulnerabilidade(
                id_vulnerabilidade, **conteudo
            ).dados()

        return jsonify(servico.executar(alterar))

    @app.delete("/api/vulnerabilidades/<int:id_vulnerabilidade>")
    def excluir_vulnerabilidade(id_vulnerabilidade):
        if dados().get("confirmar") is not True:
            raise ValueError("Confirme a exclusão com confirmar: true.")

        def excluir(inventario):
            vulnerabilidade_existente(inventario, id_vulnerabilidade)
            inventario.excluir_vulnerabilidade(id_vulnerabilidade, confirmar=True)

        servico.executar(excluir)
        return "", 204

    @app.route(
        "/api/ativos/<int:id_ativo>/dependencias/<int:id_dependencia>",
        methods=["PUT", "DELETE"],
    )
    def dependencia(id_ativo, id_dependencia):
        if request.method == "PUT":
            conteudo = dados()
            if conteudo.keys() != {"peso"}:
                raise ValueError("Informe apenas o peso da dependência.")
            resultado = servico.executar(
                lambda inv: inv.definir_dependencia(
                    id_ativo, id_dependencia, conteudo["peso"]
                ).dados()
            )
            return jsonify(resultado)
        servico.executar(lambda inv: inv.remover_dependencia(id_ativo, id_dependencia))
        return "", 204

    @app.get("/api/riscos")
    def riscos():
        inventario = servico.repositorio.carregar()
        return jsonify(
            AnaliseRisco().calcular(inventario, request.args.get("ponderar") == "true")
        )

    @app.get("/api/exportacao")
    def exportacao():
        return jsonify(
            [ativo.dados() for ativo in servico.repositorio.carregar().listar_ativos()]
        )

    @app.post("/api/importacao")
    def importacao():
        conteudo = request.get_json(silent=True)
        if not isinstance(conteudo, list):
            raise ValueError("A importação exige uma lista de objetos JSON.")
        novo = Inventario([criar_equipamento(item) for item in conteudo])

        with servico.trava:
            servico.repositorio.salvar(novo)
        return jsonify(total=len(novo.ativos)), 201

    return app


if __name__ == "__main__":
    criar_app().run(host="127.0.0.1", port=5000, debug=False)
