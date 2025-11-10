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
   ./run.sh
2. Ver containers:
   docker ps
3. Ver rede criada:   
  docker network ls | grep desafio_net
4. Acompanhar logs:
  * Server: docker logs -f desafio_server
  * Client: docker logs -f desafio_client
5. Limpeza:
  ./stop_clean.sh
</details>


<details>
  <summary>Desafio 2</summary>
  
## Volumes e persistência
* Objetivo: Demonstrar persistência de dados usando volumes Docker.
* Descrição da solução:
* Funcionamento explicado: 
* Passo a passo para execução:
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
