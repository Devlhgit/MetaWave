from django.shortcuts import render

def mainPage(request):
    # 메인 페이지 렌더링 및 POST 요청 처리
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']
        musicGenre = request.POST['musicGenre']

    return render(request, "mainPage.html")