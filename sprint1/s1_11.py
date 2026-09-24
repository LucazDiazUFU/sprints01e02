categorias = ("Servidor", "Notebook", "Switch", "Firewall")
print("Categorias:", ", ".join(categorias))
print("Primeira categoria:", categorias[0])

vulnerabilidades_ativo_1 = {"Senha fraca", "Software desatualizado", "Porta aberta"}
vulnerabilidades_ativo_2 = {"Software desatualizado", "Acesso indevido", "Porta aberta"}

print("Vulnerabilidades do ativo 1:", ", ".join(sorted(vulnerabilidades_ativo_1)))
print("Vulnerabilidades do ativo 2:", ", ".join(sorted(vulnerabilidades_ativo_2)))
print("União:", ", ".join(sorted(vulnerabilidades_ativo_1 | vulnerabilidades_ativo_2)))
print("Interseção:", ", ".join(sorted(vulnerabilidades_ativo_1 & vulnerabilidades_ativo_2)))
print("Apenas no ativo 1:", ", ".join(sorted(vulnerabilidades_ativo_1 - vulnerabilidades_ativo_2)))
