from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


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
    image = models.ImageField(
        verbose_name='Мем',
        upload_to='mems/images'
    )
    image_url = models.URLField()
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
            img_temp = NamedTemporaryFile()
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}.png", File(img_temp))
        self.save()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'

    def __str__(self):
        return self.text
