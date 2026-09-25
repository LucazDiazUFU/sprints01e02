# S2_01 — refatoração e decisões

No programa inicial `s1_07.py`, a classificação de uma severidade era feita por faixas numéricas com condições repetidas. No Trabalho 1, o usuário informa diretamente uma das quatro severidades. Centralizei a verificação em `opcao()` e `SEVERIDADES`, em `validacoes.py`, para que o cadastro e a atualização apliquem a mesma regra. Os nomes das funções indicam a operação realizada. O menu só coleta e exibe dados; `Inventario` executa as regras e `armazenamento.py` grava o arquivo.

Para o fluxo do novo programa, a entrada `alta` é normalizada para `ALTA`, e uma opção desconhecida continua gerando erro sem inserir registro. Os testes `test_cadastrar_e_consultar_vulnerabilidade` e `test_cadastro_invalido_nao_altera_base` verificam esse comportamento. A refatoração mantém o significado das quatro categorias, mas a entrada mudou de nota numérica para categoria textual conforme o registro pedido pelo Trabalho 1.
