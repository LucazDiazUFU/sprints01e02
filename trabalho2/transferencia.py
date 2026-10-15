import argparse
from pathlib import Path

import pymysql

from .armazenamento import RepositorioJSON
from .repositorios import criar_repositorio


class Transferencia:
    def __init__(self):
        self.repositorio = criar_repositorio()

    def exportar(self, caminho):
        inventario = self.repositorio.carregar()
        RepositorioJSON(caminho).salvar(inventario)
        print(f"Exportados {len(inventario.ativos)} equipamentos para {caminho}.")

    def importar(self, caminho, confirmar):
        if not confirmar:
            raise ValueError(
                "A importação substitui o inventário. Use --confirmar após backup."
            )
        if not Path(caminho).is_file():
            raise ValueError("O arquivo de importação não existe.")
        novo = RepositorioJSON(caminho).carregar()
        atual = self.repositorio.carregar()
        novo.versao = atual.versao
        self.repositorio.salvar(novo)
        print(f"Importados {len(novo.ativos)} equipamentos.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("operacao", choices=["exportar", "importar"])
    parser.add_argument("arquivo")
    parser.add_argument("--confirmar", action="store_true")
    args = parser.parse_args()
    try:
        transferencia = Transferencia()
        if args.operacao == "exportar":
            transferencia.exportar(args.arquivo)
        else:
            transferencia.importar(args.arquivo, args.confirmar)
    except pymysql.MySQLError:
        parser.exit(1, "Não foi possível acessar o MariaDB. Confira a conexão.\n")
    except (ValueError, OSError) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
