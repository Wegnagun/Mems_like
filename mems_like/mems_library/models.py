from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from django.db import models


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
    image_url = models.URLField(
        max_length=300,
    )
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
    likes_count = models.IntegerField(
        verbose_name='Количество лайков'
    )

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}.png", File(img_temp))
        super(Mem, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'

    def __str__(self):
        return self.text
