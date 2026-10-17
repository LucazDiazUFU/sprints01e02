import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from sprint3.cenario import criar_cenario
from trabalho2.api import criar_app
from trabalho2.armazenamento import RepositorioJSON
from trabalho2.banco import RepositorioSQL, VersaoDesatualizada
from trabalho2.cadastro import Inventario
from trabalho2.modelos import Notebook, Roteador, Servidor
from trabalho2.risco import AnaliseRisco


class TesteTrabalho2(unittest.TestCase):
    def setUp(self):
        self.pasta = TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.caminho = Path(self.pasta.name)
        self.inventario = criar_cenario()

    def test_tipos_e_polimorfismo(self):
        ativos = self.inventario.listar_ativos()
        self.assertIsInstance(ativos[0], Notebook)
        self.assertIsInstance(ativos[1], Servidor)
        self.assertIsInstance(ativos[2], Roteador)
        self.assertTrue(ativos[1].exibir_detalhes().startswith("Servidor"))
        self.assertEqual(ativos[1].fator_exposicao(), 1.2)

    def test_recarga_json_lista_preserva_ids_vinculos_e_tipos(self):
        repositorio = RepositorioJSON(self.caminho / "ativos.json")
        repositorio.salvar(self.inventario)
        self.assertIsInstance(json.loads(repositorio.caminho.read_text()), list)
        recarregado = repositorio.carregar()
        self.assertIsInstance(recarregado.ativos[102], Servidor)
        self.assertEqual(recarregado.ativos[101].dependencias, {102: 0.2})
        self.assertEqual(
            [item.id for item in recarregado.ativos[101].vulnerabilidades], [201, 202]
        )

    def test_base_anterior_pode_ser_carregada(self):
        repositorio = RepositorioJSON(self.caminho / "legado.json")
        dados = self.inventario.ativos[101].dados()
        dados.pop("dependencias")
        repositorio.caminho.write_text(json.dumps({"versao": 1, "ativos": [dados]}))
        self.assertIsInstance(repositorio.carregar().ativos[101], Notebook)

    def test_json_invalido_preservado(self):
        repositorio = RepositorioJSON(self.caminho / "invalidos.json")
        repositorio.caminho.write_text("arquivo inválido", encoding="utf-8")
        with self.assertRaises(ValueError):
            repositorio.carregar()
        self.assertEqual(
            repositorio.caminho.read_text(encoding="utf-8"), "arquivo inválido"
        )

    def test_mudanca_tipo_recria_subclasse(self):
        ativo = self.inventario.atualizar_ativo(101, tipo=2)
        self.assertIsInstance(ativo, Servidor)
        self.assertEqual(ativo.dependencias, {102: 0.2})
        self.assertEqual(len(ativo.vulnerabilidades), 2)

    def test_atualizacao_invalida_preserva_registro(self):
        antes = self.inventario.ativos[101].dados()
        with self.assertRaises(ValueError):
            self.inventario.atualizar_ativo(101, nome="")
        self.assertEqual(self.inventario.ativos[101].dados(), antes)

    def test_dependencia_inexistente(self):
        with self.assertRaises(LookupError):
            self.inventario.definir_dependencia(101, 999, 0.1)

    def test_soma_dependencias_impede_matriz_inadequada(self):
        with self.assertRaises(ValueError):
            self.inventario.definir_dependencia(101, 103, 0.8)
        self.assertEqual(self.inventario.ativos[101].dependencias, {102: 0.2})

    def test_exclusao_remove_dependencias_e_vulnerabilidades(self):
        self.inventario.excluir_ativo(102, confirmar=True)
        self.assertEqual(self.inventario.ativos[101].dependencias, {})
        self.assertIsNone(self.inventario.localizar_vulnerabilidade(203))
        self.assertIsNotNone(self.inventario.localizar_vulnerabilidade(201))

    def test_cenario_risco_resolvido_a_mao(self):
        resultado = AnaliseRisco().calcular(self.inventario)
        np.testing.assert_allclose(
            [item["risco_proprio"] for item in resultado["ativos"]], [10, 8, 2]
        )
        np.testing.assert_allclose(
            [item["risco_efetivo"] for item in resultado["ativos"]], [11.7, 8.5, 2]
        )
        self.assertLess(resultado["residuo"], 1e-10)
        self.assertAlmostEqual(resultado["determinante"], 1)

    def test_fatores_exposicao_sao_opcionais(self):
        resultado = AnaliseRisco().calcular(self.inventario, ponderar=True)
        np.testing.assert_allclose(
            [item["risco_efetivo"] for item in resultado["ativos"]], [12.03, 10.15, 2.2]
        )

    def test_sistema_singular_nao_resolvido(self):
        matriz = np.eye(3) - np.array([[0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]])
        with self.assertRaisesRegex(ValueError, "não é invertível"):
            AnaliseRisco.resolver(matriz, [10, 8, 2])

    def test_inventario_vazio_sem_divisao_ou_erro_de_matriz(self):
        self.assertEqual(AnaliseRisco().calcular(Inventario())["ativos"], [])

    def test_sql_recarga_e_json_equivalentes(self):
        banco = RepositorioSQL(self.caminho / "inventario.db")
        banco.salvar(self.inventario)
        recarregado = banco.carregar()
        self.assertEqual(
            [item.dados() for item in recarregado.listar_ativos()],
            [item.dados() for item in self.inventario.listar_ativos()],
        )

    def test_sql_reverte_gravacao_invalida(self):
        banco = RepositorioSQL(self.caminho / "inventario.db")
        banco.salvar(self.inventario)
        alterado = banco.carregar()
        alterado.ativos[102].nome = alterado.ativos[101].nome
        with self.assertRaises(sqlite3.IntegrityError):
            banco.salvar(alterado)
        self.assertEqual(banco.carregar().ativos[102].nome, "servidor-01")

    def test_sql_impede_sobrescrever_edicao_concorrente(self):
        banco = RepositorioSQL(self.caminho / "inventario.db")
        banco.salvar(self.inventario)
        primeira, segunda = banco.carregar(), banco.carregar()
        primeira.atualizar_ativo(101, setor="Suporte")
        banco.salvar(primeira)
        segunda.atualizar_ativo(101, setor="Financeiro")
        with self.assertRaises(VersaoDesatualizada):
            banco.salvar(segunda)
        self.assertEqual(banco.carregar().ativos[101].setor, "Suporte")


class TesteAPI(unittest.TestCase):
    def setUp(self):
        self.pasta = TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.banco = Path(self.pasta.name) / "api.json"
        self.app = criar_app(self.banco, token="")
        self.app.testing = True
        self.cliente = self.app.test_client()
        self.dados = {
            "id": 101,
            "nome": "notebook-01",
            "responsavel": "Lucas",
            "setor": "TI",
            "tipo": 1,
        }

    def cadastrar(self):
        self.assertEqual(
            self.cliente.post("/api/ativos", json=self.dados).status_code, 201
        )

    def test_crud_ativo_e_reinicio(self):
        self.cadastrar()
        self.assertEqual(
            self.cliente.get("/api/ativos/101").json["nome"], "notebook-01"
        )
        self.assertEqual(
            self.cliente.patch(
                "/api/ativos/101", json={"setor": "Suporte"}
            ).status_code,
            200,
        )
        novo = criar_app(self.banco, token="").test_client()
        self.assertEqual(novo.get("/api/ativos/101").json["setor"], "Suporte")
        self.assertEqual(
            novo.delete("/api/ativos/101", json={"confirmar": True}).status_code, 204
        )
        self.assertEqual(novo.get("/api/ativos/101").status_code, 404)

    def test_arquivo_da_api_e_lista_json(self):
        self.cadastrar()
        conteudo = json.loads(self.banco.read_text(encoding="utf-8"))
        self.assertIsInstance(conteudo, list)
        self.assertEqual(conteudo[0]["nome"], "notebook-01")

    def test_cadastro_invalido_e_duplicado(self):
        self.assertEqual(
            self.cliente.post(
                "/api/ativos", json={**self.dados, "nome": ""}
            ).status_code,
            400,
        )
        self.assertEqual(self.cliente.get("/api/ativos").json, [])
        self.cadastrar()
        self.assertEqual(
            self.cliente.post("/api/ativos", json=self.dados).status_code, 409
        )

    def test_id_imutavel_e_put_completo(self):
        self.cadastrar()
        self.assertEqual(
            self.cliente.patch("/api/ativos/101", json={"id": 999}).status_code, 400
        )
        self.assertEqual(
            self.cliente.put("/api/ativos/101", json={"setor": "Suporte"}).status_code,
            400,
        )
        dados = {chave: valor for chave, valor in self.dados.items() if chave != "id"}
        self.assertEqual(
            self.cliente.put(
                "/api/ativos/101", json={**dados, "setor": "Suporte"}
            ).status_code,
            200,
        )

    def test_exclusao_requer_confirmacao(self):
        self.cadastrar()
        self.assertEqual(
            self.cliente.delete(
                "/api/ativos/101", json={"confirmar": False}
            ).status_code,
            400,
        )
        self.assertEqual(self.cliente.get("/api/ativos/101").status_code, 200)

    def test_crud_vulnerabilidade(self):
        self.cadastrar()
        dados = {
            "id": 201,
            "descricao": "Sistema desatualizado",
            "categoria": "Software",
            "severidade": "ALTA",
        }
        self.assertEqual(
            self.cliente.post(
                "/api/ativos/101/vulnerabilidades", json=dados
            ).status_code,
            201,
        )
        self.assertEqual(
            self.cliente.get("/api/ativos/101/vulnerabilidades").json[0]["id"], 201
        )
        self.assertEqual(
            self.cliente.patch(
                "/api/vulnerabilidades/201", json={"status": "CORRIGIDA"}
            ).status_code,
            200,
        )
        self.assertEqual(
            self.cliente.patch(
                "/api/vulnerabilidades/201", json={"id": 202}
            ).status_code,
            400,
        )
        self.assertEqual(
            self.cliente.delete(
                "/api/vulnerabilidades/201", json={"confirmar": True}
            ).status_code,
            204,
        )

    def test_vulnerabilidade_sem_ativo_e_entrada_invalida(self):
        dados = {
            "id": 201,
            "descricao": "Falha",
            "categoria": "Software",
            "severidade": "ALTA",
        }
        self.assertEqual(
            self.cliente.post(
                "/api/ativos/999/vulnerabilidades", json=dados
            ).status_code,
            404,
        )
        self.cadastrar()
        self.assertEqual(
            self.cliente.post(
                "/api/ativos/101/vulnerabilidades", json={**dados, "cvss": 11}
            ).status_code,
            400,
        )
        self.assertEqual(self.cliente.get("/api/vulnerabilidades/999").status_code, 404)

    def test_dependencias_risco_e_exportacao(self):
        itens = [ativo.dados() for ativo in criar_cenario().listar_ativos()]
        self.assertEqual(
            self.cliente.post("/api/importacao", json=itens).status_code, 201
        )
        np.testing.assert_allclose(
            [
                item["risco_efetivo"]
                for item in self.cliente.get("/api/riscos").json["ativos"]
            ],
            [11.7, 8.5, 2],
        )
        self.assertIsInstance(self.cliente.get("/api/exportacao").json, list)
        self.assertEqual(
            self.cliente.put(
                "/api/ativos/101/dependencias/103", json={"peso": 0.8}
            ).status_code,
            400,
        )
        self.assertEqual(
            self.cliente.delete("/api/ativos/101/dependencias/102").status_code, 204
        )

    def test_importacao_invalida_preserva_dados(self):
        self.cadastrar()
        self.assertEqual(
            self.cliente.post("/api/importacao", json=[{"id": 999}]).status_code, 400
        )
        self.assertEqual(self.cliente.get("/api/ativos/101").status_code, 200)

    def test_nome_nao_executa_sql(self):
        self.cadastrar()
        nome = "x'); DROP TABLE equipamentos; --"
        self.assertEqual(
            self.cliente.patch("/api/ativos/101", json={"nome": nome}).status_code, 200
        )
        self.assertEqual(self.cliente.get("/api/ativos/101").json["nome"], nome)

    def test_credencial_exigida_em_escrita(self):
        cliente = criar_app(self.banco, token="credencial-de-teste").test_client()
        self.assertEqual(cliente.get("/api/ativos").status_code, 200)
        self.assertEqual(cliente.post("/api/ativos", json=self.dados).status_code, 401)
        self.assertEqual(
            cliente.post(
                "/api/ativos",
                json=self.dados,
                headers={"X-Token": "credencial-de-teste"},
            ).status_code,
            201,
        )

    def test_saude_erro_http_e_corpo_invalido(self):
        self.assertEqual(self.cliente.get("/api/saude").json["status"], "ok")
        self.assertEqual(self.cliente.get("/api/inexistente").status_code, 404)
        self.assertEqual(self.cliente.post("/api/ativos", json=[]).status_code, 400)
        self.assertEqual(self.cliente.get("/").status_code, 200)


if __name__ == "__main__":
    unittest.main()
