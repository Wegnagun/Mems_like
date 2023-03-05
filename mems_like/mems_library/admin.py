from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Mem


@admin.register(Mem)
class MemAdmin(admin.ModelAdmin):
    list_display = ('mem_id', 'text', 'pub_date', 'post_author', 'likes_count')


admin.site.unregister(Group)
