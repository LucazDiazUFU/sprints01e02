# Requisitos do CRUD — versão 1.0

Base: PDF “Avaliacao_Sprints_1_e_2_versao_2_0_2026_2.pdf” anexado ao Product Backlog do Trello. A tabela 1 do enunciado possui dez requisitos. A avaliação é individual.

## Histórias de usuário

1. Como responsável pelo inventário, quero cadastrar um ativo para saber quais recursos de TI existem.
2. Como responsável pelo inventário, quero buscar e atualizar um ativo para manter responsável e localização corretos.
3. Como analista de segurança, quero registrar uma vulnerabilidade vinculada ao ativo para acompanhar sua severidade e tratamento.
4. Como analista de segurança, quero consultar e remover registros para corrigir o inventário sem deixar vulnerabilidades órfãs.

## Requisitos funcionais

| ID | Regra verificável | Referência ao PDF | Implementação |
| --- | --- | --- | --- |
| RF01 | Mostrar menu textual e rejeitar opção, campo ou tipo inválido sem encerrar o programa. | 1 | `trabalho1/app.py`, `validacoes.py` |
| RF02 | Oferecer ao menos quatro tipos de ativo com códigos inteiros em enumeração. | 2 | `TipoAtivo` |
| RF03 | Cadastrar ativo com ID inteiro único, nome, responsável, setor/localização, tipo e lista inicial de vulnerabilidades opcional; gravar em arquivo. | 3 | `Inventario.cadastrar_ativo`, `app.py`, `armazenamento.py` |
| RF04 | Consultar ativo por ID ou por nome/hostname e mostrar os campos de maneira organizada. | 4 | `Inventario.buscar_ativo`, `mostrar_ativo` |
| RF05 | Atualizar apenas um ativo existente, sem alterar o ID, e gravar os dados novos. | 5 | `Inventario.atualizar_ativo` |
| RF06 | Excluir ativo e suas vulnerabilidades associadas, mediante confirmação. | 6 | `Inventario.excluir_ativo` |
| RF07 | Cadastrar vulnerabilidade após o ativo, com descrição, categoria, severidade e status. | 7 | `Inventario.cadastrar_vulnerabilidade` |
| RF08 | Mostrar as vulnerabilidades de um ativo ou informar que não há registros. | 8 | `Inventario.listar_vulnerabilidades`, `mostrar_vulnerabilidades` |
| RF09 | Organizar ativos em dicionário indexado por ID inteiro. | 9 | `Inventario.ativos` |
| RF10 | Publicar código em repositório e demonstrar mais de duas branches e merges. | 10 | Histórico do GitHub |
| RF11 | Atualizar e remover uma vulnerabilidade por ID sem afetar as demais. | Complemento S2 | `Inventario.atualizar_vulnerabilidade`, `excluir_vulnerabilidade` |
| RF12 | Filtrar ativos por nome, tipo, criticidade e status e vulnerabilidades por CVE, ativo, severidade e status. | Complemento S2 | `listar_ativos`, `listar_vulnerabilidades` |

## Requisitos não funcionais

| ID | Regra verificável |
| --- | --- |
| RNF01 | Usar apenas a biblioteca padrão do Python 3.10 ou superior; execução por `python3 main.py`. |
| RNF02 | Preservar o arquivo original se a leitura falhar e gravar o JSON por substituição após concluir a escrita. |
| RNF03 | Não publicar o arquivo de dados, credenciais ou informações reais de pessoas no repositório. |
| RNF04 | Manter modelos, regras, menu e armazenamento separados e executar testes com `unittest`. |

## Regras de negócio

- ID de ativo e de vulnerabilidade são inteiros positivos. IDs de ativos e nomes não se repetem. IDs das vulnerabilidades são únicos no inventário.
- Uma vulnerabilidade só pode ser vinculada a um ativo existente. Excluir o ativo exclui suas vulnerabilidades no mesmo registro.
- Campos obrigatórios não podem ficar vazios. CVE e CVSS são opcionais; quando informados, devem respeitar formato e faixa.
- O ID é imutável. A exclusão física exige confirmação `EXCLUIR` no menu.
