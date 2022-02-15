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


### Instructions [Django project setup]

- Utilizar as mesmas tecnologias ou semelhantes as que foram mencionadas no tópico acima.
- Clonar [este repositório](https://lab.coodesh.com/rennesfrso/space-flight-news-20210823).
- Criar um virtual environment e instalar os seguintes módulos com o comando <code>pip install asgiref certifi charset-normalizer Django django-extensions django-environ django-rest-framework idna pip psycopg2-binary pytz requests setuptools sqlparse tzdata urllib3 wheel gunicorn django-heroku</code>.
- Alterar os nomes dos arquivos <code>sfn-project/sfn/.env_example</code> e <code>sfn-project/configEmailAlarm.cfg_example</code>, para <code>.env</code> e <code>configEmailAlarm.cfg</code>.
- Instanciar valores válidos para as variáveis ambiente nesses arquivos renomeados.

```.env
DEBUG=False 
SECRET_KEY=
HOST=endereço do banco de dados
DATABASE=nome do banco de dados que será acessado
USER=usuário para acesso ao banco de dados
PORT=porta de acesso ao seu baco de dados
PASSWORD=senha para acesso ao seu banco de dados
[ALLOWED_HOSTS=lista de endereços que seu aplicativo web django pode servir
```


```configEmailAlarm.cfg
[DEFAULT]
USER = username@gmail.com
PASS = senhaDOusername@gmail.com
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 465
TIMEOUT = 10.0
RECEIVER_EMAIL = username@gmail.com
```

- Executar algum dos comandos listados a seguir.

- <strong>Atenção</strong>: executar o interpretador Python para iniciar a REST API com o Django no diretório que os arquivos <code>configEmailAlarm.cfg</code>, <code>ArticlesData.csv</code>, <code>EventsData.csv</code> e <code>LaunchesData.csv</code> estiverem armazenados.

### Useful commands 

- <code>python manage.py runserver</code>
    - Inicializa a API com o Django.<p>
- <code>python manage.py runscript main_psql</code>
    - realiza a requisição de todos os dados retornados pela rota <code>/articles</code> da [API Space Flight News](https://api.spaceflightnewsapi.net/v3/documentation) e armazena eles em arquivos no formato csv. Então, uma outra função executada permite que esses arquivos sejam lidos para que os dados deles sejam usados para alimentar o banco de dados na cloud. Caso os mesmos registros retornados pela API Space Flight, na mesma ordem, armazenados nos arquivos csv e lidos destes já estiverem no banco de dados, eles não serão reinseridos no neste. Dessa forma, caso não for identificado que o mesmo registro, na mesma ordem de verificação e com os mesmo valores para todos os campos está no banco de dados, este registro será armazenado pela aplicação Django. Caso exceções ocorram durante a inserção dos dados no banco de dados, cada exceção pode gerar uma notificação. Para isso, é necessário configurar corretamente o arquivo <code>configEmailAlarm.cfg</code>. Também é necessário inserir valores no arquivo <code>configEmailAlarm.cfg</code>, como no exemplo abaixo:
- <code>python request_api_data.py</code>
    - Executa diversas requisições para a rota <code>/articles</code> da API Space Flight, até que todos os dados sejam armazenados em arquivos csv.
- <code>python manage.py load_api_data.py</code> 
    - Armazena todos os registros dos três arquivos csv criados para armazenamento e análise dos dados retornados pela API do projeto Space Flight News em tabelas no banco de dados.
- <code>python manage.py delete_all_models_data</code> 
    - deleta todos os registros das três tabelas criadas pelo framework Django do banco de dados.
- [O arquivo json](/sfn-project/coodesh_app.postman_collection.json) pode ser importado usando o Postman para que os requisitos relativos as rotas para a solução em execução sejam analisados.

### About the endpoints

`[GET]/`<p>

`[GET]/articles/` - aceita requisições GET que contenham um HTTP Body Content com um JSON no formato {"page": 6}. Os objetos obtidos do banco de dados foram divididos em partes com até 10 itens cada, para não sobrecarregar a requisição.

`[POST]/articles/` adiciona um novo artigo. O formato dos dados envio dos dados pode uma requisição HTTP POST sem Body Content ou com um Body Content no seguinte formato:
{
    "api_id": 0,
    "title": "EMPTY",
    "url": "EMPTY",
    "imageUrl": "EMPTY",
    "newsSite": "EMPTY",
    "summary": "EMPTY",
    "updatedAt": "2022-02-13T13:34:02",
    "publishedAt": "2022-02-13T13:34:02",
    "featured": true,
	"event_id": "EMPTY",
    "event_provider": "EMPTY",
    "launche_id": "EMPTY",
	"launche_provider": "EMPTY",
	"article_launche_id": "EMPTY",
	"provider": "EMPTY"
}

`[GET]/articles/:id/` retorna um JSON com os dados atuais do registro de um article com a chave primária igual ao id na url, ou um JSON com uma mensagem de erro.
`[PUT]/articles/:id/` Atualiza um article baseado no id da requisição e retorna os dados já atualizados, ou retorna um JSON informando que o registro não existe.
`[DELETE]/articles/:id/` remove um article baseado no id do endereço da requisição HTTP DELETE e retorna a representação para impressão daquele article. Caso o id não retorne nenhum objeto, uma string de erro é retornada.

### About

>  This is a challenge by [Coodesh](https://coodesh.com/)
