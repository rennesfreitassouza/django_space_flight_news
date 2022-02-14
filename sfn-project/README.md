## Django sfn-project 2022

[A primeira solução](http://sfn-project.herokuapp.com/) desenvolvida por mim para o desafio [🏅 2021 - Space Flight News](../README.md).


### Tecnologias utilizadas

- [Linguagem Python](https://www.python.org/)
- [Framework Django](https://docs.djangoproject.com/en/4.0/)
- [Django REST framework](https://www.django-rest-framework.org/)
- Serviços de computação em nuvem: [Heroku](https://heroku.com) e [Amazon EC2](https://aws.amazon.com/ec2/)
- [Heroku Advanced Scheduler](https://devcenter.heroku.com/articles/advanced-scheduler)
- [Heroku Postgres](https://devcenter.heroku.com/categories/heroku-postgres)
- [Spaceflight News API](https://api.spaceflightnewsapi.net/v3/documentation)
- [Postman](https://www.postman.com/)


### Instructions

- Utilizar as mesmas tecnologias ou semelhantes as que foram mencionadas no tópico acima.
- Clonar [este repositório](https://lab.coodesh.com/rennesfrso/space-flight-news-20210823).
- Criar um virtual environment e instalar os seguintes módulos com o comando <code>pip install asgiref certifi charset-normalizer Django django-extensions django-environ django-rest-framework idna pip psycopg2-binary pytz requests setuptools sqlparse tzdata urllib3 wheel gunicorn django-heroku</code>.
- Alterar os nomes dos arquivos <code>.env_example</code> e <code>configEmailAlarm.cfg_example</code>, para <code>.env</code> e <code>configEmailAlarm.cfg</code>.
- Instanciar valores válidos para as variáveis ambiente nesses arquivos renomeados.
- Executar algum dos comandos listados a seguir.

- <strong>Atenção</strong>: executar o interpretador Python para iniciar a REST API com o Django no diretório que os arquivos <code>configEmailAlarm.cfg</code>, <code>ArticlesData.csv</code>, <code>EventsData.csv</code> e <code>LaunchesData.csv</code> estiverem armazenados.

### Useful commands 


- <code>python manage.py runserver</code>
    - Inicializa a API com o Django.<p>
- <code>python manage.py runscript main_psql</code>
    - realiza a requisição de todos os dados retornados pela rota <code>/articles</code> da [API Space Flight News](https://api.spaceflightnewsapi.net/v3/documentation) e armazena eles em arquivos no formato csv. Então, a outra função executada permite que esses arquivos sejam lidos para que os dados deles sejam usados para alimentar o banco de dados na cloud. Caso os dados lidos dos arquivos estejam no banco de dados, eles não são reinseridos nele. Caso exceções ocorram durante a inserção dos dados no banco de dados, cada exceção pode gerar uma notificação. Para isso, é necessário alterar o nome do arquivo <code>configEmailAlarm.cfg_example</code> para <code>configEmailAlarm.cfg</code>. Também é necessário inserir valores no arquivo <code>configEmailAlarm.cfg</code>, como no exemplo abaixo:

```text
[DEFAULT]
USER = username@gmail.com
PASS = 1234
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 465
TIMEOUT = 10.0
RECEIVER_EMAIL = username@gmail.com
```

<code>USER</code> e <code>PASS</code> devem ser credenciais válidas para que o alarme gere uma notificação e ela chegue ao <code>RECEIVER_EMAIL</code>

- <code>request_api_data.py</code>
    - Executa diversas requisições para a rota <code>/articles</code> da API Space Flight, até que todos os dados sejam armazenados em arquivos csv.
- <code>python manage.py load_api_data.py</code> 
    - Armazena todos os registros dos três arquivos csv criados para armazenamento e análise dos dados retornados pela API do projeto Space Flight News em tabelas no banco de dados.
- <code>python manage.py delete_all_models_data</code> 
    - deleta todos os registros do das três tabelas do banco de dados.
- [O arquivo json](/sfn-project/coodesh_app.postman_collection.json) pode ser importado usando o Postman para que os requisitos relativos as rotas para a solução em execução sejam analisados.

### About

>  This is a challenge by [Coodesh](https://coodesh.com/)
