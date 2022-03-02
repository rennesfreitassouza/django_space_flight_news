## Django sfn-project 2022

[A 2a. solução](http://sfn-project.herokuapp.com/) desenvolvida por mim para o desafio [🏅 2021 - Space Flight News](../README.md).


### Tecnologias utilizadas

- [Linguagem Python](https://www.python.org/)
- [Framework Django](https://docs.djangoproject.com/en/4.0/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter-pypackage) para reestruturar o projeto Django. [Sobre](https://www.youtube.com/watch?v=RVLzZc3GUrk) esse módulo.
- Serviços de computação em nuvem: [Heroku](https://heroku.com) e [Amazon EC2](https://aws.amazon.com/ec2/)
- [Heroku Advanced Scheduler](https://devcenter.heroku.com/articles/advanced-scheduler)
- [Heroku Postgres](https://devcenter.heroku.com/categories/heroku-postgres)
- [Spaceflight News API](https://api.spaceflightnewsapi.net/v3/documentation)
- [Postman](https://www.postman.com/)


### Instructions [Django project setup]

- Utilizar as mesmas tecnologias ou semelhantes as que foram mencionadas no tópico acima.
- Clonar [este repositório](https://lab.coodesh.com/rennesfrso/space-flight-news-20210823).
- Criar um virtual environment e instalar os seguintes módulos com o comando <code>pip install -r sfn-project/requirements.txt</code>.
- Alterar os nomes dos arquivos <code>sfn-project/.envs/.local/.django_example</code> e <code>sfn-project/configEmailAlarm.cfg_example</code>, para <code>.django</code> e <code>configEmailAlarm.cfg</code>.
- Instanciar valores válidos para as variáveis ambiente nesses arquivos renomeados.

```.django
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
DATABASE_URL= URI do banco de dados
ALLOWED_HOSTS=lista de endereços que seu aplicativo web django pode servir

HOST=endereço do banco de dados [sfn-project.config.settings.local]
DATABASE=nome do banco de dados que será acessado [sfn-project.config.settings.local]
USER=usuário para acesso ao banco de dados [sfn-project.config.settings.local]
PORT=porta de acesso ao baco de dados [sfn-project.config.settings.local]
PASSWORD=senha para acesso ao banco de dados[sfn-project.config.settings.local]
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
    - realiza a requisição de todos os dados retornados pela rota <code>/articles</code> da [API Space Flight News](https://api.spaceflightnewsapi.net/v3/documentation) e armazena eles em arquivos no formato csv. Então, uma outra função executada permite que esses arquivos sejam lidos para que os dados deles sejam usados para alimentar o banco de dados. Caso os mesmos registros retornados pela API Space Flight, na mesma ordem, armazenados nos arquivos csv e lidos destes já estiverem no banco de dados, eles não serão reinseridos no neste. Dessa forma, caso não for identificado que o mesmo registro, na mesma ordem de verificação e com os mesmo valores para todos os campos está no banco de dados, este registro será armazenado pela aplicação Django. Caso exceções ocorram durante a inserção dos dados no banco de dados, cada exceção pode gerar uma notificação. Para isso, é necessário configurar corretamente o arquivo <code>configEmailAlarm.cfg</code>. Também é necessário inserir valores no arquivo <code>configEmailAlarm.cfg</code>.
- <code>python request_api_data.py</code>
    - Executa diversas requisições para a rota <code>/articles</code> da API Space Flight, até que todos os dados sejam armazenados em arquivos csv.
- <code>python manage.py load_api_data.py</code> 
    - Armazena todos os registros dos três arquivos csv criados para armazenamento e análise dos dados retornados pela API do projeto Space Flight News em tabelas no banco de dados.
- <code>python manage.py delete_all_models_data</code> 
    - deleta todos os registros das três tabelas criadas pelo framework Django do banco de dados.
- [O arquivo json](/sfn-project/coodesh_app.postman_collection.json) pode ser importado usando o Postman para que os requisitos relativos as rotas para a solução em execução sejam analisados.

### About the endpoints

`[POST]api/token/` - retorna um JSON com dois campos. Um dos campos é um token refresh e o outro é um token de acesso. O token de acesso é uma string com valor codificado em Base64. Este valor correspondente a um token assinado que permite que uma tentativa de atenticação do tipo 'Bearer Token', com o valor retornado no JSON seja realizada com sucesso.

`[POST]api/token/refresh/` - quando o token do campo access retornado pela rota <code>api/token/</code> da aplicação expirar, esta rota retorna um novo token de acesso caso o token refresh da mesma rota <code>api/token/</code> for enviado em uma requisição para esta rota.

`[GET]/articles/` - aceita requisições GET que contenham um HTTP Body Content com um JSON no formato <code>{"page": 6}</code>. Os objetos obtidos do banco de dados foram divididos em partes com até 10 itens cada, para não sobrecarregar a requisição.

`[GET]/test_articles/` - Lista o conteúdo do banco de dados. Lê o conteúdo de um JSON no formato <code>{"limit": 50, "my_offset": 30}</code>. Sobre o conteúdo do Body Content da requisição :<code>sfn-project.coodesh_app.api_views.SFNArticlesPagination</code>.

`[POST]/articles/` adiciona um novo artigo. O formato dos dados envio dos dados pode ser uma requisição HTTP POST sem Body Content ou com um Body Content no seguinte formato:
```
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
```

`[POST]/test_articles/` adiciona um novo artigo. O formato dos dados envio dos dados deve ser uma requisição HTTP POST um Body Content no seguinte formato:
```
{
    "api_id": 222,
    "title": "This field is required.",
    "url": "This field is required.",
    "imageUrl": "This field is required.",
    "newsSite": "This field is required.",
    "summary": "This field is required.",
    "updatedAt": "2021-02-13T13:34:02",
    "publishedAt": "2021-02-13T13:34:02",
    "featured": true,
    "article_launche_id": "test launche", [OPTIONAL]
    "article_launche_id_provider": "teste Provider" [OPTIONAL]
}
```

`[GET]/articles/:id/` retorna um JSON com os dados atuais do registro de um article com a chave primária igual ao id na url, ou um JSON com uma mensagem de erro.

`[GET]/test_articles/:id/` retorna um JSON com os dados atuais do registro de um article com a chave primária igual ao id na url, ou um JSON com uma mensagem de erro.

`[PUT]/articles/:id/` Atualiza um article baseado no id da requisição e retorna os dados já atualizados, ou retorna um JSON informando que o registro não existe.

`[PUT]/test_articles/:id/` Atualiza um article baseado no id da requisição. Uma nova requisição [GET] deve ser realizada para que os os dados atualizados do registro sejam retornados. Todos os dados do registro devem ser enviados na requisição.

`[DELETE]/articles/:id/` remove um article baseado no id do endereço da requisição HTTP DELETE e retorna a representação para impressão daquele article. Caso o id não retorne nenhum objeto, uma string de erro é retornada.

`[DELETE]/test_articles/:id/` remove um article baseado no id do endereço da requisição HTTP DELETE e retorna uma resposta HTTP sem conteúdo e com status code 204. Também retorna um JSON, em caso de erro.


### About

>  This is a challenge by [Coodesh](https://coodesh.com/)
