def antes(ativos, tipo):
    resultado = []
    for ativo in ativos:
        if ativo["tipo"] == tipo:
            if ativo["status"] == "ATIVO":
                resultado.append(ativo["nome"])
    return resultado


def depois(ativos, tipo):
    return [
        ativo["nome"]
        for ativo in ativos
        if ativo["tipo"] == tipo and ativo["status"] == "ATIVO"
    ]
