from django.urls import path
from . import views

urlpatterns = [
    path('musicDatas/', views.getTestDatas, name='musicDatas'),
    path('musicData/<int:id>', views.getTestData, name='musicData')
]