from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


def gerar():
    pasta = Path(__file__).with_name("evidencias")
    pasta.mkdir(exist_ok=True)
    for numero in (1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 20):
        nome = f"s3_{numero:02d}"
        resultado = subprocess.run(
            [sys.executable, "-m", f"sprint3.{nome}"],
            capture_output=True,
            text=True,
            check=True,
            timeout=20,
        )
        (pasta / f"{nome}.txt").write_text(resultado.stdout, encoding="utf-8")
    (pasta / "execucao.json").write_text(
        json.dumps(
            {
                "data_utc": datetime.now(timezone.utc).isoformat(),
                "python": sys.version.split()[0],
                "programas": 12,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    gerar()
