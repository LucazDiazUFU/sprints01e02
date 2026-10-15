import math

import numpy as np
import pytest

from sprint3.s3_02 import (
    fatorial_iterativo,
    fatorial_recursivo,
    fibonacci,
    fibonacci_memorizado,
)
from sprint3.s3_03 import FilaDeque, FilaLista, ListaEncadeada
from sprint3.s3_05 import bubble_sort, busca_binaria, insertion_sort, selection_sort
from sprint3.s3_10 import escalonar
from sprint3.s3_11 import determinante_cofatores, determinante_sarrus
from sprint3.s3_13 import tabelas
from sprint3.s3_14 import meio_somador, multiplexador
from trabalho2.cadastro import Inventario
from trabalho2.modelos import criar_equipamento


@pytest.mark.parametrize("numero", [0, 1, 5, 15])
def test_fatoriais(numero):
    assert fatorial_iterativo(numero) == math.factorial(numero)
    assert fatorial_recursivo(numero) == math.factorial(numero)


@pytest.mark.parametrize("numero", [0, 1, 2, 10, 20])
def test_fibonacci(numero):
    assert fibonacci(numero) == fibonacci_memorizado(numero)


@pytest.mark.parametrize(
    "funcao", [fatorial_iterativo, fatorial_recursivo, fibonacci, fibonacci_memorizado]
)
def test_numeros_invalidos(funcao):
    with pytest.raises(ValueError):
        funcao(-1)


@pytest.mark.parametrize("classe", [FilaLista, FilaDeque])
def test_fila_fifo_e_vazia(classe):
    fila = classe()
    with pytest.raises(IndexError):
        fila.dequeue()
    fila.enqueue(101)
    fila.enqueue(102)
    assert fila.dequeue() == 101
    assert fila.dequeue() == 102


def test_lista_encadeada_cabeca_cauda_e_reinsercao():
    lista = ListaEncadeada()
    for item in [101, 102, 103]:
        lista.inserir(item)
    assert lista.remover(101)
    assert lista.remover(103)
    assert list(lista) == [102]
    assert lista.remover(102)
    assert not lista.remover(999)
    lista.inserir(104)
    assert list(lista) == [104]


@pytest.mark.parametrize("ordenar", [bubble_sort, selection_sort, insertion_sort])
@pytest.mark.parametrize(
    "dados", [[], [1], [3, 1, 2, 1], list(range(20)), list(range(20, 0, -1))]
)
def test_ordenacao_resultado_e_entrada_preservada(ordenar, dados):
    antes = dados.copy()
    ordenados, _ = ordenar(dados)
    assert ordenados == sorted(dados)
    assert dados == antes


def test_busca_binaria_bordas_e_ausencia():
    for valor in [1, 2, 3, 4, 5]:
        assert busca_binaria([1, 2, 3, 4, 5], valor)[0] == valor - 1
    assert busca_binaria([], 1)[0] is None
    assert busca_binaria([1, 2, 3], 999)[0] is None


def test_escalonamento_tres_classificacoes():
    np.testing.assert_allclose(escalonar([[1, 1], [2, 1]], [3, 4])["solucao"], [1, 2])
    assert escalonar([[1, 1], [2, 2]], [3, 6])["classificacao"] == "SPI"
    assert escalonar([[1, 1], [2, 2]], [3, 7])["classificacao"] == "SI"


def test_determinantes_e_limite_sarrus():
    matriz = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    assert determinante_sarrus(matriz) == pytest.approx(np.linalg.det(matriz))
    assert determinante_cofatores(matriz) == pytest.approx(np.linalg.det(matriz))
    with pytest.raises(ValueError):
        determinante_sarrus([[1, 0], [0, 1]])


def test_logica_equivalencia_e_argumento():
    linhas = tabelas()
    assert all(
        item["de_morgan_esquerda"] == item["de_morgan_direita"] for item in linhas
    )
    assert all(item["modus_ponens"] for item in linhas)
    assert any(not item["afirmar_consequente"] for item in linhas)


def test_circuitos_somador_e_mux():
    assert meio_somador(True, True) == {"soma": False, "vai_um": True}
    assert multiplexador(True, False, False)
    assert not multiplexador(True, False, True)


@pytest.mark.parametrize("peso", [-0.1, 1, 2, float("nan"), float("inf"), True])
def test_pesos_invalidos(peso):
    with pytest.raises(ValueError):
        criar_equipamento(
            {
                "id": 101,
                "nome": "notebook-01",
                "responsavel": "Lucas",
                "setor": "TI",
                "tipo": 1,
                "dependencias": {102: peso},
            }
        )


def test_dependencia_ciclica_estavel_e_remocao():
    inventario = Inventario()
    inventario.cadastrar_ativo(101, "notebook-01", "Lucas", "TI", 1)
    inventario.cadastrar_ativo(102, "servidor-01", "Lucas", "TI", 2)
    inventario.definir_dependencia(101, 102, 0.4)
    inventario.definir_dependencia(102, 101, 0.5)
    inventario.remover_dependencia(101, 102)
    assert inventario.ativos[101].dependencias == {}


def test_refatoracao_preserva_filtro():
    from sprint3.refatoracao import antes, depois

    ativos = [
        {"nome": "a", "tipo": 1, "status": "ATIVO"},
        {"nome": "b", "tipo": 1, "status": "INATIVO"},
        {"nome": "c", "tipo": 2, "status": "ATIVO"},
    ]
    assert antes(ativos, 1) == depois(ativos, 1) == ["a"]


def test_terminal_edicao_preserva_cvss_zero(tmp_path, monkeypatch):
    from trabalho2.app import Aplicacao

    app = Aplicacao(tmp_path / "ativos.json")
    app.inventario.cadastrar_ativo(101, "notebook", "Exemplo", "TI", 1)
    app.inventario.cadastrar_vulnerabilidade(
        101, 201, "Teste", "Configuração", "BAIXA", cvss=0
    )
    respostas = iter(["201"] + [""] * 8)
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))
    app.atualizar_vulnerabilidade()
    assert app.inventario.localizar_vulnerabilidade(201)[1].cvss == 0
