id_ativo = int(input("Digite o ID do ativo: "))
nome = input("Digite o nome do ativo: ").strip()
responsavel = input("Digite o responsável pelo ativo: ").strip()

print(f"ID: {id_ativo} ({type(id_ativo).__name__})")
print(f"Nome: {nome} ({type(nome).__name__})")
print(f"Responsável: {responsavel} ({type(responsavel).__name__})")
