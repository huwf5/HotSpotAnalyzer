import logging

from django.core.management.base import BaseCommand

from application import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    import command: python manage.py import [json_file]
    import data to database
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Path to the JSON file containing the data"
        )

    def handle(self, *args, **options):
        json_file = options["json_file"]
        if not json_file:
            self.stdout.write(
                self.style.ERROR("Please provide the path to the JSON file")
            )
            return

        try:
            from apps.user.fixtures.import_message import Import
            importer = Import(json_file=json_file)
            importer.run()
        except Exception as e:
            print(e)
        print("import completed!")

