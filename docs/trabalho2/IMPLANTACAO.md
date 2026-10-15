# Subir o Trabalho 02 na VPS

Use a branch `trabalho2/entregas` do repositório `LucazDiazUFU/sprints01e02`. Os arquivos estão na raiz. O Trabalho 01 continua em trabalho1 e o Trabalho 02 está em trabalho2. Recomendação para sua VPS com EasyPanel: App e MariaDB no mesmo projeto e na mesma rede interna.

## Opção A — EasyPanel e MariaDB existente

### 1. Preparar o banco

No serviço MariaDB, mantenha o volume persistente. Anote o host interno, porta interna 3306, banco, usuário e senha. Se o serviço já contém outros sistemas, crie um banco separado para este trabalho. O App não deve usar root.

No phpMyAdmin/DbGate ou console SQL do MariaDB, como administrador, execute uma única vez, substituindo a senha:

```sql
CREATE DATABASE trabalho02 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'trabalho02_app'@'%' IDENTIFIED BY 'SUBSTITUA_POR_SENHA_FORTE';
GRANT SELECT, INSERT, UPDATE, DELETE ON trabalho02.* TO 'trabalho02_app'@'%';
```

Se banco/usuário já existem, não repita CREATE nem altere a senha de outro sistema. Use as credenciais correspondentes. A origem `%` permite os endereços dos containers; mantenha o serviço acessível somente pela rede interna, sem publicar a porta 3306 na internet.

Selecione o banco trabalho02 e importe `deploy/schema_mariadb.sql` como administrador. Ele cria as duas tabelas e a linha de controle sem apagar registros. No terminal do cliente MariaDB, após selecionar o banco, também pode usar `SOURCE /caminho/schema_mariadb.sql;` se o arquivo estiver disponível ali. Não execute o schema SQLite `trabalho2/schema.sql` neste banco.

Para conferir:

```sql
SHOW TABLES;
SELECT * FROM trabalho2_controle;
SELECT id, JSON_VALID(dados), JSON_EXTRACT(dados, '$.nome')
FROM trabalho2_equipamentos;
```

Uma base nova terá versao=0 e nenhum equipamento.

### 2. Criar o App

No mesmo projeto do EasyPanel, adicione um serviço App chamado `trabalho02`. Configure a origem GitHub, autorize acesso ao repositório privado, escolha `LucazDiazUFU/sprints01e02` e a branch `trabalho2/entregas`. Use caminho de build `/` e builder Dockerfile, arquivo `Dockerfile` na raiz. Se o formulário pedir o caminho relativo, use `.`. Não escolha Nixpacks.

Na seção de ambiente do App, cole e substitua os valores:

```dotenv
DB_ENGINE=mariadb
DB_HOST=HOST_INTERNO_REAL_DO_MARIADB
DB_PORT=3306
DB_NAME=trabalho02
DB_USER=trabalho02_app
DB_PASSWORD=SENHA_REAL_DO_USUARIO
INVENTARIO_PRODUCAO=1
INVENTARIO_TOKEN=TOKEN_ALEATORIO_GERADO_POR_VOCE
```

Gere o token no terminal da VPS com `openssl rand -hex 32` e cole o resultado somente no ambiente do App. Use a mesma credencial para acessar a tela. Não coloque senhas no GitHub nem no chat. No EasyPanel, os valores são literais; não acrescente aspas ao redor da senha.

DB_HOST deve ser o host interno copiado do serviço, e não `localhost`, `127.0.0.1` ou o domínio HTTPS do painel. Dentro do App, localhost aponta para o próprio App. A porta é a interna 3306, mesmo se existir uma porta externa diferente para acesso pelo computador.

### 3. Domínio e volume

Adicione um domínio/subdomínio ao App, com destino HTTP para a porta interna `5000`; habilite HTTPS no proxy do EasyPanel. Exemplo de nome, se você possuir o domínio: trabalho02.seudominio.com.br. Não é preciso expor 5000 ou 3306 publicamente.

O MariaDB precisa do volume permanente em `/var/lib/mysql`, administrado pelo serviço do painel. Se for guardar exportações ou o CSV de monitoramento dentro do App, adicione um volume para `/app/dados`, com permissão de escrita para UID 10001. Os dados principais continuam no MariaDB; não precisam de volume no App. Um volume ou bind mount já existente com dono root pode exigir ajuste de dono pelo administrador antes do uso; não aplique chmod 777.

Mantenha uma réplica do App para este trabalho e pelo menos 512 MB de memória disponível para ele. O processo inicia Gunicorn com um worker e quatro threads. Não configure reinício periódico, suspensão ou scale-to-zero durante as 24h.

### 4. Implantar e abrir

Clique Deploy. Os logs podem mostrar “Aguardando o banco de dados...” por até 90 segundos. A inicialização não cria banco ou usuário, nem importa schema automaticamente. Depois deve aparecer o Gunicorn escutando em 0.0.0.0:5000.

Abra `https://SEU_DOMINIO/api/saude`. O resultado esperado é `status: ok` e `segundos_ativo`. Abra a página principal, expanda “Acessar inventário”, informe o token e clique “Atualizar lista”. O aviso inicial de credencial é normal antes de preencher o campo. O token fica em memória da página e é pedido novamente ao atualizar/fechar a aba.

Cadastre um equipamento e uma vulnerabilidade, consulte o risco e depois reinicie apenas o App. Os dados devem continuar no MariaDB. Essa conferência de implantação fica com Lucas; os testes automatizados permanecem pausados.

## Opção B — Docker Compose com banco existente

Na VPS, com Git e Docker Compose instalados:

```bash
git clone --branch trabalho2/entregas --single-branch https://github.com/LucazDiazUFU/sprints01e02.git
cd sprints01e02
cp .env.example .env
chmod 600 .env
nano .env
```

O repositório é privado: use a autenticação do seu Git, sem colocar um token na URL. Preencha `.env` com os dados reais. Em `.env` do Compose, senhas que tenham `$` ou `#` devem ser colocadas entre aspas simples para preservar seu valor; não copie essas aspas para o formulário do EasyPanel.

Se o MariaDB já roda em um container, descubra a rede dele e conecte o App a ela. O arquivo adicional usa uma rede Docker existente, que precisa aceitar containers externos:

```bash
docker network ls
```

Acrescente em `.env` o nome real:

```dotenv
DB_DOCKER_NETWORK=NOME_REAL_DA_REDE
```

Depois de criar banco, usuário e importar schema:

```bash
docker compose -f compose.yaml -f deploy/compose.rede.yaml up -d --build
docker compose -f compose.yaml -f deploy/compose.rede.yaml logs -f --tail=100 inventario
```

No Docker Swarm, a rede overlay do painel pode não aceitar containers externos. Nesse caso prefira o App nativo do EasyPanel no mesmo projeto, em vez de alterar redes de outros sistemas. Não use o host interno do EasyPanel em uma rede Compose isolada esperando que ele resolva automaticamente.

Se DB_HOST é um servidor acessível por IP privado, sem depender de rede Docker compartilhada, use somente `docker compose up -d --build`.

A porta do App fica vinculada ao loopback da VPS. Teste na própria VPS:

```bash
curl --fail http://127.0.0.1:5000/api/saude
```

Para abrir no computador sem domínio/proxy, execute no computador um túnel SSH e deixe o terminal aberto:

```bash
ssh -L 5000:127.0.0.1:5000 USUARIO_SSH@IP_DA_VPS
```

Abra `http://localhost:5000` no navegador. Para acesso permanente configure um proxy HTTPS. Evite misturar um Compose manual com o gerenciamento de domínio do EasyPanel sem configurar a rede correta.

## Opção C — aplicação e MariaDB novos com Compose

Use esta opção apenas se quiser um serviço MariaDB novo dedicado. Ela não utiliza o MariaDB que já está rodando.

```bash
cp deploy/.env.completo.example .env
chmod 600 .env
nano .env
docker compose -f compose.completo.yaml up -d --build
docker compose -f compose.completo.yaml ps
docker compose -f compose.completo.yaml logs -f --tail=100
```

Defina senhas diferentes para root e para o usuário do App, além do token. O container oficial cria o banco/usuário e importa `deploy/schema_mariadb.sql` na primeira inicialização do volume vazio. Os dados ficam no volume `banco`. Não execute `down -v`, pois isso remove os volumes e seus dados. Mudar as senhas no `.env` depois da primeira inicialização não muda automaticamente os usuários já gravados no banco.

## Backup e importação do Trabalho 01

Pela interface, use “Baixar JSON”. O arquivo contém uma lista de equipamentos, cada um com suas vulnerabilidades e dependências. Guarde a cópia fora da VPS. Também configure backups do banco no EasyPanel.

O arquivo legado do Trabalho 01 pode ser importado: a ferramenta aceita a lista JSON e também o formato antigo `{ "versao": 1, "ativos": [...] }`. Não apague a base anterior. Para a opção B simples:

```bash
docker compose exec -T inventario python -m trabalho2.transferencia exportar /app/dados/backup.json
docker compose cp inventario:/app/dados/backup.json ./backup-antes-importacao.json
docker compose cp ./ativos-antigos.json inventario:/tmp/ativos-antigos.json
docker compose exec -T inventario python -m trabalho2.transferencia importar /tmp/ativos-antigos.json --confirmar
```

Use os mesmos `-f` da implantação quando usar a rede adicional ou compose.completo.yaml. No EasyPanel, rode os comandos Python no console do App e disponibilize o JSON nele antes de importar. A importação substitui o inventário inteiro e só deve ser feita após backup. Não é uma junção automática de bases.

Para demonstrar o cenário resolvido à mão em um banco de demonstração:

```bash
python -m trabalho2.transferencia importar docs/trabalho2/cenario_exemplo.json --confirmar
```

Esse comando é executado dentro do App/container, com suas variáveis de ambiente. Ele substitui os dados atuais; use apenas na base de demonstração.

## Comprovar 24h

Depois de a aplicação estar estável, execute o monitor. No Compose, para mantê-lo mesmo ao fechar o SSH:

```bash
docker compose exec -d inventario python scripts/verificar_24h.py --url http://127.0.0.1:5000 --duracao 86400 --intervalo 60 --arquivo /app/dados/monitoramento_24h.csv
```

Não atualize nem reinicie o App durante a observação. O monitor exige resposta saudável e tempo ativo crescente; falha ou reinício interrompe a comprovação. Após o período, copie o CSV para seu computador e confira que há pelo menos 86400 segundos monitorados. O intervalo é amostral, não comprova cada milissegundo. A política de restart reinicia processo encerrado, mas o Docker não reinicia automaticamente um processo apenas por healthcheck unhealthy.

No EasyPanel, pode acompanhar pelo seu computador com Python 3 e o domínio HTTPS, deixando-o ligado:

```bash
python scripts/verificar_24h.py --url https://SEU_DOMINIO --duracao 86400 --intervalo 60 --arquivo monitoramento_24h.csv
```

O roteiro menciona o servidor do docente. Confirme se a evidência da sua VPS é aceita ou replique a implantação no servidor fornecido.

## Problemas de conexão

| Sintoma | O que conferir |
|---|---|
| Nome do host não resolve | App e banco na mesma rede; copiar o host interno real |
| Access denied | Usuário, senha, banco e origem permitida pelo MariaDB; senha do ambiente não troca usuário existente |
| Connection refused/timeout | Banco iniciado, rede e porta interna 3306; não usar localhost no App |
| Tabela não existe | Selecionar o banco correto e importar schema_mariadb.sql |
| 401 na tela | Token do App, campo na tela e botão Atualizar lista |
| Falha no build por Git | Autorizar o repositório privado no EasyPanel e selecionar a branch correta |
| Permission denied em /app/dados | Dono do volume/bind mount e UID 10001 |

Para conexão pela internet ou outra rede não confiável, use conexão privada/túnel ou TLS com verificação. O adaptador aceita `DB_SSL_CA=/caminho/ca.pem` e verifica certificado e hostname; monte o arquivo CA no App. Não habilite acesso público ao banco só para resolver a comunicação entre dois containers na mesma VPS.

Fontes de configuração: https://easypanel.io/docs/services/app , https://easypanel.io/docs/services/mariadb , https://hub.docker.com/_/mariadb .
