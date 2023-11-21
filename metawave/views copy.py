from django.shortcuts import render
from .models import inputPicture, MoodthemePlaylist

import  os


# 이미지 분류 및 음악 추천을 수행하는 함수
def classify_and_recommend(request, pictures):

    # 이미지 분류를 위한 설정
    folder_path = r'C:\Users\GAIS\Documents\GitHub\MetaWave\model\categorized_images'
    # class_labels = [folder_name for folder_name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder_name))]

    # 입력 이미지의 경로 생성
    input_img_path = f'C:\\Users\\GAIS\\Documents\\GitHub\\MetaWave\\media\\pictures\\{pictures}'
    print('input_img_path:', input_img_path)
    # inputPath(input_img_path)
    
    # 이미지 분류 수행 및 결과 얻기
    # result = classify_image(input_img_path)
    # predic_theme = class_labels[result - 1]

    # 테마에 따라 음악 파일 가져오기
    # music_files_with_themes = get_music_files_with_themes(os.path.join(r'c:\Users\GAIS\mtg-jamendo-dataset\classified_music_data', predic_theme))

    picture_instance = inputPicture(picture=pictures)
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
        print("POST 요청 받음")

        pictures = request.FILES['picture']

        # 데이터베이스에 이미지 정보 저장
        picture_instance = inputPicture(picture=pictures)
        picture_instance.save()

        return classify_and_recommend(request, pictures)

    # GET 요청일 경우 mainPage.html 템플릿 렌더링
    return render(request, "mainPage.html")






