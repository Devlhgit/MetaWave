from django.shortcuts import render
from django.db.models import Q
from .models import inputPicture, MoodthemePlaylist

import random
# import model.song_recommender

def mainPage(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']
        musicGenre = request.POST['musicGenre']
        
        print('picture_url :', pictures )
        print('/media/pictures/'+str(pictures))

        picture_instance = inputPicture(name=name, author=author, picture=pictures, musicGenre=musicGenre)
        picture_instance.save()

        # 선택한 장르와 같은 랜덤한 10개의 PlayList 출력
        random_playList = MoodthemePlaylist.objects.filter(Q(tags=musicGenre) | Q(tags=musicGenre)).order_by('?')[:10]

        

        return render(request, 'recommend.html', 
                      {'picture' : picture_instance, 
                       'random_playList' : random_playList})
    
    return render(request, "mainPage.html")

