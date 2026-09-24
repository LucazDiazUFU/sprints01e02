# S2_05 — matriz de validações

| Campo | Regra | Erro apresentado |
| --- | --- | --- |
| ID de ativo/vulnerabilidade | Inteiro positivo, sem duplicidade | “deve ser um número inteiro positivo” / “Já existe” |
| Nome/hostname | Texto não vazio, até 120 caracteres, único ignorando caixa | “Nome não pode ficar vazio” / “Já existe um ativo com esse nome” |
| Responsável e setor | Texto não vazio, até 120 caracteres | “não pode ficar vazio” |
| Tipo | Código inteiro presente em `TipoAtivo` | “Tipo inválido” |
| Criticidade | BAIXA, MEDIA, ALTA ou CRITICA | “Criticidade inválido” |
| Status do ativo | ATIVO, INATIVO ou MANUTENCAO | “Status inválido” |
| Descrição da vulnerabilidade | Texto não vazio, até 500 caracteres | “Descrição não pode ficar vazio” |
| Categoria | Texto não vazio, até 120 caracteres | “Categoria não pode ficar vazio” |
| Severidade | BAIXA, MEDIA, ALTA ou CRITICA | “Severidade inválido” |
| Status da vulnerabilidade | ABERTA, EM_TRATAMENTO, CORRIGIDA ou RISCO_ACEITO | “Status inválido” |
| CVE | Opcional; quando preenchida, `CVE-AAAA-NNNN...` | “CVE inválida” |
| CVSS | Opcional; número finito entre 0 e 10 | “CVSS deve ser um número entre 0 e 10” |

Os testes cobrem exemplos válidos, campos vazios, duplicidade, registro inexistente, CVE fora do formato, CVSS abaixo/acima da faixa e `nan`.
