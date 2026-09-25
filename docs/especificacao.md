# Especificação do inventário de segurança

Versão 1.0 — 24/09/2026. Responsável pelo projeto: Lucas Dias dos Santos. Fonte: Trabalho 1 da disciplina de Cibersegurança da UFU, versão 2.0 (2026/2). Esta versão consolida a interpretação do enunciado e os cartões S2_01 a S2_19.

## Objetivo e escopo

Manter um inventário local de ativos de TI e suas vulnerabilidades, por menu textual em Python. Um usuário opera o programa no próprio computador. Não há autenticação, rede, sincronização ou consulta automática a bases externas. Os exemplos de CVE documentados são apenas estudo; o usuário insere vulnerabilidades manualmente.

## Entradas, saídas e dados

| Entidade | Campos | Regra |
| --- | --- | --- |
| Ativo | `id`, `nome`, `responsavel`, `setor`, `tipo`, `criticidade`, `status`, `descricao` | ID inteiro positivo único; nome único sem diferenciar caixa; tipo 1 a 6; campos básicos obrigatórios. |
| Vulnerabilidade | `id`, `descricao`, `categoria`, `severidade`, `status`, `cve`, `cvss`, `referencia`, `recomendacao` | ID inteiro positivo único; quatro campos básicos obrigatórios; CVE e CVSS opcionais. |
| Relação | `Ativo.vulnerabilidades` | Lista de vulnerabilidades dentro do ativo; exclusão do ativo remove a lista. |
| Persistência | `trabalho1/ativos.json` | Arquivo texto JSON UTF-8 com `versao` e lista de ativos, regravado após alterações. |

O programa apresenta os campos ao cadastrar, consultar, atualizar e excluir. Mensagens de erro identificam opção inválida, campo vazio, ID repetido, registro inexistente e arquivo ilegível. O histórico antes/depois fica em memória durante a execução; o enunciado não exige persistência de auditoria.

## Regras e funções

`TipoAtivo` é uma enumeração de códigos inteiros. `Ativo` e `Vulnerabilidade` validam seus dados ao serem criados. `Inventario` guarda `ativos` em um dicionário e executa o CRUD. O menu em `app.py` recebe entradas e confirma exclusões. `armazenamento.py` lê e grava JSON. Consulte [requisitos](requisitos.md), [matriz de validações](../sprint2/matriz_validacoes.md) e [critérios de aceitação](criterios_aceitacao.md).

## Rastreabilidade

| Requisitos | Código | Evidência |
| --- | --- | --- |
| RF01–RF03 | `app.py`, `validacoes.py`, `modelos.py`, `cadastro.py`, `armazenamento.py` | Testes de menu, cadastro, enumeração e persistência. |
| RF04–RF06 | `cadastro.py` | Testes de busca, atualização, exclusão e ID ausente. |
| RF07–RF09 | `modelos.py`, `cadastro.py` | Testes de vínculo, consulta, filtro e dicionário. |
| RF10 | Branches, commits, merges e PR no GitHub | Histórico do repositório. |
| RF11–RF12 | `cadastro.py` | Testes de atualização, exclusão e filtros de vulnerabilidades. |

## Restrições e revisão

O programa precisa de Python 3.10 ou superior e usa somente a biblioteca padrão. Dados reais e segredos não entram no repositório. Os testes automatizados verificam regras centrais; a revisão final, a apresentação de cinco minutos e a explicação individual são responsabilidade do estudante.
