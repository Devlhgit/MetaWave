from django.shortcuts import render
from django.db.models import Q
from .models import inputPicture, MoodthemePlaylist
from model.playSongML import inputPath
#from tensorflow.keras.models import load_model
#from model.song_recommender import classify_image, get_music_files_with_themes, play_random_music_with_theme

import  os


# 이미지 분류 및 음악 추천을 수행하는 함수
def classify_and_recommend(request, name, author, pictures, musicGenre):

    # 이미지 분류를 위한 설정
    folder_path = r'C:\Users\GAIS\Documents\GitHub\MetaWave\model\categorized_images'
    class_labels = [folder_name for folder_name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder_name))]

    # 입력 이미지의 경로 생성
    input_img_path = f'C:\\Users\\GAIS\\Documents\\GitHub\\MetaWave\\media\\pictures\\{pictures}'
    print('input_img_path:', input_img_path)
    inputPath(input_img_path)
    
    # 이미지 분류 수행 및 결과 얻기
    # result = classify_image(input_img_path)
    # predic_theme = class_labels[result - 1]

    # 테마에 따라 음악 파일 가져오기
    # music_files_with_themes = get_music_files_with_themes(os.path.join(r'c:\Users\GAIS\mtg-jamendo-dataset\classified_music_data', predic_theme))

    # 선택한 장르와 같은 랜덤한 10개의 플레이리스트 가져오기
    random_playList = MoodthemePlaylist.objects.filter(tags=musicGenre).order_by('?')[:10]

    picture_instance = inputPicture(name=name, author=author, picture=pictures, musicGenre=musicGenre)
    picture_instance.save()

    # recommend.html 템플릿 렌더링 및 필요한 데이터 전달
    # return render(request, 'recommend.html', {
    #     'picture': picture_instance,
    #     'random_playList': random_playList,
    #     'play_random_music_with_theme': play_random_music_with_theme(music_files_with_themes),
    # })


def mainPage(request):
    # 메인 페이지 렌더링 및 POST 요청 처리

    if request.method == "POST":
        # POST 요청이 들어오면 폼 데이터를 추출하여 classify_and_recommend 함수 호출
        name = request.POST['name']
        author = request.POST['author']
        pictures = request.FILES['picture']
        musicGenre = request.POST['musicGenre']

        # 데이터베이스에 이미지 정보 저장
        picture_instance = inputPicture(name=name, author=author, picture=pictures, musicGenre=musicGenre)
        picture_instance.save()

        return classify_and_recommend(request, name, author, pictures, musicGenre)

    # GET 요청일 경우 mainPage.html 템플릿 렌더링
    return render(request, "mainPage.html")




# def mainPage(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         author = request.POST['author']
#         pictures = request.FILES['picture']
#         musicGenre = request.POST['musicGenre']

#         picture_instance = inputPicture(name=name, author=author, picture=pictures, musicGenre=musicGenre)
#         picture_instance.save()

#         # 선택한 장르와 같은 랜덤한 10개의 PlayList 출력
#         random_playList = MoodthemePlaylist.objects.filter(Q(tags=musicGenre) | Q(tags=musicGenre)).order_by('?')[:10]

#         # songrecommender
#         folder_path = r'C:\Users\GAIS\Documents\GitHub\MetaWave\model\categorized_images' # 폴더 경로 설정

#         # 폴더 내의 모든 하위 폴더를 순회하여 클래스 레이블 생성
#         class_labels = [] # 클래스 레이블을 저장할 리스트
#         for folder_name in os.listdir(folder_path):
#             if os.path.isdir(os.path.join(folder_path, folder_name)):
#                 class_labels.append(folder_name)

#         input_img_path = r'C:\Users\GAIS\Documents\GitHub\MetaWave/media/pictures/'+str(pictures) # Input 받은 사진의 경로

#         result = classify_image(input_img_path) # 이미지 정규화

#         predic_theme = class_labels[result -1]  # 예측된 무드와 노래의 태깅
#         print('predic_theme:', predic_theme)

#         # 무작위 음악과 테마 재생
#         music_files_with_themes = get_music_files_with_themes(os.path.join(r'c:\Users\GAIS\mtg-jamendo-dataset\classified_music_data', predic_theme))

#         return render(request, 'recommend.html', 
#                       {'picture' : picture_instance, 
#                        'random_playList' : random_playList,
#                         'play_random_music_with_theme' : play_random_music_with_theme(music_files_with_themes)})

    
#     return render(request, "mainPage.html")




