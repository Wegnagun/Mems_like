from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import Mem


@admin.register(Mem)
class MemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'mem_id', 'img', 'text', 'pub_date', 'post_author', 'likes_count'
    )
    save_on_top = True

    @admin.display(description='Картинка мема')
    def img(self, obj):
        return format_html(
            f'<img src={obj.image_url} '
            f'alt="не загрузилась" style=" width: 200px;">'
        )


admin.site.unregister(Group)
