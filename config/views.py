from django.shortcuts import render
from metawave.models import picture
# from django.shortcuts import redirect


def mainPage(request):
    if request.method == "POST":
        # print(111, request.POST)
        # print(222, request.FILES)
        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']

        picture_instance = picture(name=request.POST['name'], author=request.POST['author'], picture=request.FILES['picture'])
        picture_instance.save()
        

        # uploaded_file = request.FILES.get('picture')

        # if uploaded_file is not None:

        #     print('uploaded_file:', uploaded_file)
        #     context = {'uploaded_file' : uploaded_file.url}
        #     print('context:', context)

        # return render(request, 'recommend.html', context)
    
    return render(request, "mainPage.html")


def recommend(request):
    return render(request, 'recommend.html',)
