# Generated by Django 4.1.5 on 2023-03-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mems_library', '0002_alter_mem_post_author_alter_mem_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mem',
            name='mem_id',
            field=models.CharField(error_messages={'unique': 'Мем с таким id уже создан.'}, max_length=200, unique=True),
        ),
    ]
