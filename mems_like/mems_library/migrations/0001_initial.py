# Generated by Django 4.1.5 on 2023-03-05 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem_id', models.IntegerField(error_messages={'unique': 'Мем с таким id уже создан.'}, unique=True)),
                ('text', models.CharField(error_messages={'unique': 'Мем с таким описанием уже создан.'}, max_length=200, unique=True, verbose_name='Текст мема')),
                ('image_url', models.URLField()),
                ('image', models.ImageField(upload_to='mems/images', verbose_name='Мем')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации')),
                ('post_author', models.TextField(verbose_name='Автор мема')),
                ('likes_count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Мем',
                'verbose_name_plural': 'Мемы',
                'ordering': ('-pub_date',),
            },
        ),
    ]
