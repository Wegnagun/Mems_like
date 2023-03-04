import requests
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()

GROUP_ID = -45045130
POSTS_COUNT = 20
API_VERSION = 5.81


class Command(BaseCommand):
    help = 'Загрузите все мемы в вашу базу (используя API ВКонтакте).'

    def handle(self, *args, **options):
        params = {
            'owner_id': GROUP_ID,
            'count': POSTS_COUNT,
            'v': API_VERSION
        }
        api_response = requests.get(
            'https://api.vk.com/method/wall.get', params=params
        )
        print(api_response)
