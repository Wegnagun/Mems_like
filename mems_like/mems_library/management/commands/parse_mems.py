import os
import requests
import datetime
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()

GROUP_ID = -45045130
POSTS_COUNT = 25
API_VERSION = 5.81
ACCESS_TOKEN = os.environ.get('VK_TOKEN', 'enter you VK Token')
POSTS = 20


class Command(BaseCommand):
    help = 'Загрузите все мемы в вашу базу (используя API ВКонтакте).'

    def handle(self, *args, **options):
        """ Получаем данные с ВК и добавляем POSTS постов в базу """
        """ # image type = y заметка для поиска изображения в респонсе) """
        params = {
            'access_token': ACCESS_TOKEN,
            'owner_id': GROUP_ID,
            'count': POSTS_COUNT,
            'v': API_VERSION,
            'offset': 0
        }
        try:
            api_response = requests.get(
                'https://api.vk.com/method/wall.get', params=params
            ).json()
        except Exception as error:
            message = {'error': error,
                       'message': 'params данные'}
            return message
        else:
            count = 0
            for i in api_response.get("response").get('items'):
                if (
                    i.get("attachments")[0].get('type') != "link"
                    and count != POSTS
                ):
                    id = i.get('id')
                    text = i.get('text')
                    pub_date = i.get('date')
                    normal_date = datetime.datetime.fromtimestamp(pub_date)
                    post_author = (
                        'Админ группы'
                        if i.get('from_id') == GROUP_ID
                        else i.get('from_id')
                    )
                    likes_count = i.get('likes').get('count')
                    count += 1
                    print(
                        f"{count}. Пост с id {id}:\n    "
                        f"Заголовок: {text}\n    "
                        f"Дата и время публикации:  "
                        f"{normal_date:%Y-%m-%d %H:%M:%S}\n    "
                        f"Автор поста: {post_author}\n    "
                        f"Налукасили: {likes_count}\n"
                        f"'==============================================='"
                    )


