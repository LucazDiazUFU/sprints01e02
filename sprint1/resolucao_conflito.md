# Resolução de conflito

Criei duas branches a partir da versão que dizia `Status: Pendente`. Na branch `teste/conflito-a`, alterei a linha para `Status: Ativo`. Na `teste/conflito-b`, alterei a mesma linha para `Status: Em manutenção`. Ao tentar integrar a primeira na segunda, o Git indicou conflito em `exemplo.txt`.

Escolhi `Status: Em manutenção` como resultado do exercício, retirei os marcadores de conflito, conferi o arquivo e finalizei o merge com o commit `bbc2ab1` (`Resolve conflito de status`). A escolha ilustra a resolução técnica; no sistema real, a situação correta do ativo teria de ser confirmada com o responsável.

As branches e o commit podem ser verificados no arquivo `sprint1_git.bundle`.
