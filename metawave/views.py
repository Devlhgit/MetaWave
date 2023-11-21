from django.shortcuts import render
from .models import inputPicture


def mainPage(request):
    # 메인 페이지 렌더링 및 POST 요청 처리
    if request.method == "POST":
        pictures = request.FILES['picture']
        
        global global_image_path
        global_image_path = f'C:\\Users\\GAIS\\Documents\\GitHub\\MetaWave\\media\\pictures\\{pictures}'

        picture_instance = inputPicture(picture=pictures)
        picture_instance.save()


    return render(request, "mainPage.html")
