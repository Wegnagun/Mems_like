from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from mems_library.views import MemViewSet

admin.site.site_header = 'Зацени Мем'
admin.site.index_title = 'Разделы админки'
admin.site.site_title = 'Админка'


router = routers.DefaultRouter()
router.register('mem', MemViewSet, basename='mem')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
