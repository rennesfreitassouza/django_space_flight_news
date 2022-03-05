from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from coodesh_app.models import SFNArticles, SFNArticlesLaunches, SFNArticlesEvents
from pytz import UTC
import os
from coodesh_app.src import notification
import configparser


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def notify(message_body):
    parser = configparser.ConfigParser()
    parser.read("configEmailAlarm.cfg")
    receiver_email = parser['DEFAULT'].get('RECEIVER_EMAIL')
    notification.main(receiver_email=receiver_email,
                      subject_line='[Notificação] Falha banco de dados sfn-project', message_body=message_body)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from ArticlesData.csv, LaunchesData.csv and EventsData.csv into database."

    def handle(self, *args, **options):

        print("Loading data for tables [It does not update them]...")
        print("Current working directory: ", os.getcwd())
        with open('ArticlesData.csv', encoding='utf-8') as csv_articles:
            for row in DictReader(csv_articles):

                articles = SFNArticles.objects.filter(my_id=row['my_id'], api_id=row['api_id'], title=row['title'],
                                                      url=row['url'], imageUrl=row['imageUrl'], newsSite=row['newsSite'], summary=row['summary'])

                if not articles.exists():
                    article = SFNArticles()
                    article.my_id = row['my_id']
                    article.api_id = row['api_id']
                    article.title = row['title']
                    article.url = row['url']
                    article.imageUrl = row['imageUrl']
                    article.newsSite = row['newsSite']
                    article.summary = row['summary']

                    raw_publishedAt = row['publishedAt']
                    article.publishedAt = UTC.localize(
                        datetime.strptime(raw_publishedAt[:-5], DATETIME_FORMAT))

                    raw_updatedAt = row['updatedAt']
                    article.updatedAt = UTC.localize(
                        datetime.strptime(raw_updatedAt[:-5], DATETIME_FORMAT))
                    article.featured = row['featured']
                    article.save()

                if row['launches'] == "NOT_EMPTY":
                    with open('LaunchesData.csv', encoding='utf-8') as articlesLaunches:
                        for launches_row in DictReader(articlesLaunches):
                            if launches_row['article_my_id'] == row['my_id']:
                                try:
                                    db_article = SFNArticles.objects.get(
                                        my_id=launches_row['article_my_id'])
                                except SFNArticles.DoesNotExist as e:
                                    print(f'{e}')
                                else:
                                    article_launche = SFNArticlesLaunches()

                                    article_launche.article_launche_id = launches_row['launche_id']
                                    article_launche.provider = launches_row['provider']

                                    article_launche.sfnarticles = db_article
                                    try:
                                        article_launche.save()
                                    except Exception as e:
                                        print(
                                            f"SFNArticlesLaunches save() error {e}")
                                        notify(
                                            f"SFNArticlesLaunches().save() exception: {e}. Record not saved.")

                if row['events'] == "NOT_EMPTY":
                    with open('EventsData.csv', encoding='utf-8') as articlesLaunches:
                        for launches_row in DictReader(articlesLaunches):
                            if launches_row['article_my_id'] == row['my_id']:
                                try:
                                    db_article = SFNArticles.objects.get(
                                        my_id=launches_row['article_my_id'])
                                except SFNArticles.DoesNotExist as e:
                                    print(f'{e}')
                                else:
                                    article_event = SFNArticlesEvents()

                                    article_event.article_event_id = launches_row['event_id']
                                    article_event.provider = launches_row['provider']
                                    article_event.sfnarticles = db_article
                                    try:
                                        article_event.save()
                                    except Exception as e:
                                        print(
                                            f"SFNArticlesEvents save() error: {e}")
                                        notify(
                                            f"SFNArticlesEvents().save() exception: {e}. Record not saved.")

        print("Load complete!")
