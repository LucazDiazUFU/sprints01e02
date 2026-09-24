import json
import os
import tempfile
from pathlib import Path

from .cadastro import Inventario
from .modelos import Ativo


def carregar(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return Inventario()
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        if not isinstance(dados, dict) or dados.get("versao") != 1 or not isinstance(dados.get("ativos"), list):
            raise ValueError("Formato da base de dados inválido. O arquivo original foi preservado.")
        inventario = Inventario([Ativo.carregar(item) for item in dados["ativos"]])
        return inventario
    except (OSError, json.JSONDecodeError, TypeError, KeyError) as erro:
        raise ValueError("Não foi possível ler a base de dados. O arquivo original foi preservado.") from erro


def salvar(caminho, inventario):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    dados = {"versao": 1, "ativos": [item.dados() for item in inventario.listar_ativos()]}
    temporario = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=caminho.parent, delete=False) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, caminho)
    except OSError as erro:
        if temporario and temporario.exists():
            temporario.unlink()
        raise ValueError("Não foi possível gravar a base de dados.") from erro
