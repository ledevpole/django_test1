# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
from titre_wiki.models import Title
import wikipedia
import random
import logging
from pprint import pprint

# Get an instance of a logger
logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates titles """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete Title instances")
    Title.objects.using('db_titre_wiki').all().delete()


def create_title():
    """Creates an title object using api from wikipedia"""
    logger.info("Creating titles")

    """ Here call the  api"""
    wikipedia.set_lang("fr")
    w = wikipedia.random(10)
    pprint(w)
    length = len(w)
    for i in range(length):
        title = Title(
            title_wiki=w[i],
            article_id=0,
        )
        title.save(using='db_titre_wiki')
    return title


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 100 titles
    for i in range(10):
        create_title()

