FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 INVENTARIO_ARQUIVO=/app/dados/equipamentos.json
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -u 10001 -m inventario
COPY trabalho1 ./trabalho1
COPY trabalho2 ./trabalho2
COPY sprint3/web ./sprint3/web
RUN mkdir -p /app/dados && chown -R inventario:inventario /app
USER inventario
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/saude', timeout=3)"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-", "trabalho2.api:criar_app()"]
