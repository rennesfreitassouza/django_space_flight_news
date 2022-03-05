from coodesh_app.models import SFNArticles, SFNArticlesLaunches, SFNArticlesEvents
from coodesh_app.management.commands.load_api_data import DATETIME_FORMAT
from datetime import datetime
from pytz import UTC
from coodesh_app.serializers import SFNArticlesSerializer


def create_new_article(data):

    article = SFNArticles()
    article.api_id = data.get('api_id', 0)
    article.title = data.get('title', 'EMPTY')
    article.url = data.get('url', 'EMPTY')
    article.imageUrl = data.get('imageUrl', 'EMPTY')
    article.newsSite = data.get('newsSite', 'EMPTY')
    article.summary = data.get('summary', 'EMPTY')

    raw_publishedAt = {'publishedAt': data.get(
        'publishedAt', datetime.today().strftime(DATETIME_FORMAT))}
    article.publishedAt = UTC.localize(
        datetime.strptime(raw_publishedAt.get('publishedAt'), DATETIME_FORMAT))

    raw_updatedAt = {'updatedAt': data.get(
        'updatedAt', datetime.today().strftime(DATETIME_FORMAT))}

    article.updatedAt = UTC.localize(
        datetime.strptime(raw_updatedAt.get('updatedAt'), DATETIME_FORMAT))
    article.featured = data.get('featured', True)
    retorno = article.set_article_data_pk_0(article)
    if 'my_id' in retorno.keys():
        try:
            new_record = SFNArticles.objects.get(my_id=retorno['my_id'])
        except:
            response = {'ERROR': 'ERROR TO GET RECORD'}
        else:
            create_new_launche(new_record, data)
            create_new_event(new_record, data)
            response = SFNArticlesSerializer().format_article_data(new_record)
    return response


def create_new_launche(db_article, data):
    article_launche = SFNArticlesLaunches()

    article_launche.article_launche_id = data.get('launche_id', 'EMPTY')
    article_launche.provider = data.get('launche_provider', 'EMPTY')

    article_launche.sfnarticles = db_article
    try:
        article_launche.save()
    except Exception as e:
        print(
            f"SFNArticlesLaunches save() error {e}")


def create_new_event(db_article, data):
    article_event = SFNArticlesEvents()

    article_event.article_event_id = data.get('event_id', 'EMPTY')
    article_event.provider = data.get('event_provider', 'EMPTY')
    article_event.sfnarticles = db_article
    try:
        article_event.save()
    except Exception as e:
        print(
            f"SFNArticlesEvents save() error: {e}")
