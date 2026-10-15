# Trabalho 02 — inventário em orientação a objetos

O projeto continua o Trabalho 01. Os campos e as validações de ativos e vulnerabilidades foram reaproveitados. Equipamento deriva de Ativo; Notebook, Servidor e Roteador especializam comportamento. Inventario organiza os objetos, os repositórios persistem, AnaliseRisco calcula e Aplicacao controla o terminal. A interface web usa o mesmo cadastro por meio da API.

| Roteiro | Implementação | Evidência ou etapa restante |
|---|---|---|
| Objetos individuais, herança e polimorfismo — 20% | trabalho2/modelos.py e cadastro.py | Subclasses reconstruídas a partir de tipo; regras originais em trabalho1 |
| Persistência JSON em arquivo ou SQL — 20% | trabalho2/mariadb.py, armazenamento.py e deploy/schema_mariadb.sql | Cada equipamento é um objeto JSON com vulnerabilidades e dependencias; exportação e backup são listas desses objetos |
| Container estável por no mínimo 24h — 45% | Dockerfile, Compose e scripts/verificar_24h.py | Preparado; implantação e comprovação no servidor do docente ainda pendentes |
| Modelo linear de risco — 15% | trabalho2/risco.py, vista Análise de risco, /api/riscos | M, v, A, verificação numérica de invertibilidade, solução direta e resultados por ativo |

## Persistência

MariaDB utiliza InnoDB. trabalho2_equipamentos tem id e dados JSON. Os dados JSON de cada equipamento incluem suas vulnerabilidades e dependências. trabalho2_controle guarda a versão global para detectar alterações concorrentes. Uma transação bloqueia a linha de controle ao salvar, compara a versão, grava o conjunto e confirma. Se falhar, rollback preserva a versão anterior. A leitura usa uma transação com visão consistente.

Esta estratégia grava o inventário inteiro a cada alteração e atende ao porte acadêmico. Não foi projetada para inventários grandes ou alta concorrência. Senhas vêm de variáveis de ambiente. A aplicação só precisa de SELECT, INSERT, UPDATE e DELETE nas tabelas; o administrador importa o schema antes de iniciar.

O modo SQLite continua disponível para os exercícios locais da S3. O modo MariaDB é o indicado nesta entrega. Não há migração automática de dados pessoais antigos: use a transferência JSON após backup.

## Risco resolvido à mão

O arquivo cenario_exemplo.json tem três equipamentos e quatro vulnerabilidades. A ordem dos equipamentos é 101, 102, 103; das vulnerabilidades, 201, 202, 203, 204.

M = [[1,1,0,0],[0,0,1,0],[0,0,0,1]], v = [4,6,8,2], b = Mv = [10,8,2].

A = [[0,0.2,0],[0,0,0.25],[0,0,0]]. O elemento Aij é a parcela do risco de j recebida por i.

x3 = 2; x2 = 8 + 0.25×2 = 8.5; x1 = 10 + 0.2×8.5 = 11.7.

Logo x = [11.7,8.5,2]. I-A é triangular com diagonal 1; seu determinante é 1. A soma de cada linha de A é menor que 1. O cadastro impõe essa regra, diagonal zero, pesos não negativos e menores que 1, além de exigir que os ativos existam.

O programa verifica posto e condicionamento antes de np.linalg.solve. O resíduo mostra quanto a solução satisfaz o sistema. Fatores de exposição por tipo são opcionais e começam desmarcados; assim o cálculo padrão coincide com o roteiro. Severidades sem CVSS usam BAIXA=2, MEDIA=5, ALTA=8, CRITICA=10. Todas as vulnerabilidades registradas entram no modelo; para excluir uma do cenário de risco, remova o registro. Os escores não são probabilidades.

## Apresentação em cinco minutos

1. Mostre as classes e explique que cada ativo é um objeto, com dados comuns herdados de Ativo.
2. Cadastre um ativo e uma vulnerabilidade, depois atualize e consulte. Mostre a recusa de um ID repetido e o cancelamento de uma exclusão.
3. Reinicie apenas o container da aplicação e mostre os dados novamente, comprovando persistência no MariaDB.
4. Em uma base de demonstração, importe o cenário pequeno, apresente as dependências e confira b e x com os valores acima.
5. Mostre o container e o CSV de observação real. Só afirme 24h depois de o monitor terminar com sucesso. A exigência cita o servidor disponibilizado pelo docente; confirme com ele se a sua VPS pode ser usada como evidência.

## Estado desta versão

Código e arquivos de implantação preparados. Os testes continuam pausados por solicitação de Lucas. Os resultados anteriores da S3 não validam o novo adaptador MariaDB. Neste ambiente não há Docker nem servidor MariaDB; construção da imagem e integração real precisam ser conferidas na implantação. Não foi alegada execução de 24h.
