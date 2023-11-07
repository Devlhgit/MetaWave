from django.shortcuts import render
from .models import inputPicture

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status # POST 메서드를 쓰기 위함
from .models import MusicList
from .serializer import TestDataSerializer

import random

def mainPage(request):
    if request.method == "POST":

        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']

        picture_instance = inputPicture(name=request.POST['name'], author=request.POST['author'], picture=request.FILES['picture'])
        picture_instance.save()
        
        return render(request, 'recommend.html')
    
    return render(request, "mainPage.html")


def recommend(request):
    return render(request, 'recommend.html',)


# Serializer
@api_view(['GET'])
def getTestDatas(request):
    datas = MusicList.objects.all() # MusicList 모든 데이터 읽어들이기
    serializer = TestDataSerializer(datas, many=True) # 데이터 직렬화
    return Response(serializer.data) # 결과 출력

@api_view(['GET'])
def getTestData(request, id):
    data = MusicList.objects.get(id=id) # name필드값이 name인 데이터를 가져옴
    serializer = TestDataSerializer(data, many=False) # serializer에서 하나의 레코드만 가져옴 (many=False)
    return Response(serializer.data)


# Show data in HTML
def musicPlayList(request):
    all_playList = MusicList.objects.all()
    random_playList = random.sample(list(all_playList), 5) # Random 5 data

    context = {'random_playList' : random_playList}
    
    return render(request, 'recommend.html', context) # 'recommend.html으로 전달'