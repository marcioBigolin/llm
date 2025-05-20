## Modelo reduzido de LLM 

Serviço que utiliza Language Large Models (LLM) para interpretar perguntas e gerar informações a partir dos dados do Integra.
Para entender o desenvolvimento veja a estrutura do projeto [aqui](docs/estrutura_de_arquivos.md).

## Para rodar a aplicação 
Basta digitar 
```
docker compose up 
```

Acesse via http://localhost a app web roda na porta 80 mesmo

## Documentação técnica

Requisitos do ambiente de dev (se não for usar o docker) é:
- ter instalado o Python3 e o pip

Para baixar as dependências desse serviço, execute o comando abaixo no diretório do módulo pela primeira vez:

```
pip install -r requirements.txt
```

Após para iniciar o serviço basta utilizar 

```
python3 service.py
```

## Banco de dados vetorial

# Variáveis de ambiente

As variáveis de ambiente são definidas no arquivo `.env` ou passadas no docker. Aqui estão as variáveis que você precisa configurar estão relatadas acima.

Por favor, substitua os valores acima pelos seus próprios valores de configuração.

