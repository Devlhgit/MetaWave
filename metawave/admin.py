from django.contrib import admin
from .models import Picture


@admin.register(Picture)
class Admin(admin.ModelAdmin):
    list_display = ['id', 'picture']


