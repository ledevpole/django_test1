# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
from titre_wiki.models import Title
from article_wiki.models import Article
import wikipedia
import time
import logging
from pprint import pprint

# Get an instance of a logger
logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates titles """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

""" Populate one article every minute"""
MODE_POPULATE_ARTICLES = 'populate'

MODE_FAST_ARTICLES = 'fastpopulate'

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
    Article.objects.using('db_article_wiki').all().delete()


def create_titles():
    """Creates titles objects using api from wikipedia"""
    logger.info("Creating titles")

    """ Here call the  api"""
    wikipedia.set_lang("fr")
    w = wikipedia.random(10)
    pprint(w)
    length = len(w)
    for i in range(length):
        title = Title(
            title_wiki =w [i],
            article_id = 0,
        )
        title.save(using = 'db_titre_wiki')

def create_articles(delayed = True):
    """populate articles in database"""
    titles = Title.objects.using('db_titre_wiki').all()
    pprint(titles)
    length = len(titles)
    wikipedia.set_lang("fr")
    for i in range(length):
        try:
            w = wikipedia.page(titles[i].title_wiki)
            article = Article(
                article_content = w.content,
                title_id = titles[i].id,
            )
        except wikipedia.exceptions.DisambiguationError as e:
            article = Article(
                article_content = '\n'.join(e.options),
                title_id = titles[i].id,
            )
        except wikipedia.exceptions.PageError as e:
            article = Article(
                article_content = 'didn\'t match any page...',
                title_id = titles[i].id,
            )

        article.save(using = 'db_article_wiki')
        titles[i].article_id = article.id
        titles[i].save(using = 'db_titre_wiki')
        pprint(titles[i])
        pprint(article)
        if(delayed):
            time.sleep(60)

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear / populate
    :return:
    """
    if mode == MODE_CLEAR:
        # Clear data from tables
        clear_data()
        return

    if mode == MODE_REFRESH:
        clear_data()
        # Creating 100 titles
        for i in range(10):
            create_titles()
        return

    if mode == MODE_POPULATE_ARTICLES:
        create_articles()
        return
    if mode == MODE_FAST_ARTICLES:
        create_articles(False)
        return
