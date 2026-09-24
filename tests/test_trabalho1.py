import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from trabalho1.app import main
from trabalho1.armazenamento import carregar, salvar
from trabalho1.cadastro import Inventario
from trabalho1.validacoes import TIPOS


class TesteInventario(unittest.TestCase):
    def setUp(self):
        self.inventario = Inventario()

    def ativo(self, id=101, nome="notebook-01"):
        return self.inventario.cadastrar_ativo(id, nome, "Lucas", "TI", 1)

    def vulnerabilidade(self, ativo_id=101, id=201):
        return self.inventario.cadastrar_vulnerabilidade(
            ativo_id, id, "Sistema desatualizado", "Atualização", "ALTA"
        )

    def test_enum_tem_quatro_tipos_ou_mais(self):
        self.assertGreaterEqual(len(TIPOS), 4)
        self.assertTrue(all(isinstance(codigo, int) for codigo in TIPOS))

    def test_cadastrar_buscar_por_id_e_nome(self):
        ativo = self.ativo()
        self.assertIs(self.inventario.buscar_ativo(id=101), ativo)
        self.assertIs(self.inventario.buscar_ativo(nome="NOTEBOOK-01"), ativo)

    def test_cadastro_com_id_repetido(self):
        self.ativo()
        with self.assertRaisesRegex(ValueError, "ID"):
            self.ativo(nome="outro")

    def test_cadastro_com_nome_repetido(self):
        self.ativo()
        with self.assertRaisesRegex(ValueError, "nome"):
            self.ativo(id=102, nome="NOTEBOOK-01")

    def test_cadastro_invalido_nao_altera_base(self):
        with self.assertRaises(ValueError):
            self.inventario.cadastrar_ativo("abc", "", "Lucas", "TI", 99)
        self.assertEqual(self.inventario.ativos, {})

    def test_cadastro_com_campo_vazio(self):
        with self.assertRaisesRegex(ValueError, "Responsável"):
            self.inventario.cadastrar_ativo(101, "notebook-01", "", "TI", 1)
        self.assertEqual(self.inventario.ativos, {})

    def test_busca_e_filtros_combinados(self):
        self.ativo()
        self.inventario.cadastrar_ativo(102, "servidor-01", "Ana", "TI", 2, "ALTA")
        self.assertEqual([item.id for item in self.inventario.listar_ativos(tipo=2, criticidade="alta")], [102])
        self.assertEqual(self.inventario.listar_ativos(nome="impressora"), [])
        self.assertIsNone(self.inventario.buscar_ativo(id=999))

    def test_atualizacao_parcial_e_historico(self):
        self.ativo()
        novo = self.inventario.atualizar_ativo(101, responsavel="Ana")
        self.assertEqual((novo.nome, novo.responsavel, novo.id), ("notebook-01", "Ana", 101))
        self.assertEqual(self.inventario.historico[-1]["antes"], {"responsavel": "Lucas"})
        self.assertEqual(self.inventario.historico[-1]["depois"], {"responsavel": "Ana"})

    def test_atualizacao_invalida_preserva_ativo(self):
        self.ativo()
        with self.assertRaises(ValueError):
            self.inventario.atualizar_ativo(101, nome="")
        self.assertEqual(self.inventario.buscar_ativo(id=101).nome, "notebook-01")

    def test_atualizacao_de_inexistente(self):
        with self.assertRaisesRegex(ValueError, "não encontrado"):
            self.inventario.atualizar_ativo(999, setor="TI")

    def test_exclusao_exige_confirmacao_e_remove_vulnerabilidades(self):
        self.ativo()
        self.vulnerabilidade()
        self.assertFalse(self.inventario.excluir_ativo(101))
        self.assertEqual(len(self.inventario.listar_vulnerabilidades(ativo_id=101)), 1)
        self.assertTrue(self.inventario.excluir_ativo(101, confirmar=True))
        self.assertIsNone(self.inventario.buscar_ativo(id=101))
        self.assertEqual(self.inventario.listar_vulnerabilidades(), [])

    def test_exclusao_de_inexistente(self):
        with self.assertRaisesRegex(ValueError, "não encontrado"):
            self.inventario.excluir_ativo(999, confirmar=True)

    def test_vulnerabilidade_inicial(self):
        from trabalho1.modelos import Vulnerabilidade
        inicial = Vulnerabilidade(201, "Senha fraca", "Autenticação", "MEDIA", "ABERTA")
        ativo = self.inventario.cadastrar_ativo(101, "notebook", "Lucas", "TI", 1, vulnerabilidades=[inicial])
        self.assertEqual(ativo.vulnerabilidades[0].id, 201)

    def test_cadastrar_e_consultar_vulnerabilidade(self):
        self.ativo()
        self.vulnerabilidade()
        self.assertEqual(self.inventario.listar_vulnerabilidades(ativo_id=101)[0][1].descricao, "Sistema desatualizado")
        self.assertEqual(self.inventario.listar_vulnerabilidades(ativo_id=101, severidade="BAIXA"), [])

    def test_vulnerabilidade_sem_ativo(self):
        with self.assertRaisesRegex(ValueError, "Ativo não encontrado"):
            self.vulnerabilidade()

    def test_vulnerabilidade_duplicada(self):
        self.ativo()
        self.vulnerabilidade()
        with self.assertRaisesRegex(ValueError, "ID"):
            self.vulnerabilidade()

    def test_cve_cvss_e_filtros(self):
        self.ativo()
        self.inventario.cadastrar_vulnerabilidade(101, 201, "Falha", "Software", "CRITICA", cve="CVE-2021-44228", cvss=10)
        self.assertEqual(len(self.inventario.listar_vulnerabilidades(cve_codigo="cve-2021-44228", severidade="CRITICA")), 1)
        self.assertEqual(self.inventario.listar_vulnerabilidades(status="CORRIGIDA"), [])

    def test_cve_invalida(self):
        self.ativo()
        with self.assertRaisesRegex(ValueError, "CVE"):
            self.inventario.cadastrar_vulnerabilidade(101, 201, "Falha", "Software", "ALTA", cve="incorreta")

    def test_cvss_fora_da_faixa_e_nan(self):
        self.ativo()
        for valor in (-1, 11, "nan"):
            with self.subTest(valor=valor), self.assertRaisesRegex(ValueError, "CVSS"):
                self.inventario.cadastrar_vulnerabilidade(101, 201, "Falha", "Software", "ALTA", cvss=valor)

    def test_atualizar_vulnerabilidade(self):
        self.ativo()
        self.vulnerabilidade()
        self.inventario.atualizar_vulnerabilidade(201, status="CORRIGIDA")
        self.assertEqual(self.inventario.listar_vulnerabilidades(status="CORRIGIDA")[0][1].id, 201)

    def test_excluir_vulnerabilidade(self):
        self.ativo()
        self.vulnerabilidade()
        self.assertFalse(self.inventario.excluir_vulnerabilidade(201))
        self.assertTrue(self.inventario.excluir_vulnerabilidade(201, confirmar=True))
        self.assertEqual(self.inventario.listar_vulnerabilidades(ativo_id=101), [])

    def test_persistencia_apos_reiniciar(self):
        self.ativo()
        self.vulnerabilidade()
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "ativos.json"
            salvar(caminho, self.inventario)
            novo = carregar(caminho)
            self.assertEqual(novo.buscar_ativo(id=101).nome, "notebook-01")
            self.assertEqual(novo.listar_vulnerabilidades(ativo_id=101)[0][1].id, 201)

    def test_arquivo_corrompido_preservado(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "ativos.json"
            caminho.write_text("{ inválido", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "preservado"):
                carregar(caminho)
            self.assertEqual(caminho.read_text(encoding="utf-8"), "{ inválido")

    def test_arquivo_com_raiz_invalida_preservado(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "ativos.json"
            caminho.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "preservado"):
                carregar(caminho)
            self.assertEqual(caminho.read_text(encoding="utf-8"), "[]")

    def test_arquivo_com_id_duplicado(self):
        self.ativo()
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "ativos.json"
            dados = self.inventario.buscar_ativo(id=101).dados()
            caminho.write_text(json.dumps({"versao": 1, "ativos": [dados, dados]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ID"):
                carregar(caminho)

    def test_menu_com_entrada_invalida_e_saida(self):
        with tempfile.TemporaryDirectory() as pasta, patch("builtins.input", side_effect=["x", "0"]), patch("builtins.print") as imprimir:
            main(Path(pasta) / "ativos.json")
            self.assertTrue(any(chamada.args == ("Opção inválida.",) for chamada in imprimir.call_args_list))


if __name__ == "__main__":
    unittest.main()
