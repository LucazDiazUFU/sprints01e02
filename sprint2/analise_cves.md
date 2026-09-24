# S2_12 a S2_14 — exemplos de vulnerabilidades

Consulta às fichas da NVD em 24/09/2026. Os ativos abaixo são exemplos hipotéticos. O registro de uma CVE não prova que o software esteja instalado ou vulnerável; é preciso conferir produto e versão antes de abrir um incidente real.

| CVE e fonte | Ativo hipotético e motivo da prioridade | Tratamento e verificação |
| --- | --- | --- |
| [CVE-2021-44228 — NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-44228): falha no Apache Log4j 2 que pode permitir execução remota de código em configurações afetadas. | Aplicação web que usa uma versão afetada de Log4j. Prioridade crítica se estiver exposta e a versão for confirmada. | Responsável pela aplicação atualiza a dependência para versão corrigida indicada pelo fornecedor, verifica inventário de dependências e registra o teste após atualização. |
| [CVE-2023-34362 — NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-34362): injeção SQL em versões afetadas do MOVEit Transfer. | Servidor hipotético de transferência de arquivos com versão afetada e acesso pela rede. Prioridade alta/crítica conforme exposição e impacto dos dados. | Responsável pelo servidor aplica a correção do fornecedor, verifica a versão instalada, restringe exposição conforme necessidade e documenta nova checagem. |

No sistema, uma CVE pode ser cadastrada manualmente com descrição, categoria, severidade, status, referência e recomendação. O menu 7 filtra por CVE exata e combina ativo, severidade e status. Caso não haja registro, apresenta a ausência de resultados. A consulta externa é humana; não há integração automática com NVD.
