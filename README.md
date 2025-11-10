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
* Objetivo: Usar Docker Compose para orquestrar múltiplos serviços dependentes.
* Descrição da solução:
* Funcionamento explicado: 
* Passo a passo para execução:
</details>

<details>
  <summary>Desafio 4</summary>
  
## Microsserviços Independentes
* Objetivo: Criar dois microsserviços independentes que se comunicam via HTTP.
* Descrição da solução:
* Funcionamento explicado: 
* Passo a passo para execução:
</details>

<details>
  <summary>Desafio 5</summary>
  
## Microsserviços com API Gateway
* Objetivo: Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços.
* Descrição da solução:
* Funcionamento explicado: 
* Passo a passo para execução:
</details>