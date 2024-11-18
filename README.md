# Projeto de cloud

## Autor do repositório:
Tomas Rolim Miele

## Explicação do Projeto
Esse projeto consiste na criação de uma API RESTfull 
com a implementação de 3 endpoints. O primeiro sendo
o registro de um novo usuário, o segundo o login deste
usuário e por fim uma consulta sobre as últimas atualizações de uma ação de sua escolha, caso não seja
passada nenhuma ação o endpoint coletará essas informações
sobre a ação da Apple (AAPL).

## Explicação de Como Executar a Aplicação

### Baixando o repositório:
1. Clone o repositório:  

Copie o linke a baixo e cole-o no terminal de seu computador e execute o comando. (Sugestão: antes de clonar o repositório entre no diretório do Downloads ou Desktop).
>https://github.com/tomasmiele/cloud-projeto.git

2. Entre no repositório:  

Para isso, ainda no terminal execute o comando:

>```bash
>cd cloud-projeto
>```

3. Rodar a aplicação:

Abra o aplicativo do Docker e deixe-o rodando, feito isso execute no terminal, dentro da pasta que acabamos de entrar, o comando:

>```bash
>docker compose up 
>```

4. Teste dos endpoints:

Mais adiante explicarei detalhadamente cada endpoint, ou seja, o que você deve passar como parâmetro para eles e o que esperar como retorno.

Para acessá-los entre em um browser, como o Google Chrome, e coloque esse link:

>http://localhost:8000/docs

Pronto! A aplicação está pronta para uso.

### Baixando apenas o Compose:
1. Crie o arquivo compose

(Sugestão: antes de criar o arquivo entre no diretório do Downloads ou Desktop)

Crie um arquivo chamado docker-compose.yalm ou compose.yalm e cole o conteúdo a sequir nele.

> ```
>services:
>  db:
>    image: postgres:15
>    container_name: postgres_container
>    environment:
>      - POSTGRES_USER=${POSTGRES_USER:-projeto}
>      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-projeto}
>      - POSTGRES_DB=${POSTGRES_DB:-projeto}
>    ports:
>      - "5432:5432"
>
>  app:
>    image: tomasmiele/cloud-projeto:latest
>    container_name: fastapi_app
>    environment:
>      - POSTGRES_USER=${POSTGRES_USER:-projeto}
>      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-projeto}
>      - POSTGRES_DB=${POSTGRES_DB:-projeto}
>      - DB_HOST=db
>      - DB_PORT=5432
>      - SECRET_KEY=${SECRET_KEY}
>      - API_KEY=${API_KEY:-H456ZLCOCHH7CH10}
>    ports:
>      - "8000:8000"
>    depends_on:
>      - db
> ```

2. Rodar a aplicação:

Abra o aplicativo do Docker e deixe-o rodando, feito isso abra o terminal da sua máquina (caso tenha clonado em uma pasta específica entre nela) e execute o comando:

>```bash
>docker compose up 
>```

3. Teste dos endpoints:

Como dito, mais adiante explicarei detalhadamente cada endpoint, ou seja, o que você deve passar como parâmetro para eles e o que esperar como retorno.

Para acessá-los entre em um browser, como o Google Chrome, e coloque esse link:

>http://localhost:8000/docs

Pronto! A aplicação está pronta para uso.

## Documentação dos Endpoints 
### POST: "/registrar"
Essa rota é encarregada de criar um novo usuário no sistema. O retorno esperado é um token JWT para o usuário registrado.

#### Parâmetros de entrada:

- nome (string): Nome do usuário. (Obrigatório)
- email (string): Email do usuário. (Obrigatório)
- senha (string): Senha do usuário. (Obrigatório)

![Param registrar](img/param_registrar.png)

#### Exemplo de Requisição

> ```json
> {
>  "nome": "Humberto Sandmann",
>   "email": "humberto@example.com",
>   "senha": "senha123"
> }
> ```

#### Respostas:

200 OK: Usuário registrado com sucesso. Retorna o token JWT.
> ```json
> {"jwt": "token_jwt_gerado"}
> ```
![200 registrar](img/200_registrar.png)

409 Conflict: Email já registrado
> ```json
> {"detail": "Email já registrado."}
> ```
![409 registrar](img/409_registrar.png)

### POST: "/login"
Aqui o objetivo é testar se um usuário já está cadastrado, para isso esse endpoint autentica o usuário com email e senha. Caso esteja cadastrado, será gerado o mesmo token JWT quando criado o usuário.

#### Parâmetros de entrada:

- email (string): Email do usuário. (Obrigatório)
- senha (string): Senha do usuário. (Obrigatório)

![Param login](img/param_login.png)

#### Exemplo de Requisição

> ```json
> {
>   "email": "humberto@example.com",
>   "senha": "senha123"
> }
> ```

#### Respostas:

200 OK: Login bem-sucedido. Retorna o token JWT.
> ```json
>{"jwt": "token_jwt_gerado"}
>```

![200 login](img/200_login.png)

401 Unauthorized: Email não registrado ou senha incorreta.
> ```json
> {"detail": "Email não registrado."}
> ```  
![401 login](img/401_login_email.png)
ou
> ```json
> {"detail": "Senha incorreta."}
> ```
![401 login](img/401_login_senha.png)

### GET: "/consultar"
O objetivo aqui é validar se o usuário já foi cadastrado, para isso no header é passado o token gerado ao cadastrado. Além disso há uma consulta a respeito de informações diárias de uma ação especificada (caso nenhuma ação seja passada a opção padrão é a AAPL) retornando os dados dos últimos 5 dias.

#### Parâmetros de entrada:

- acao (query parameter): Símbolo da ação a ser consultada. Caso não seja passado nada nenhum parâmetro ele assume a ação da Apple (AAPL) como padrão.
- Autenticação: O usuário precisa estar autenticado com um token JWT válido.

![Endpoint consultar](img/endpoint_consultar.png)

Exemplo de Requisição
> ```bash
>GET /consultar?acao=AAPL
> ```

> ```json
> {"acao": "AAPL"}
> ```

#### Respostas:

200 OK:  Retorna as informações dos últimos 5 dias da ação especificada ou a padrão.
> ```json
> {  
>  "Informações dos últimos 5 dias da Ação: AAPL": {  
>          "1. open": { ... },  
>          "2. high": { ... },  
>          "3. low": { ... },  
>          "4. close": { ... },  
>          "5. volume": { ... }  
>  }   
> }
> ```

![200 consultar](img/200_consultar.png)

203 Forbidden: Token não autenticado.
>``` json
>{"detail": "Not authenticated"}
>```

![203 consultar](img/203_consultar.png)

204 No Content: Ação não encontrada.
> ``` json
>{"detail": "Não existe essa ação."}
> ```

![204 consultar](img/204_consultar.png)

## Vídeo de Execução da Aplicação

[Vídeo Testando Execução](https://youtu.be/UqpAmjzpcYY)

## Docker Hub
https://hub.docker.com/repository/docker/tomasmiele/cloud-projeto/general

## Código do docker-compose.yaml
### Copiar Arquivo:

Crie um arquivo chamado docker-compose.yalm ou compose.yalm e cole o conteúdo a sequir nele.

> ```
>services:
>  db:
>    image: postgres:15
>    container_name: postgres_container
>    environment:
>      - POSTGRES_USER=${POSTGRES_USER:-projeto}
>      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-projeto}
>      - POSTGRES_DB=${POSTGRES_DB:-projeto}
>    ports:
>      - "5432:5432"
>
>  app:
>    image: tomasmiele/cloud-projeto:latest
>    container_name: fastapi_app
>    environment:
>      - POSTGRES_USER=${POSTGRES_USER:-projeto}
>      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-projeto}
>      - POSTGRES_DB=${POSTGRES_DB:-projeto}
>      - DB_HOST=db
>      - DB_PORT=5432
>      - SECRET_KEY=${SECRET_KEY}
>      - API_KEY=${API_KEY:-H456ZLCOCHH7CH10}
>    ports:
>      - "8000:8000"
>    depends_on:
>      - db
> ```

## Deploy na AWS

Os requisitos para a realização desse deploy eram:

1. "[...] A implantação deve ser feita utilizando o Elastic Kubernetes Service (EKS). A aplicação deve ser implantada em um cluster EKS."
2. "Você deve subir um cluster EKS e implantar dois PODs, sendo um da aplicação e outro do banco de dados. A aplicação deve ser capaz de se conectar ao banco de dados e realizar as operações de endpoints da API acima descritas."

### Acesso na conta AWS
Após entrar na sua conta AWS acessaremos o CloudShell para a realização de um deploy rápido e prático. Essa ferramenta pode ser achada através da "Search Engine" ou clicando no botão da foto abixo.

![CloudShell](img/CloudShell.png)

Para saber mais do CloudShell: [Saiba mais](https://docs.aws.amazon.com/pt_br/cloudshell/latest/userguide/welcome.html)

### Por que usar o CloudShell?

Essa ferramenta já possui o AWS CLI e o EKSCTL instalados, o que facilitará o processo de deploy da nossa aplicação

### 1. Criação do cluster EKS

>```bash
>eksctl create cluster --name {NOME DO SEU PROJETO} --region {REGIÃO DE INTERESSE} --nodes 2
>```

Note: aqui usaremos 2 nós, porém dependendo da sua aplicação esse valor por variar. Para a região, escolha a mais adequada para sua aplicação

### 2. Configuração do kubectl

>```bash
>aws eks --region {REGIÃO DE INTERESSE} update-kubeconfig --name {NOME DO SEU PROJETO}
>```

### 3. Criação do arquivo do banco de dados

>```bash
>nano nome-do-arquivo.yml
>```

Configure o arquivo conforme o suas especificidades, no caso desse tutoria será:

>```
>apiVersion: apps/v1
>kind: Deployment
>metadata:
>  name: postgres-db-cloud
>spec:
>  replicas: 1
>  selector:
>    matchLabels:
>      app: postgres
>  template:
>    metadata:
>      labels:
>        app: postgres
>    spec:
>      containers:
>        - name: postgres
>          image: postgres:15
>          ports:
>            - containerPort: 5432
>          env:
>            - name: POSTGRES_USER
>              value: "projeto"
>            - name: POSTGRES_PASSWORD
>              value: "projeto"
>            - name: POSTGRES_DB
>              value: "projeto"
>---
>apiVersion: v1
>kind: Service
>metadata:
>  name: postgres
>spec:
>  ports:
>    - port: 5432
>  selector:
>    app: postgres
>```

Para realizar o deploy execute o comando abaixo:

>```bash
>kubectl apply -f nopme-do-arquivo.yml
>```

Para verificar o pod rodando execute:

>```bash
>kubectl get pods
>```

### 4. Criação do arquivo app

Essa parte será uma duplicata da parte anterior porém para aplicação

>```bash
>nano nome-do-arquivo.yml
>```

>```
>apiVersion: apps/v1
>kind: Deployment
>metadata:
>  name: fastapi-app
>spec:
>  replicas: 1
>  selector:
>    matchLabels:
>      app: fastapi
>  template:
>    metadata:
>      labels:
>        app: fastapi
>    spec:
>      containers:
>        - name: fastapi
>          image: tomasmiele/cloud-projeto:latest
>          ports:
>            - containerPort: 8000
>          env:
>            - name: DATABASE_URL
>              value: "postgresql://projeto:projeto@postgres:5432/projeto"
>            - name: SECRET_KEY
>              value: "581fc9c4fdda675143cfd3d2d65b1ceeec42f4e1e1be182fe26d7f32961eb223cfdc4c6da159e4e8c48c86e419763e7597af855f179df92416241c47e5083f5c476b46e3efd26ea1491f723f555370b9dc62c8f532559759c7345dd93b2ecd67f5b21ec1af42f7f32e3f4283d3ca2e0e2e155159cc7ba8fb5cccfdff217c3f31b7832ad4952f5e2c747954cc91111772a04bb7bed7a5a149b88632b8314dfae1dd01c33c75d084d2ebcbd1b54fcd9a8a0102eb27d58ae65c4573402dff168f01960ef6dc7be7eedb95d5b28f3b35461b5662a243d487b0ef818a01d00d83e7e8753c59c3ba163cbe85774f4c70af4269d0829c06d603e1f89d4e333be4768f24"
>            - name: API_KEY
>              value: "H456ZLCOCHH7CH10"
>---
>apiVersion: v1
>kind: Service
>metadata:
>  name: fastapi-service
>spec:
>  type: LoadBalancer
>  ports:
>    - port: 80
>      targetPort: 8000
>  selector:
>    app: fastapi
>```

Para realizar o deploy execute o comando abaixo:

>```bash
>kubectl apply -f nopme-do-arquivo.yml
>```

Para verificar o pod rodando execute:

>```bash
>kubectl get pods
>```

### 5. Acesse sua aplicação:

Execute o comando abaixo para listar os serviços disponíveis no cluster e obter o **EXTERNAL-IP**:

>```bash
>kubectl get svc fastapi-service
>```

EXTERNAL-IP: Este é o IP público da aplicação. Use-o para acessá-la.

Caso o campo EXTERNAL-IP apareça como <pending>, aguarde alguns minutos até que o LoadBalancer seja provisionado.

Para testar a aplicação:

Acesse um navegador e copie o EXTERNAL-IP da saída do comando anterior.
A barra de pesquisa será parecida com:

>```
>http://<EXTERNAL-IP>
>```

