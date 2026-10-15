from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class ConfiguracaoBanco:
    host: str
    porta: int
    usuario: str
    senha: str = field(repr=False)
    banco: str
    ca: str = ""

    @classmethod
    def ambiente(cls):
        nomes = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        faltantes = [nome for nome in nomes if not os.getenv(nome)]
        if faltantes:
            raise ValueError("Configure as variáveis: " + ", ".join(faltantes))
        porta = int(os.getenv("DB_PORT", "3306"))
        if not 1 <= porta <= 65535:
            raise ValueError("DB_PORT deve estar entre 1 e 65535.")
        return cls(
            os.environ["DB_HOST"],
            porta,
            os.environ["DB_USER"],
            os.environ["DB_PASSWORD"],
            os.environ["DB_NAME"],
            os.getenv("DB_SSL_CA", ""),
        )

    def parametros(self):
        parametros = {
            "host": self.host,
            "port": self.porta,
            "user": self.usuario,
            "password": self.senha,
            "database": self.banco,
            "charset": "utf8mb4",
            "autocommit": False,
            "connect_timeout": 5,
            "read_timeout": 15,
            "write_timeout": 15,
        }
        if self.ca:
            parametros.update(
                ssl_ca=self.ca, ssl_verify_cert=True, ssl_verify_identity=True
            )
        return parametros
