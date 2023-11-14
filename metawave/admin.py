from django.contrib import admin
from .models import MusicList, inputPicture

import base64
from django.utils.safestring import mark_safe

@admin.register(MusicList)
class Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'artist', 'album', 'genre']


@admin.register(inputPicture)
class Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'display_picture']

    def display_picture(self, obj): # MySQL BLOB 데이터 이미지 객체로 변환
        image_data_base64 = base64.b64encode(obj.picture).decode('utf-8')
        image_tag = f'<img src="data:image/png;base64,{image_data_base64}" style="max-width:300px;max-height:300px"/>'
        return mark_safe(image_tag)

    display_picture.short_description = 'Picture'
