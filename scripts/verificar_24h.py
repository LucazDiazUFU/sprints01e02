import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from urllib.error import URLError
from urllib.request import urlopen


def verificar(url, duracao, intervalo, caminho):
    if duracao < 0 or intervalo <= 0:
        raise ValueError("Duração e intervalo inválidos.")
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    inicio = time.monotonic()
    anterior = None
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        gravador = csv.writer(arquivo)
        gravador.writerow(
            ["data_utc", "segundos_monitorados", "segundos_ativo", "resultado"]
        )
        while True:
            tempo = time.monotonic() - inicio
            with urlopen(url.rstrip("/") + "/api/saude", timeout=10) as resposta:
                dados = json.load(resposta)
            ativo = float(dados["segundos_ativo"])
            if dados["status"] != "ok" or anterior is not None and ativo < anterior:
                gravador.writerow(
                    [datetime.now(timezone.utc).isoformat(), tempo, ativo, "falha"]
                )
                raise ValueError(
                    "A aplicação falhou ou reiniciou durante a observação."
                )
            gravador.writerow(
                [datetime.now(timezone.utc).isoformat(), tempo, ativo, "ok"]
            )
            arquivo.flush()
            anterior = ativo
            if tempo >= duracao:
                print(f"Observação concluída: {tempo:.1f}s. Registro: {caminho}")
                return
            time.sleep(min(intervalo, duracao - tempo))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    parser.add_argument("--duracao", type=float, default=86400)
    parser.add_argument("--intervalo", type=float, default=60)
    parser.add_argument("--arquivo", default="dados/monitoramento_24h.csv")
    argumentos = parser.parse_args()
    try:
        verificar(
            argumentos.url, argumentos.duracao, argumentos.intervalo, argumentos.arquivo
        )
    except (ValueError, OSError, URLError, KeyError) as erro:
        parser.exit(1, f"Não foi possível comprovar o período: {erro}\n")


if __name__ == "__main__":
    main()
