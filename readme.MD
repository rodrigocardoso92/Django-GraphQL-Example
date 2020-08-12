<img alt="Django" src="https://miro.medium.com/max/700/1*jLrvxW83rre-25Nrhk-tww.png" />

# Exemplo de utilização do GraphQL com DJANGO Framework


Este é um simples projeto de utilização do GraphQL com o Django.

Para interagir com o sistema, foram criadas duas entidades, uma de usuario e outra de postagens do usuario

## Entidades
  - Usuario
    - username
    - email
    - bio
    - password

  - Post
    - title
    - content
    - user foreign key

## Iniciando projeto

Antes de iniciar o sistema, execute o seguinte comando para baixar as dependencias utilizadas no projeto:

```
pip install -r requirements.txt
```

Crie uma database com as mesmas configuracoes apresentadas no arquivo <b>.env</b>

Para configurar o banco de dados, execute os seguintes comandos:
```
python manage.py makemigrations
python manage.py migrate
```

Para iniciar o sistema, execute:

```
python manage.py runserver
```

Para interagir com o sistema, acesse o seguinte link:
```
http://127.0.0.1:8000/graphql
```

Em seguida, basta seguir a documentação gerada pelo GraphQL para realizar as Queries e Mutations


# OBS:

POR SER UM PROJETO DE APRESENTACAO, NAO HA PROBLEMAS EM EXPOR O ARQUIVO <b>.env</b> MAS LEMBRE-SE, NUNCA EXPONHA O ARQUIVO EM PROJETOS REAIS!
