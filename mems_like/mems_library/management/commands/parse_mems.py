import datetime
import json
import os

import requests
from django.core import files
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from mems_library.models import Mem

load_dotenv()

GROUP_ID = -45045130
POSTS_COUNT = 4
API_VERSION = 5.81
ACCESS_TOKEN = os.environ.get('VK_TOKEN', 'enter you VK Token')
POSTS = 4


def show_data(
    mem_id: int, count: int, text: str, pub_date,
    post_author: int, likes_count: int, image_url: str
) -> str:
    return (
        f"{count}. Пост с id {mem_id}:\n    "
        f"Заголовок: {text}\n    "
        f"Дата и время публикации:  "
        f"{pub_date:%Y-%m-%d %H:%M:%S}\n    "
        f"Автор поста: {post_author}\n    "
        f"Ссылка на изображение: {image_url}\n    "
        f"Налукасили: {likes_count}\n"
        f"'=============================================='"
    )


def download_img(image_url, mem_id):
    image_name = f'{mem_id}.png'
    response = requests.get(image_url, stream=True)
    image_temp_file = NamedTemporaryFile(delete=False)
    for chunk in response.iter_content(1024 * 8):
        if not chunk:
            break
        image_temp_file.write(chunk)
    image_temp_file.flush()
    temp_file = files.File(image_temp_file, name=image_name)
    return temp_file


class Command(BaseCommand):
    """ Команда парсинга мемов и сохранения в бд. """
    help = 'Загрузите все мемы в вашу базу (используя API ВКонтакте).'

    def handle(self, *args, **options):
        """ Получаем данные с ВК и добавляем посты в базу """
        params = {
            'access_token': ACCESS_TOKEN,
            'owner_id': GROUP_ID,
            'count': POSTS_COUNT,
            'v': API_VERSION,
            'offset': 6
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
            data = []
            for i in api_response.get("response").get('items'):
                temp_data = {
                    'mem_id': 0, 'text': '', 'pub_date': '', 'image_url': '',
                    'post_author': '', 'likes_count': 0
                }
                if (
                    i.get("attachments")[0].get('type') != "link"
                    and count != POSTS
                    and i.get("attachments")[0].get('type') != "video"
                ):
                    temp_data['mem_id'] = i.get('id')
                    temp_data['text'] = i.get('text')
                    temp_data['pub_date'] = datetime.datetime.fromtimestamp(
                        i.get('date')
                    )
                    temp_data['post_author'] = (
                        'Админ группы'
                        if i.get('from_id') == GROUP_ID
                        else i.get('from_id')
                    )
                    temp_data['likes_count'] = i.get('likes').get('count')
                    image_url = [
                        item.get('url') for item in
                        i.get('attachments')[0].get('photo').get('sizes')
                        if item.get('type') == 'r'
                    ][0]
                    temp_data['image_url'] = image_url
                    count += 1
                    data.append(temp_data)
                    print(show_data(**temp_data, count=count))

            if options['r']:
                with open(
                    f'data/mems.json', 'w', encoding="utf-8"
                ) as file:
                    json.dump(data, file, default=str, ensure_ascii=False)
                    self.stdout.write(self.style.SUCCESS(
                        'Данные успешно записаны в mems.json'))
                    file.close()
                    try:
                        file = open('data/mems.json',
                                    'r', encoding='utf-8')
                    except IOError:
                        self.stdout.write(self.style.ERROR(
                            'Не удалось открыть файл!'))
                    else:
                        with file:
                            reader = json.load(file)
                            Mem.objects.bulk_create(
                                Mem(**data) for data in reader)
                            self.stdout.write(self.style.SUCCESS(
                                f'Модель Mem обновлена!'))

    def add_arguments(self, parser):
        parser.add_argument(
            '-r',
            const='mems.json',
            nargs='?',
            type=str,
            help='загрузить mems.json в базу'
        )
