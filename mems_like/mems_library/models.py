from django.db import models
from urllib import request
import os
from django.core.files import File


class Mem(models.Model):
    """ Модель мемов. """

    mem_id = models.IntegerField(
        unique=True,
        error_messages={
            'unique': "Мем с таким id уже создан."
        },
    )
    text = models.TextField(
        verbose_name='Текст мема',
        unique=True,
        error_messages={
            'unique': "Мем с таким описанием уже создан."
        }
    )
    image_url = models.URLField()
    image = models.ImageField(
        verbose_name='Мем',
        upload_to='mems/images'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации'
    )
    post_author = models.CharField(
        max_length=200,
        verbose_name='Автор мема'
    )
    likes_count = models.IntegerField()

    def get_remote_image(self):
        if self.image_url and not self.image:
            result = request.urlretrieve(self.image_url)
            self.image.save(
                os.path.basename(self.image_url),
                File(open(result[0], 'rb'))
            )
            self.save()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'

    def __str__(self):
        return self.text
