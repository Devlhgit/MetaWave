from django.shortcuts import render

def mainPage(request):
    # 메인 페이지 렌더링 및 POST 요청 처리
    if request.method == "POST":
        pictures = request.FILES['picture']
        
        global global_image_path
        global_image_path = f'C:\\Users\\GAIS\\Documents\\GitHub\\MetaWave\\media\\pictures\\{pictures}'


    return render(request, "mainPage.html")
