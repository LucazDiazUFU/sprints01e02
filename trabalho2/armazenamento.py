import json
import os
from pathlib import Path
import tempfile

from .cadastro import Inventario
from .modelos import criar_equipamento


class RepositorioJSON:
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def carregar(self):
        if not self.caminho.exists():
            return Inventario()
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
            if isinstance(dados, dict) and dados.get("versao") == 1:
                dados = dados.get("ativos")
            if not isinstance(dados, list):
                raise ValueError("A base precisa conter uma lista de objetos JSON.")
            return Inventario([criar_equipamento(item) for item in dados])
        except (OSError, json.JSONDecodeError, TypeError, KeyError) as erro:
            raise ValueError(
                "Não foi possível carregar a base; o arquivo foi preservado."
            ) from erro

    def salvar(self, inventario):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        temporario = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.caminho.parent, delete=False
            ) as arquivo:
                temporario = Path(arquivo.name)
                json.dump(
                    [ativo.dados() for ativo in inventario.listar_ativos()],
                    arquivo,
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                )
                arquivo.write("\n")
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self.caminho)
        except (OSError, ValueError) as erro:
            if temporario and temporario.exists():
                temporario.unlink()
            raise ValueError("Não foi possível salvar a base.") from erro
