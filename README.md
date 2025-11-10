# fccpd
Projeto da cadeira de Fundamentos de Computação Concorrente, Paralela e Distribuída

👤 André Castro - andre20072006@gmail.com

<details>
  <summary>Desafio 1</summary>

## Containers em Rede

### Objetivo
Criar dois containers que se comunicam usando uma rede Docker customizada criada pelo docker-compose.

### Descrição da solução
Um container roda um servidor Flask simples expondo `/`.  
Outro container roda um script que faz `curl` periódico para o servidor.  
Ambos ficam na mesma rede nomeada (`desafio_net`), garantindo resolução DNS automática (`server` → IP do container).

### Funcionamento explicado
- O `server` sobe um Flask escutando em `0.0.0.0:8080`.  
- O `client` usa `curl http://server:8080/` em loop.  
- Como os dois containers estão na mesma rede, o hostname `server` funciona sem configurar IP.  
- Os logs mostram requisições com timestamps.

### Passo a passo para execução
1. Subir ambiente:
   ```bash
   ./run.sh
   ```
2. Ver containers:
   ```bash
   docker ps
   ```
3. Ver rede criada:   
  ```bash
  docker network ls | grep desafio_net
  ```
4. Acompanhar logs:
  * Server:
    ```bash
    docker logs -f desafio_server
    ```
  * Client:
    ```bash
    docker logs -f desafio_client
    ```
5. Limpeza:
  ```bash
  ./stop_clean.sh
  ```
</details>


<details>
  <summary>Desafio 2</summary>
  
## Volumes e persistência
* **Objetivo:** Demonstrar que os dados continuam existindo mesmo após a remoção do container, usando volumes Docker para armazenar o banco fora do container.

* **Descrição da solução:**  
  A solução usa um container PostgreSQL com um volume nomeado. Um script `init.sql` cria uma tabela e insere um registro inicial. O diretório interno onde o PostgreSQL guarda os dados (`/var/lib/postgresql/data`) é montado em um volume Docker, garantindo que a remoção do container não apague o conteúdo. Ao recriar o container, os dados são carregados a partir do volume.

* **Funcionamento explicado:**  
  1. O PostgreSQL sobe pela primeira vez.  
  2. O `init.sql` cria a tabela e insere o primeiro registro.  
  3. Os dados ficam armazenados no volume `desafio2_data`.  
  4. O container é destruído com `docker compose down`, mas o volume permanece.  
  5. Ao subir novamente (`docker compose up -d`), o PostgreSQL carrega tudo do volume.  
  6. A consulta mostra que os registros continuam lá — provando a persistência.

* **Passo a passo para execução:**
  1. Suba o container:
     ```bash
     docker compose up -d
     ```
  2. Verifique o registro inicial no banco:
     ```bash
     docker exec -it desafio2_db psql -U user -d teste -c "SELECT * FROM registros;"
     ```
  3. Derrube o container:
     ```bash
     docker compose down
     ```
  4. Confirme que o volume ainda existe:
     ```bash
     docker volume ls | grep desafio2_data
     ```
  5. Suba novamente:
     ```bash
     docker compose up -d
     ```
  6. Consulte outra vez para confirmar a persistência:
     ```bash
     docker exec -it desafio2_db psql -U user -d teste -c "SELECT * FROM registros;"
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
* Objetivo: Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços.
* Descrição da solução:
* Funcionamento explicado: 
* Passo a passo para execução:
</details>