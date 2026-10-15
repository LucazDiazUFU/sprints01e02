# Sprint 3

A entrega mantém os campos e as regras do Trabalho 01 e acrescenta os assuntos da S3. Os códigos novos não têm comentários. Cada atividade possui um relatório com arquivos, resultados e limites.

| Atividade | Relatório |
|---|---|
| S3_01 — Herança, polimorfismo e abstração | [S3_01.md](S3_01.md) |
| S3_02 — Funções de alta ordem e recursão | [S3_02.md](S3_02.md) |
| S3_03 — Filas e listas encadeadas | [S3_03.md](S3_03.md) |
| S3_04 — Análise de algoritmos e complexidade | [S3_04.md](S3_04.md) |
| S3_05 — Busca e ordenação | [S3_05.md](S3_05.md) |
| S3_06 — Qualidade de software e código limpo | [S3_06.md](S3_06.md) |
| S3_07 — Estratégias de teste e testes unitários | [S3_07.md](S3_07.md) |
| S3_08 — GitHub, pull requests e integração contínua | [S3_08.md](S3_08.md) |
| S3_09 — Matrizes e transformações lineares | [S3_09.md](S3_09.md) |
| S3_10 — Sistemas lineares | [S3_10.md](S3_10.md) |
| S3_11 — Determinantes e invertibilidade | [S3_11.md](S3_11.md) |
| S3_12 — Erros numéricos | [S3_12.md](S3_12.md) |
| S3_13 — Lógica proposicional e argumentação | [S3_13.md](S3_13.md) |
| S3_14 — Portas lógicas e arquitetura | [S3_14.md](S3_14.md) |
| S3_15 — Usabilidade, prototipação e acessibilidade | [S3_15.md](S3_15.md) |
| S3_16 — Front-end moderno | [S3_16.md](S3_16.md) |
| S3_17 — JavaScript assíncrono e APIs | [S3_17.md](S3_17.md) |
| S3_18 — APIs REST e testes de integração | [S3_18.md](S3_18.md) |
| S3_19 — Backend e persistência | [S3_19.md](S3_19.md) |
| S3_20 — Redes, segurança, LGPD e sustentabilidade | [S3_20.md](S3_20.md) |

## Executar

Requer Python 3.12. Na raiz do repositório:

```bash
python3 -m pip install -r requirements-dev.txt
python3 main_trabalho2.py
python3 -m flask --app trabalho2.api:criar_app run --host 127.0.0.1 --port 5000
```

O terminal e o servidor usam bases distintas. Abra http://127.0.0.1:5000 para a interface. Os arquivos de dados não devem ser enviados ao GitHub.

```bash
python3 -m pytest -q
python3 -m sprint3.gerar_evidencias
docker compose up --build -d
python3 scripts/verificar_24h.py --url http://127.0.0.1:5000
```

O monitoramento padrão dura 86400 segundos. O teste curto só verifica o monitor, sem comprovar 24h. O servidor do docente e o acesso necessário devem ser providenciados por Lucas. O protótipo SVG precisa ser importado no Figma para concluir essa parte da S3_15. A revisão humana da S3_08 e a apresentação ficam com Lucas.

A atividade Trabalho 02 copiada no Product Backlog inclui Sprints 3, 4 e 5. Esta entrega cobre a base da Sprint 3; não declara o trabalho inteiro concluído.
