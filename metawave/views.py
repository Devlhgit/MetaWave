from django.shortcuts import render
from django.db.models import Q
from .models import inputPicture, MoodthemePlaylist

import random

# python debugging
# import pdb
# def some_function():
#     # 코드
#     pdb.set_trace()  # 디버거 실행

def mainPage(request):
    if request.method == "POST":
        # some_function()
        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']
        musicGenre = request.POST['musicGenre']
        print('musicGenre :', musicGenre)

        picture_instance = inputPicture(name=name, author=author, picture=pictures, musicGenre=musicGenre)
        picture_instance.save()

        # 선택한 장르와 같은 랜덤한 10개의 PlayList 출력
        random_playList = MoodthemePlaylist.objects.filter(Q(tags=musicGenre) | Q(tags=musicGenre)).order_by('?')[:10]

        return render(request, 'recommend.html', 
                      {'picture' : picture_instance, 
                       'random_playList' : random_playList})
    
    return render(request, "mainPage.html")

# # Show data in HTML
# def musicPlayList(request):
#     all_playList = MoodthemePlaylist.objects.all()
#     random_playList = random.sample(list(all_playList), 10) # Random 10 data

#     context = {'random_playList' : random_playList}
    
#     return render(request, 'recommend.html', context) # 'recommend.html으로 전달'