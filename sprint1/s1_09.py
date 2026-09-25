def exibir_ativo(nome, responsavel):
    print(f"Ativo: {nome}")
    print(f"Responsável: {responsavel}")


def classificar_vulnerabilidade(grau):
    if 0 <= grau <= 2:
        return "BAIXA"
    if grau <= 5 and grau >= 3:
        return "MÉDIA"
    if grau <= 8 and grau >= 6:
        return "ALTA"
    if grau <= 10 and grau >= 9:
        return "CRÍTICA"
    return "INVÁLIDA"


def exibir_vulnerabilidade(nome, grau):
    print(f"Vulnerabilidade: {nome}")
    print(f"Classificação: {classificar_vulnerabilidade(grau)}")


nome_ativo = input("Digite o nome do ativo: ").strip()
responsavel = input("Digite o responsável pelo ativo: ").strip()
nome_vulnerabilidade = input("Digite a vulnerabilidade: ").strip()
grau = int(input("Digite o grau da vulnerabilidade (0 a 10): "))

exibir_ativo(nome_ativo, responsavel)
exibir_vulnerabilidade(nome_vulnerabilidade, grau)
