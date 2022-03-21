from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from coodesh_app.models import SFNArticles, SFNArticlesLaunches, SFNArticlesEvents
from pytz import UTC
import os
from coodesh_app.src.exceptions import UnknownExceptionNotify, SFNArticlesDoesNotExistNotify
from request_api_data import str_articlesdata_csv, str_launchesdata_csv, str_eventsdata_csv
import traceback


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class Command(BaseCommand):


    # Show this when the user types help
    help = f"Loads data from {str_articlesdata_csv}, {str_launchesdata_csv} and {str_eventsdata_csv} into database."

    def handle(self, *args, **options):

        print("Loading data for tables [It does not update them]...")
        print("Current working directory: ", os.getcwd())

        with open(str_articlesdata_csv, encoding='utf-8') as csv_articles:
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
                    
                    try:
                        article.save()
                    except Exception as e:
                        raise UnknownExceptionNotify(__file__, e.args, traceback.format_exc(), notify=True)
        print(f"{str_articlesdata_csv} data loaded!")
        with open(str_articlesdata_csv, encoding='utf-8') as csv_articles:
            for row in DictReader(csv_articles):
                if row['launches'] == "NOT_EMPTY":
                    with open(str_launchesdata_csv, encoding='utf-8') as articlesLaunches:
                        for launches_row in DictReader(articlesLaunches):
                            if launches_row['article_my_id'] == row['my_id']:
                                try:
                                    db_article = SFNArticles.objects.get(
                                        my_id=launches_row['article_my_id'])
                                except SFNArticles.DoesNotExist as e:
                                    raise SFNArticlesDoesNotExistNotify(__file__, e.args, traceback.format_exc(), notify=True)
                                else:
                                    article_launche = SFNArticlesLaunches()

                                    article_launche.article_launche_id = launches_row['launche_id']
                                    article_launche.provider = launches_row['provider']

                                    article_launche.sfnarticles = db_article
                                    try:
                                        article_launche.save()
                                    except Exception as e:
                                        raise UnknownExceptionNotify(__file__, e.args, notify=True)
        print(f"{str_launchesdata_csv} data loaded!")
        with open(str_articlesdata_csv, encoding='utf-8') as csv_articles:
            for row in DictReader(csv_articles):
                if row['events'] == "NOT_EMPTY":
                    with open(str_eventsdata_csv, encoding='utf-8') as articlesLaunches:
                        for launches_row in DictReader(articlesLaunches):
                            if launches_row['article_my_id'] == row['my_id']:
                                try:
                                    db_article = SFNArticles.objects.get(
                                        my_id=launches_row['article_my_id'])
                                except SFNArticles.DoesNotExist as e:
                                    raise SFNArticlesDoesNotExistNotify(__file__, e.args, traceback.format_exc(), notify=True)
                                else:
                                    article_event = SFNArticlesEvents()

                                    article_event.article_event_id = launches_row['event_id']
                                    article_event.provider = launches_row['provider']
                                    article_event.sfnarticles = db_article
                                    try:
                                        article_event.save()
                                    except Exception as e:
                                        raise UnknownExceptionNotify(__file__, e.args, traceback.format_exc(),notify=True)
        print(f"{str_eventsdata_csv} data loaded!")
        print("Data load complete!")
