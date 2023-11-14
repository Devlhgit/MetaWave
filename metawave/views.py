from django.shortcuts import render
from .models import inputPicture, MoodthemePlaylist

import random



def mainPage(request):
    if request.method == "POST":

        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']

        picture_instance = inputPicture(name=name, author=author, picture=pictures)
        picture_instance.save()

        all_playList = MoodthemePlaylist.objects.all()
        random_playList = random.sample(list(all_playList), 10)

        context = {'random_playList' : random_playList}

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