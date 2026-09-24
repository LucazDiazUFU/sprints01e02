# Trabalho 1 — inventário de segurança

Programa em Python para cadastrar ativos de TI e acompanhar as vulnerabilidades associadas. O menu funciona no terminal. Os dados ficam em `trabalho1/ativos.json`, criado na primeira alteração, e continuam disponíveis após fechar o programa.

## Executar

Requer Python 3.10 ou superior. Na pasta do repositório:

```bash
python3 main.py
```

No Windows, use `py main.py`. Não há dependências externas. Para testar:

```bash
python3 -m unittest discover -s tests -v
```

O arquivo `trabalho1/ativos.json` contém os dados locais do usuário e não deve ser enviado ao GitHub. Se ele estiver ilegível, o programa avisa e preserva o arquivo. Faça uma cópia antes de editá-lo manualmente.

## Menu e dados

O menu permite cadastrar, buscar, listar, atualizar e excluir ativos; também permite cadastrar, consultar, atualizar e excluir vulnerabilidades. O ativo recebe ID inteiro positivo, nome/hostname, responsável, setor/localização e tipo. Tipo usa códigos inteiros de 1 a 6 da enumeração `TipoAtivo`. Criticidade e status são opcionais com valores iniciais.

Cada vulnerabilidade recebe ID inteiro positivo, descrição, categoria, severidade e status. CVE, CVSS, referência e recomendação são opcionais. Para cadastrar uma vulnerabilidade inicial, responda `s` após cadastrar o ativo. Também é possível adicionar vulnerabilidades depois pelo menu 6.

O ID do ativo não muda. A busca por ID é direta no dicionário; a busca por nome ignora letras maiúsculas/minúsculas. Listagens aceitam filtros. A exclusão pede a palavra `EXCLUIR`. Ao excluir um ativo, as vulnerabilidades dentro dele também são removidas. Essa exclusão é física no arquivo; antes de confirmar, confira o ID. O programa não exige dados pessoais além do nome do responsável.

## Fluxo para apresentar em cinco minutos

1. Execute `python3 main.py` e cadastre um notebook com ID 101, nome `notebook-01`, responsável e setor.
2. Cadastre a vulnerabilidade 201 pelo menu 6 e consulte-a no menu 7. Mostre uma tentativa com severidade inválida.
3. Busque o ativo pelo ID e depois pelo nome, atualize o setor e liste os ativos.
4. Saia e abra o programa novamente para mostrar que os dados foram gravados no arquivo.
5. Cancele uma exclusão, depois confirme `EXCLUIR` e mostre que o ativo e sua vulnerabilidade desapareceram.

Use dados de exemplo na apresentação. Treine a explicação das classes, do dicionário por ID, da enumeração e da gravação em JSON antes da avaliação individual.

## Organização

- `main.py`: entrada do programa.
- `trabalho1/app.py`: menu e apresentação dos dados.
- `trabalho1/modelos.py`: classes `Ativo` e `Vulnerabilidade`.
- `trabalho1/validacoes.py`: enumeração e regras de entrada.
- `trabalho1/cadastro.py`: cadastro, consulta, atualização, exclusão e histórico em memória.
- `trabalho1/armazenamento.py`: leitura e gravação do arquivo JSON.
- `tests/`: testes do CRUD e da persistência.
- `docs/`: requisitos, critérios e especificação da S2.
- `sprint2/`: registros e demonstrações das atividades da S2.

## Decisões da S2

As regras de entrada foram concentradas em `validacoes.py` para evitar validações diferentes entre cadastro e atualização. `cadastro.py` cuida dos dados e `app.py` cuida das perguntas ao usuário. A classe `Inventario` guarda os ativos em `dict` indexado pelo ID, enquanto cada ativo guarda sua lista de vulnerabilidades. A função de gravação usa um arquivo temporário e substitui o JSON anterior após concluir a escrita. Não há senhas, chaves ou dados reais no repositório.

Os exercícios da S1 estão em `sprint1/`. A [especificação](docs/especificacao.md) relaciona os dez requisitos do enunciado ao código e aos testes. Os exemplos de CVE em `sprint2/` são cenários de estudo; não afirmam que há sistemas vulneráveis em uma organização real.
