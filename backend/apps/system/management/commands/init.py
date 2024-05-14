import logging

from django.core.management.base import BaseCommand

from application import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    startup command: python manage.py init
    """

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:

            try:
                exec(
                    f"""
from {app}.fixtures.initialize import Initialize
Initialize(app="{app}").run()
                """
                )
            except ModuleNotFoundError:
                pass
        print("Initialization completed!")
