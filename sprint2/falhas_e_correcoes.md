# S2_18 — testes e correções

Comando: `python3 -m unittest discover -s tests -v`. A suíte cobre cadastro, busca, atualização e exclusão, além de persistência, duplicidade, registro ausente e valores de fronteira.

O teste `test_arquivo_com_raiz_invalida_preservado` começou falhando: um JSON válido com conteúdo `[]` causava `AttributeError`, pois o carregamento chamava `.get()` antes de confirmar que a raiz era um dicionário. Corrigi `carregar()` para verificar o tipo antes de acessar os campos. Depois da correção, o programa apresenta erro controlado e preserva o arquivo original. A falha e o resultado da correção foram executados localmente.

Também conferi que um arquivo JSON ilegível não seja sobrescrito na abertura do programa. O teste `test_arquivo_corrompido_preservado` escreve um arquivo inválido, verifica a mensagem de erro e confirma que o conteúdo original permanece. A função de CVSS usa `math.isfinite` para rejeitar `nan` e infinito. A execução final da suíte está em `sprint2/resultado_testes.txt`.
