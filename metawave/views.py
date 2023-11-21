from django.shortcuts import render
from .models import inputPicture, MoodthemePlaylist


def mainPage(request):
    # 메인 페이지 렌더링 및 POST 요청 처리
    if request.method == "POST":
        pictures = request.FILES['picture']

        picture_instance = inputPicture(picture=pictures)
        picture_instance.save()

        return render(request, "mainPage.html")


    return render(request, "mainPage.html")