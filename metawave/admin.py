from django.contrib import admin
from .models import MusicList, picture

@admin.register(MusicList)
class Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'artist', 'album', 'genre']


@admin.register(picture)
class Admin(admin.ModelAdmin):
    list_display = ['picture']
