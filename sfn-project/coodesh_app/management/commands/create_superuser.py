from django.core.management import BaseCommand
from django.contrib.auth.models import User
from coodesh_app.src.exceptions import UnknownExceptionNotify


class Command(BaseCommand):
    # Show this when the user types help
    help = "Creates a new superuser."

    def handle(self, *args, **options):
        try:
            User.objects.create_superuser('admin', 'email@email.com', 'admin')
        except Exception as e:
            raise UnknownExceptionNotify(__file__, e.args, notify=True)
        print("Operation completed!")
