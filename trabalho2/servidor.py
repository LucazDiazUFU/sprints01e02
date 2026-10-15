import os
import time

import pymysql

from .repositorios import criar_repositorio


class Servidor:
    def iniciar(self):
        limite = time.monotonic() + 90
        while True:
            try:
                criar_repositorio()
                break
            except pymysql.MySQLError as erro:
                if time.monotonic() >= limite:
                    raise SystemExit(
                        "Banco indisponível. Confira rede, credenciais "
                        "e schema_mariadb.sql."
                    ) from erro
                print("Aguardando o banco de dados...", flush=True)
                time.sleep(3)
        os.execvp(
            "gunicorn",
            [
                "gunicorn",
                "--bind", "0.0.0.0:5000",
                "--workers", "1",
                "--threads", "4",
                "--timeout", "60",
                "--graceful-timeout", "20",
                "--access-logfile", "-",
                "--error-logfile", "-",
                "trabalho2.api:criar_app()",
            ],
        )


if __name__ == "__main__":
    Servidor().iniciar()
