from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Mem
from .serializers import MemSerializer


class MemViewSet(viewsets.ModelViewSet):
    """ Контроллер мемов. """

    queryset = Mem.objects.all()
    serializer_class = MemSerializer

    @action(
        detail=False,
        methods=('post',),
        url_path='like',
    )
    def add_like(self, request):
        mem = Mem.objects.filter(
            mem_id=request.id
        )
        return 'ssss'
