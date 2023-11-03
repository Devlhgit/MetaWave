from django.contrib import admin
from metawave.models import picture

@admin.register(picture)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'author', 'picture']
