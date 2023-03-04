from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

admin.site.site_header = 'Зацени Мем'
admin.site.index_title = 'Разделы админки'
admin.site.site_title = 'Админка'


router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
