from rest_framework import viewsets

from .models import Mem
from .serializers import MemSerializer


class MemViewSet(viewsets.ModelViewSet):
    """ Контроллер мемов. """

    queryset = Mem.objects.all()
    serializer_class = MemSerializer
