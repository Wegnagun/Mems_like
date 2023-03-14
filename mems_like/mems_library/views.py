from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Mem
from .serializers import MemSerializer


class MemViewSet(viewsets.ModelViewSet):
    """ Контроллер мемов. """

    queryset = Mem.objects.all()
    serializer_class = MemSerializer

    @action(
        detail=True,
        methods=('post',),
        url_path='like',
    )
    def add_like(self, request, pk):
        mem = Mem.objects.get(pk=pk)
        mem.likes_count = int(mem.likes_count) + 1
        mem.save()
        return Response(
            {'status': 'полайкано', "теперь лаков": mem.likes_count}
        )

    @action(
        detail=True,
        methods=('post',),
        url_path='dislike',
    )
    def delete_like(self, request, pk):
        mem = Mem.objects.get(pk=pk)
        mem.likes_count = int(mem.likes_count) - 1
        mem.save()
        return Response(
            {'status': 'надизлайкано(', "теперь лаков": mem.likes_count}
        )
