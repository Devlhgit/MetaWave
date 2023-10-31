from django.shortcuts import render
from metawave.models import picture
# from django.shortcuts import redirect


def mainPage(request):
    if request.method == "POST":
        print(111, request.POST)
        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']

        picture_instance = picture(name=request.POST['name'], author=request.POST['author'], picture=request.FILES['picture'])
        picture_instance.save()

        return render(request, 'recommend.html')

    return render(request, "mainPage.html")


def recommend(request):
    return render(request, 'recommend.html')
