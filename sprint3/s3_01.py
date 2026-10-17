from pathlib import Path
from tempfile import TemporaryDirectory

from trabalho2.armazenamento import RepositorioJSON
from trabalho2.modelos import Notebook, Roteador, Servidor

from .cenario import criar_cenario


def demonstrar():
    inventario = criar_cenario()
    for ativo in inventario.listar_ativos():
        print(ativo.exibir_detalhes())
        print("Notebook:", isinstance(ativo, Notebook))
        print("Servidor:", isinstance(ativo, Servidor))
        print("Roteador:", isinstance(ativo, Roteador))
    with TemporaryDirectory() as pasta:
        repositorio = RepositorioJSON(Path(pasta) / "equipamentos.json")
        repositorio.salvar(inventario)
        recarregado = repositorio.carregar()
        print(
            "Tipos recarregados:",
            [type(item).__name__ for item in recarregado.listar_ativos()],
        )
        print("IDs recarregados:", list(recarregado.ativos))
        print("Dependências:", recarregado.ativos[101].dependencias)
        print(
            "Vulnerabilidades:",
            [item.id for item in recarregado.ativos[101].vulnerabilidades],
        )


if __name__ == "__main__":
    demonstrar()
