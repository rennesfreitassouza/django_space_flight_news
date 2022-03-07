from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from coodesh_app.models import SFNArticles, SFNArticlesLaunches, SFNArticlesEvents
from pytz import UTC
import os
from django.db.utils import IntegrityError


class Command(BaseCommand):
    # Show this when the user types help
    help = "Deletes data from SFNArticlesEvents, SFNArticlesLaunches and SFNArticles."

    def handle(self, *args, **options):

        print("Deleting all data stored in SFNArticlesEvents...")
        SFNArticlesEvents.objects.all().delete()
        print("Deleting all data stored in SFNArticlesLaunches...")
        SFNArticlesLaunches.objects.all().delete()
        print("Deleting all data stored in SFNArticles...")
        SFNArticles.objects.all().delete()

        print("Operations completed!")
