# Critérios de aceitação — versão 1.0

## Ativos

| Operação | Dado | Quando | Então | Teste |
| --- | --- | --- | --- | --- |
| Criar | Um ID inteiro livre e todos os campos obrigatórios válidos | O usuário cadastra o ativo | O registro aparece na busca e continua após reiniciar | `test_cadastrar_buscar_por_id_e_nome`, `test_persistencia_apos_reiniciar` |
| Criar | Um ID ou nome já cadastrado | O usuário tenta cadastrar outro ativo | O programa informa a duplicidade e preserva o registro anterior | `test_cadastro_com_id_repetido`, `test_cadastro_com_nome_repetido` |
| Consultar | Um ativo já cadastrado | O usuário informa o ID ou o nome em caixa diferente | O mesmo ativo é apresentado | `test_cadastrar_buscar_por_id_e_nome` |
| Consultar | Um ID ausente | O usuário busca o registro | A resposta é vazia, sem erro de chave | `test_busca_e_filtros_combinados` |
| Atualizar | Um ativo existente | O usuário muda apenas o responsável | O ID e os outros campos permanecem e o histórico registra antes/depois | `test_atualizacao_parcial_e_historico` |
| Atualizar | Campo vazio ou ID inexistente | O usuário tenta atualizar | A alteração é recusada e os dados anteriores permanecem | `test_atualizacao_invalida_preserva_ativo`, `test_atualizacao_de_inexistente` |
| Excluir | Um ativo com vulnerabilidade | O usuário confirma `EXCLUIR` | O ativo e suas vulnerabilidades são removidos | `test_exclusao_exige_confirmacao_e_remove_vulnerabilidades` |
| Excluir | Um ativo sem confirmação ou ID ausente | O usuário cancela ou informa ID ausente | O registro fica intacto ou o programa informa ausência | `test_exclusao_exige_confirmacao_e_remove_vulnerabilidades`, `test_exclusao_de_inexistente` |

## Vulnerabilidades

| Situação | Dado | Quando | Então | Teste |
| --- | --- | --- | --- | --- |
| Cadastro | Ativo existente, descrição, categoria, severidade e status válidos | O usuário informa uma vulnerabilidade | Ela aparece na consulta daquele ativo | `test_cadastrar_e_consultar_vulnerabilidade` |
| Vínculo inválido | Ativo inexistente | O usuário tenta cadastrar | O cadastro é recusado, sem registro órfão | `test_vulnerabilidade_sem_ativo` |
| Valor inválido | CVE mal formatada ou CVSS fora de 0 a 10 | O usuário tenta cadastrar | O programa informa o erro e não cria o registro | `test_cve_invalida`, `test_cvss_fora_da_faixa_e_nan` |
| Filtro | CVE existente e severidade conhecida | O usuário combina filtros | Apenas os registros correspondentes aparecem | `test_cve_cvss_e_filtros` |

## Definição de pronto

Código versionado, execução limpa, testes aprovados, README com instruções e demonstração dos dez requisitos. A revisão final será feita pelo estudante; a apresentação e a avaliação ocorrerão em sala.
