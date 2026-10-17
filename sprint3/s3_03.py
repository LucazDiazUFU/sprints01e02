from collections import deque
from dataclasses import dataclass


class FilaLista:
    def __init__(self):
        self.itens = []

    def enqueue(self, valor):
        self.itens.append(valor)

    def dequeue(self):
        if not self.itens:
            raise IndexError("A fila está vazia.")
        return self.itens.pop(0)


class FilaDeque:
    def __init__(self):
        self.itens = deque()

    def enqueue(self, valor):
        self.itens.append(valor)

    def dequeue(self):
        if not self.itens:
            raise IndexError("A fila está vazia.")
        return self.itens.popleft()


@dataclass
class No:
    valor: object
    proximo: "No | None" = None


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.cauda = None

    def inserir(self, valor):
        novo = No(valor)
        if self.cauda is None:
            self.cabeca = novo
        else:
            self.cauda.proximo = novo
        self.cauda = novo

    def remover(self, valor):
        anterior = None
        atual = self.cabeca
        while atual is not None:
            if atual.valor == valor:
                if anterior is None:
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual is self.cauda:
                    self.cauda = anterior
                return True
            anterior, atual = atual, atual.proximo
        return False

    def __iter__(self):
        atual = self.cabeca
        while atual is not None:
            yield atual.valor
            atual = atual.proximo


if __name__ == "__main__":
    for classe in (FilaLista, FilaDeque):
        fila = classe()
        fila.enqueue(101)
        fila.enqueue(102)
        print(classe.__name__, fila.dequeue(), fila.dequeue())
    ativos = ListaEncadeada()
    for id_ativo in (101, 102, 103):
        ativos.inserir(id_ativo)
    print("Antes:", list(ativos))
    ativos.remover(102)
    print("Depois:", list(ativos))
