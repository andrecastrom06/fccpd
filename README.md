# fccpd
Projeto da cadeira de Fundamentos de Computação Concorrente, Paralela e Distribuída

👤 André Castro - andre20072006@gmail.com

<details>
  <summary>Desafio 1</summary>

## Containers em Rede

### Objetivo
Criar dois containers que se comunicam usando uma rede Docker customizada criada pelo `docker-compose`.

---

### Descrição da Solução
- Um container roda um servidor **Flask** simples expondo `/`.
- Outro container roda um script que faz requisições periódicas usando **curl**.
- Ambos estão na mesma rede nomeada (`desafio_net`), o que permite que o hostname `server` resolva automaticamente para o IP do container.

---

### Funcionamento
- O **server** escuta em `0.0.0.0:8080`.
- O **client** envia `curl http://server:8080/` em loop com intervalo configurável.
- A comunicação é feita via DNS interno do Docker.
- Os logs mostram o horário e status HTTP de cada requisição.

---

### Passo a Passo
1. **Subir o ambiente**
   ```bash
   ./run.sh
   ```

2. **Ver containers ativos**
   ```bash
   ./run.sh
   ```

3. **Confirmar a rede criada**
   ```bash
   docker network ls | grep desafio_net
   ```

4. **Acompanhar logs**
   #### Server
      ```bash
      docker logs -f desafio_server
      ```

   #### Client
      ```bash
      docker logs -f desafio_client
      ```   

5. **Encerrar e limpar tudo**
   ```bash
   ./run.sh stop
   ```   
</details>


<details>
  <summary>Desafio 2</summary>
  
## Volumes e Persistência

### Objetivo
Demonstrar que os dados continuam existindo mesmo após a remoção do container, usando **volumes Docker** para armazenar o banco fora do container.

---

### Descrição da Solução
A solução usa um container **PostgreSQL** com um volume nomeado.  
O script `init.sql` cria uma tabela e insere um registro inicial.  
O diretório interno do PostgreSQL (`/var/lib/postgresql/data`) é montado em um volume Docker (`desafio2_data`), garantindo que a remoção do container não apague os dados.  
Ao recriar o container, o banco recarrega automaticamente o conteúdo do volume.

---

### Funcionamento
1. O PostgreSQL sobe pela primeira vez.  
2. O `init.sql` cria a tabela e insere o primeiro registro.  
3. Os dados ficam armazenados no volume `desafio2_data`.  
4. O container é removido com `./run.sh stop`, mas o volume permanece.  
5. Ao subir novamente (`./run.sh`), o PostgreSQL lê os dados do volume.  
6. A consulta mostra que os registros continuam lá — provando a persistência.

---

### 🚀 Passo a Passo
1. **Subir o container**
   ```bash
   ./run.sh
   ```

2. **Verificar o registro inicial**
   ```bash
   docker exec -it $(docker ps -qf "ancestor=postgres:15") psql -U user -d teste -c "SELECT * FROM registros;"
   ```

3. **Parar e limpar tudo (inclusive volume)**
   ```bash
   ./run.sh stop
   ```

4. **Subir novamente**
   ```bash
   ./run.sh
   ```

5. **Confirmar que o dado ainda existe**
   ```bash
   docker exec -it $(docker ps -qf "ancestor=postgres:15") psql -U user -d teste -c "SELECT * FROM registros;"
   ```

6. **Encerrar e limpar tudo**
   ```bash
   ./run.sh stop
   ```  
</details>

<details>
  <summary>Desafio 3</summary>
  
## Docker Compose Orquestrando Serviços
* **Objetivo:** Usar Docker Compose para orquestrar três serviços interligados (web, db, cache) utilizando rede interna, variáveis de ambiente e `depends_on`.

* **Descrição da solução:**  
  A solução utiliza três containers:  
  - **web:** aplicação Flask que consulta o PostgreSQL e o Redis.  
  - **db:** banco de dados PostgreSQL para armazenar informações.  
  - **cache:** serviço Redis usado como cache in-memory.  

  O `docker-compose.yml` define os serviços, as dependências e a rede interna `desafio3_net`, permitindo que os containers se comuniquem via hostname (`web`, `db`, `cache`).  
  O serviço `web` só inicia após `db` e `cache`, garantindo que as dependências estejam prontas.

* **Funcionamento explicado:**  
  - O Compose cria e conecta automaticamente os 3 serviços na mesma rede.  
  - O web acessa o banco via `host=db` e o cache via `host=cache`.  
  - O PostgreSQL armazena dados em volume interno.  
  - O Redis mantém informações em memória e responde ao teste de conectividade.  
  - A rota `/` do Flask retorna o status da comunicação com ambos os serviços.  

* **Passo a passo para execução:**  
  1. Subir os serviços:
     ```bash
     docker compose up -d
     ```
  2. Verificar se os containers estão rodando:
     ```bash
     docker ps
     ```
  3. Testar a comunicação do serviço web:
     ```bash
     curl http://localhost:8080/
     ```
  4. Validar comunicação entre containers:
     - Testar PostgreSQL:
       ```bash
       docker exec -it desafio3_db psql -U user -d teste -c "SELECT NOW();"
       ```
     - Testar Redis:
       ```bash
       docker exec -it desafio3_cache redis-cli ping
       ```
     - Testar resolução de host:
       ```bash
       docker exec -it desafio3_web ping db
       docker exec -it desafio3_web ping cache
       ```
  5. Derrubar tudo:
     ```bash
     docker compose down
     ```
</details>

<details>
  <summary>Desafio 4</summary>

## Microsserviços Independentes

### Objetivo
Criar dois microsserviços independentes que se comunicam via HTTP, cada um rodando em seu próprio container Docker.

### Descrição da solução
Foram criados dois serviços:

- **Microsserviço A (service_a):**
  - Expondo o endpoint `/users`
  - Retorna uma lista JSON de usuários
  - Implementado em Flask
  - Container próprio com Dockerfile dedicado

- **Microsserviço B (service_b):**
  - Consome o microsserviço A via HTTP
  - Endpoint `/consume` retorna dados combinados
  - Implementado em Flask + Requests
  - Container próprio com dependência explícita do serviço A

A comunicação entre ambos ocorre pelo hostname interno `service_a`, via rede padrão criada pelo Docker Compose.

### Funcionamento explicado
- O **service_a** inicia e disponibiliza a lista de usuários.
- O **service_b** sobe depois (via `depends_on`) e faz chamadas HTTP para `service_a:5000/users`.
- Os dois containers estão na mesma rede interna do compose, então não precisam de IP fixo.
- O acesso externo é feito pelas portas mapeadas:
  - `5001` → microsserviço A
  - `5002` → microsserviço B

### Passo a passo para execução

1. **Iniciar os containers**
   ```bash
   docker compose up --build -d
   ```

2. **Listar containers rodando**
   ```bash
   docker ps
   ```

3. **Testar o microsserviço A**
   ```bash
   curl http://localhost:5001/users
   ```

4. **Testar o microsserviço B consumindo o A**
   ```bash
   curl http://localhost:5002/consume
   ```

5. **Ver logs**
   ```bash
   docker logs -f desafio4_service_a
   docker logs -f desafio4_service_b
   ```

6. **Rebuild caso altere algum app.py**
   ```bash
   docker compose down -v
   docker compose build --no-cache
   docker compose up -d
   ```
</details>

<details>
  <summary>Desafio 5</summary>

## Microsserviços com API Gateway

* **Objetivo:** Criar uma arquitetura composta por dois microsserviços independentes, acessados através de um API Gateway centralizado. Os três serviços rodam em containers separados, conectados pela mesma rede Docker.

* **Descrição da solução:**  
  A solução utiliza três containers:
  - **service_users:** expõe dados de usuários.
  - **service_orders:** expõe dados de pedidos.
  - **gateway:** ponto único de entrada, responsável por repassar as requisições aos serviços internos.

  Cada serviço é um pequeno app Flask com seu próprio Dockerfile.  
  O `docker-compose.yml` constrói e sobe tudo, gerenciando dependências e expondo apenas o gateway para acesso externo.

* **Funcionamento explicado:**
  1. O Docker sobe os containers `service_users`, `service_orders` e depois o `gateway`.
  2. Os serviços internos são acessados **somente pela rede Docker** (`service_users:5000` e `service_orders:5000`).
  3. O gateway recebe requisições externas nas rotas:
     - `/users` → repassa para `service_users`
     - `/orders` → repassa para `service_orders`
  4. O gateway devolve para o cliente a resposta consolidada.
  5. Assim, o sistema tem um **único ponto de entrada** mesmo com múltiplos serviços internos.

* **Passo a passo para execução:**
  1. Suba a arquitetura completa:
     ```bash
     docker-compose up --build
     ```

  2. Teste o gateway:
     ```bash
     curl http://localhost:8000/users
     curl http://localhost:8000/orders
     ```

  3. Teste os microsserviços diretamente (opcional):
     ```bash
     curl http://localhost:5001/users
     curl http://localhost:5002/orders
     ```

  4. Derrube os containers:
     ```bash
     docker-compose down -v
     ```

  5. Suba novamente:
     ```bash
     docker-compose up
     ```

  6. Teste o gateway de novo:
     ```bash
     curl http://localhost:8000/users
     curl http://localhost:8000/orders
     ```
</details>