import ipaddress
import json
import statistics

from trabalho2.risco import AnaliseRisco
from .cenario import criar_cenario

if __name__ == "__main__":
    rede = ipaddress.ip_network("192.168.1.0/24")
    endereco = ipaddress.ip_address("192.168.1.10")
    riscos = [
        ativo["risco_efetivo"]
        for ativo in AnaliseRisco().calcular(criar_cenario())["ativos"]
    ]
    print(
        json.dumps(
            {
                "rede": str(rede),
                "endereco": str(endereco),
                "pertence_a_rede": endereco in rede,
                "media": statistics.mean(riscos),
                "mediana": statistics.median(riscos),
                "modas": statistics.multimode(riscos),
                "variancia_populacional": statistics.pvariance(riscos),
                "desvio_populacional": statistics.pstdev(riscos),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
