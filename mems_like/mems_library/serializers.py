from rest_framework import serializers

from .models import Mem


class MemSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Мемов. """

    class Meta:
        model = Mem
        fields = (
            'mem_id', 'text', 'pub_date', 'image', 'post_author', 'likes_count'
        )
