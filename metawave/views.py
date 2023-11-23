from ..model.img_analysis import analyze_image, analyze_image_to_csv
from django.shortcuts import render
from .models import Picture
from joblib import load
import os, random, pygame
import pandas as pd
import pdb



# 모델 및 데이터 파일의 경로 설정
RendomFrest_model_path = r"model\model_depth10.joblib"
mlb_path = r"model\mlb.joblib"
csv_file_path = r"model\input_image_analysis_results.csv"
music_folder_path = r"C:\Users\gjaischool\Desktop\jamendo"


# 웹 페이지의 메인 페이지 처리 함수
def mainPage(request):
    #pdb.set_trace()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'upload':
            # 이미지 업로드 로직 처리
            handle_image_upload(request)
        elif action == 'play':
            # 재생
            play_music(mood_list)
        elif action == 'pause':
            # 정지
            handle_pause()
        elif action == 'next':
            # 다음 곡
            handle_next()
        elif action == 'previous':
            # 이전 곡
            handle_previous()

    return render(request, "mainPage_copy.html")

def handle_pause():
    # 음악 일시정지 로직 (실제 구현 필요)
    return HttpResponse("Music playback paused.")

def handle_next():
    # 다음 곡 재생 로직 (실제 구현 필요)
    return HttpResponse("Next music track.")

def handle_previous():
    # 이전 곡 재생 로직 (실제 구현 필요)
    return HttpResponse("Previous music track.")



def handle_image_upload(request):
    picture = request.FILES.get('picture')
    if not picture:
        return HttpResponse("No image uploaded.", status=400)

    picture_instance = Picture(picture=picture)
    picture_instance.save()
    global mood_list
    mood_list = analyze_image_and_predict_mood(picture_instance.picture.path)
    

def play_music(mood_list):
    music_files = []
    for mood in mood_list:
        music_files.extend(get_music_files_for_mood(mood))

    selected_music_file = random.choice(music_files) if music_files else None
    pygame.init()

    if selected_music_file:
        pygame.mixer.music.load(selected_music_file)
        pygame.mixer.music.play()
        mood_folder = os.path.basename(os.path.dirname(selected_music_file))

        print("recommender song list : ", cleaned_predicted_mood_list)
        print("recommender song count : ", len(music_files))
        print("selected Mood : ", mood_folder)
        print("Playing Music File:", selected_music_file)
    else:
        print("No music files found for the given moods.")

def analyze_image_and_predict_mood(image_path):
    color_ratios = analyze_image(image_path)
    analyze_image_to_csv(image_path, color_ratios)
    
    try:
        RendomFrest_model = load(RendomFrest_model_path)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return[]
    
    mlb = load(mlb_path)
    data_df = pd.read_csv(csv_file_path)
    new_data = data_df.iloc[0].to_dict()
    new_data.pop('Filename', None)
    new_data_df = pd.DataFrame([new_data])

    predicted_mood = RendomFrest_model[0].predict(new_data_df)
    predicted_mood_list = mlb.inverse_transform(predicted_mood)

    cleaned_predicted_mood_list = [mood.strip() for mood_tuple in predicted_mood_list for mood in mood_tuple]
    return cleaned_predicted_mood_list

def get_music_files_for_mood(mood):
    mood_folder = os.path.join(music_folder_path, mood)
    if os.path.exists(mood_folder):
        return [os.path.join(mood_folder, file) for file in os.listdir(mood_folder) if file.endswith(('.mp3', '.wav'))]
    else:
        return []
    

