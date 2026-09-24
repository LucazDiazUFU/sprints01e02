grau = int(input("Digite o grau da vulnerabilidade (0 a 10): "))

if grau >= 0 and grau <= 2:
    print("Classificação: BAIXA")
    print("A vulnerabilidade apresenta baixo risco.")

elif grau >= 3 and grau <= 5:
    print("Classificação: MÉDIA")
    print("A vulnerabilidade apresenta risco moderado.")

elif grau >= 6 and grau <= 8:
    print("Classificação: ALTA")
    print("A vulnerabilidade deve ser tratada com prioridade.")

elif grau >= 9 and grau <= 10:
    print("Classificação: CRÍTICA")
    print("A vulnerabilidade requer ação imediata.")

else:
    print("Grau inválido. Digite um número entre 0 e 10.")