from trabalho2.cadastro import Inventario


def criar_cenario():
    inventario = Inventario()
    inventario.cadastrar_ativo(101, "notebook-01", "Lucas", "TI", 1)
    inventario.cadastrar_ativo(102, "servidor-01", "Lucas", "TI", 2)
    inventario.cadastrar_ativo(103, "roteador-01", "Lucas", "Rede", 3)
    inventario.cadastrar_vulnerabilidade(
        101, 201, "Configuração insegura", "Configuração", "MEDIA", cvss=4
    )
    inventario.cadastrar_vulnerabilidade(
        101, 202, "Atualização pendente", "Software", "ALTA", cvss=6
    )
    inventario.cadastrar_vulnerabilidade(
        102, 203, "Serviço exposto", "Rede", "ALTA", cvss=8
    )
    inventario.cadastrar_vulnerabilidade(
        103, 204, "Configuração antiga", "Configuração", "BAIXA", cvss=2
    )
    inventario.definir_dependencia(101, 102, 0.2)
    inventario.definir_dependencia(102, 103, 0.25)
    return inventario
