import os

from .armazenamento import RepositorioJSON
from .banco import RepositorioSQL


def criar_repositorio(caminho=None, terminal=False):
    modo = os.getenv("DB_ENGINE", "json" if terminal else "sqlite").lower()
    if modo == "mariadb":
        from .mariadb import RepositorioMariaDB

        return RepositorioMariaDB()
    if modo == "json" and terminal:
        return RepositorioJSON(caminho or "dados/equipamentos.json")
    if modo == "sqlite" and not terminal:
        return RepositorioSQL(
            caminho or os.getenv("INVENTARIO_BANCO", "dados/inventario.db")
        )
    raise ValueError("Use DB_ENGINE=mariadb, ou a opção local json/SQLite adequada.")
