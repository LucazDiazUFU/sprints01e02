# S2_03 e S2_15 — fluxo em memória

O protótipo é a classe `Inventario`, executada em `sprint2/demo.py`. Execute `python3 -m sprint2.demo` na raiz. O dicionário `ativos` usa o ID inteiro como chave:

1. `cadastrar_ativo(101, ...)` valida e insere `ativos[101]`.
2. `buscar_ativo(id=101)` usa `dict.get`; a busca por nome percorre os valores.
3. `atualizar_ativo(101, setor="Suporte")` valida um novo objeto e substitui apenas o registro válido.
4. `excluir_ativo(101, confirmar=True)` remove a chave e as vulnerabilidades aninhadas.

O mesmo ciclo vale para vulnerabilidades, vinculadas ao ID do ativo. As operações de memória são cobertas por `tests/test_trabalho1.py`. O menu chama `salvar()` após alterações para persistir os dados; o protótipo não precisa de arquivo.
