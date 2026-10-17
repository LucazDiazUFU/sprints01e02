from pathlib import Path

from trabalho1 import app as menu_anterior

from .armazenamento import RepositorioJSON
from .risco import AnaliseRisco


class Aplicacao:
    def __init__(self, caminho="dados/equipamentos.json"):
        self.repositorio = RepositorioJSON(Path(caminho))
        self.inventario = self.repositorio.carregar()

    def cadastrar_ativo(self):
        menu_anterior.cadastrar_ativo(self.inventario)

    def buscar_ativo(self):
        menu_anterior.buscar_ativo(self.inventario)

    def listar_ativos(self):
        menu_anterior.listar_ativos(self.inventario)

    def atualizar_ativo(self):
        menu_anterior.atualizar_ativo(self.inventario)

    def excluir_ativo(self):
        return menu_anterior.excluir_ativo(self.inventario)

    def cadastrar_vulnerabilidade(self):
        menu_anterior.cadastrar_vulnerabilidade(self.inventario)

    def consultar_vulnerabilidades(self):
        menu_anterior.consultar_vulnerabilidades(self.inventario)

    def atualizar_vulnerabilidade(self):
        id = input("ID da vulnerabilidade: ").strip()
        encontrado = self.inventario.localizar_vulnerabilidade(id)
        if encontrado is None:
            raise LookupError("Vulnerabilidade não encontrada.")
        vuln = encontrado[1]
        pedir = menu_anterior.pedir
        self.inventario.atualizar_vulnerabilidade(
            id,
            descricao=pedir("Descrição", vuln.descricao),
            categoria=pedir("Categoria", vuln.categoria),
            severidade=pedir("Severidade", vuln.severidade),
            status=pedir("Status", vuln.status),
            cve=pedir("CVE", vuln.cve),
            cvss=pedir("CVSS", vuln.cvss if vuln.cvss is not None else ""),
            referencia=pedir("Referência", vuln.referencia),
            recomendacao=pedir("Recomendação", vuln.recomendacao),
        )
        print("Vulnerabilidade atualizada.")

    def excluir_vulnerabilidade(self):
        return menu_anterior.excluir_vulnerabilidade(self.inventario)

    def definir_dependencia(self):
        id = input("ID do ativo que recebe o risco: ").strip()
        id_ativo = input("ID do ativo do qual ele depende: ").strip()
        peso = input("Fração do risco transmitida (0 a menos de 1): ").strip()
        self.inventario.definir_dependencia(id, id_ativo, peso)
        print("Dependência cadastrada.")

    def remover_dependencia(self):
        self.inventario.remover_dependencia(
            input("ID do ativo: ").strip(), input("ID da dependência: ").strip()
        )
        print("Dependência removida.")

    def riscos(self):
        resultado = AnaliseRisco().calcular(self.inventario)
        for ativo in resultado["ativos"]:
            print(
                f"{ativo['id']} | {ativo['nome']}"
                f" | próprio: {ativo['risco_proprio']:.4f}"
                f" | efetivo: {ativo['risco_efetivo']:.4f}"
            )
        print(f"Determinante: {resultado['determinante']:.6f}")
        print(f"Número de condição: {resultado['condicao']:.6f}")
        if resultado["aviso"]:
            print(resultado["aviso"])

    def executar(self):
        operacoes = {
            "1": self.cadastrar_ativo,
            "2": self.buscar_ativo,
            "3": self.listar_ativos,
            "4": self.atualizar_ativo,
            "5": self.excluir_ativo,
            "6": self.cadastrar_vulnerabilidade,
            "7": self.consultar_vulnerabilidades,
            "8": self.atualizar_vulnerabilidade,
            "9": self.excluir_vulnerabilidade,
            "10": self.definir_dependencia,
            "11": self.remover_dependencia,
            "12": self.riscos,
        }
        alteracoes = {"1", "4", "5", "6", "8", "9", "10", "11"}
        while True:
            print("\nINVENTÁRIO - TRABALHO 02")
            print("1 Cadastrar | 2 Buscar | 3 Listar | 4 Atualizar | 5 Excluir ativo")
            print("6 Cadastrar | 7 Consultar | 8 Atualizar | 9 Excluir vulnerabilidade")
            print(
                "10 Cadastrar dependência | 11 Remover dependência | 12 Riscos | 0 Sair"
            )
            try:
                escolha = input("Opção: ").strip()
                if escolha == "0":
                    break
                if escolha not in operacoes:
                    print("Opção inválida.")
                    continue
                self.inventario = self.repositorio.carregar()
                resultado = operacoes[escolha]()
                if escolha in alteracoes and resultado is not False:
                    self.repositorio.salvar(self.inventario)
            except (ValueError, LookupError) as erro:
                print(f"Erro: {erro}")
                self.inventario = self.repositorio.carregar()
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrado.")
                break
