from trabalho1.cadastro import Inventario


inventario = Inventario()
ativo = inventario.cadastrar_ativo(101, "notebook-01", "Lucas", "TI", 1)
print("Cadastrado:", ativo.id, ativo.nome)
inventario.cadastrar_vulnerabilidade(101, 201, "Sistema desatualizado", "Software", "ALTA")
print("Busca por ID:", inventario.buscar_ativo(id=101).nome)
print("Busca por nome:", inventario.buscar_ativo(nome="NOTEBOOK-01").id)
inventario.atualizar_ativo(101, setor="Suporte")
print("Setor atualizado:", inventario.buscar_ativo(id=101).setor)
print("Vulnerabilidades:", len(inventario.listar_vulnerabilidades(ativo_id=101)))
inventario.excluir_ativo(101, confirmar=True)
print("Após exclusão:", inventario.buscar_ativo(id=101))
