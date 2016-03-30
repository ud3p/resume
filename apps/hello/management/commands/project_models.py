from django.core.management.base import BaseCommand
from django.db.models import get_models

class Command(BaseCommand):
    help = 'This command prints all project models and the count of objects in every model'

    def handle(self, *args, **options):

        models_list = []
        for model in get_models():
            models_list.append('[{0}] - {1} objects'.format(model.__name__,
                                                            model._default_manager.count()))

        map(self.stdout.write, models_list)
        models_error_list = ['error: ' + model for model in models_list]
        map(self.stderr.write, models_error_list)

