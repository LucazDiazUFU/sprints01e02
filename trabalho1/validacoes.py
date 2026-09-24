import re
import math
from enum import IntEnum


class TipoAtivo(IntEnum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    APLICACAO_WEB = 4
    BANCO_DE_DADOS = 5
    ESTACAO_DE_TRABALHO = 6


TIPOS = {
    TipoAtivo.NOTEBOOK: "Notebook",
    TipoAtivo.SERVIDOR: "Servidor",
    TipoAtivo.ROTEADOR: "Roteador",
    TipoAtivo.APLICACAO_WEB: "Aplicação web",
    TipoAtivo.BANCO_DE_DADOS: "Banco de dados",
    TipoAtivo.ESTACAO_DE_TRABALHO: "Estação de trabalho",
}
CRITICIDADES = ("BAIXA", "MEDIA", "ALTA", "CRITICA")
STATUS_ATIVO = ("ATIVO", "INATIVO", "MANUTENCAO")
SEVERIDADES = ("BAIXA", "MEDIA", "ALTA", "CRITICA")
STATUS_VULNERABILIDADE = ("ABERTA", "EM_TRATAMENTO", "CORRIGIDA", "RISCO_ACEITO")


def texto(valor, campo, limite=120):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} não pode ficar vazio.")
    valor = valor.strip()
    if len(valor) > limite:
        raise ValueError(f"{campo} deve ter no máximo {limite} caracteres.")
    return valor


def numero(valor, campo):
    if isinstance(valor, bool):
        raise ValueError(f"{campo} deve ser um número inteiro positivo.")
    try:
        numero_convertido = int(valor)
    except (ValueError, TypeError):
        raise ValueError(f"{campo} deve ser um número inteiro positivo.") from None
    if numero_convertido <= 0 or str(numero_convertido) != str(valor).strip():
        raise ValueError(f"{campo} deve ser um número inteiro positivo.")
    return numero_convertido


def opcao(valor, permitidos, campo):
    valor = texto(valor, campo).upper().replace(" ", "_")
    if valor not in permitidos:
        raise ValueError(f"{campo} inválido. Use: {', '.join(permitidos)}.")
    return valor


def tipo_ativo(valor):
    codigo = numero(valor, "Tipo")
    if codigo not in TIPOS:
        raise ValueError("Tipo inválido. Escolha um código da lista.")
    return codigo


def cve(valor):
    if not valor:
        return ""
    valor = texto(valor, "CVE", 25).upper()
    if not re.fullmatch(r"CVE-\d{4}-\d{4,}", valor):
        raise ValueError("CVE inválida. Use o formato CVE-AAAA-NNNN.")
    return valor


def cvss(valor):
    if valor is None or valor == "":
        return None
    try:
        nota = float(valor)
    except (ValueError, TypeError):
        raise ValueError("CVSS deve ser um número entre 0 e 10.") from None
    if not math.isfinite(nota) or not 0 <= nota <= 10:
        raise ValueError("CVSS deve ser um número entre 0 e 10.")
    return nota
