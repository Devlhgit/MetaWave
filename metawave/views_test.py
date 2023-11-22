from django.shortcuts import render
from .models import inputPicture
import os, joblib, random, pygame
import pandas as pd
from model.img_analysis import analyze_image, analyze_image_to_csv

# 모델 및 데이터 파일의 경로 설정
RendomFrest_model_path = r"C:\Users\GAIS\Documents\GitHub\MetaWave\model\Recommended_Moodes_Predict.pkl"
mlb_path = r"C:\Users\GAIS\Documents\GitHub\MetaWave\model\mlb.pkl"
csv_file_path = r"C:\Users\GAIS\Documents\GitHub\MetaWave\model\input_image_analysis_results.csv"
music_folder_path = r"C:\Users\GAIS\mtg-jamendo-dataset\classified_music_data"


def mainPage(request):
    if request.method == "POST":
        pictures = request.FILES['picture']
        handle_uploaded_picture(pictures)
        analyze_and_play_music()

    return render(request, "mainPage.html")

# 이미지 처리 함수
def handle_uploaded_picture(picture):
    global global_image_path
    global_image_path = f'C:\\Users\\GAIS\\Documents\\GitHub\\MetaWave\\media\\pictures\\{picture}'
    picture_instance = inputPicture(picture=picture)
    picture_instance.save()

# 이미지 분석 및 음악 재생 함수
def analyze_and_play_music():
    color_ratios = analyze_image(global_image_path)
    analyze_image_to_csv(global_image_path, color_ratios)
    
    RendomFrest_model = load_random_forest_model()
    mlb = load_mlb_model()
    new_data_df = prepare_new_data()
    
    predicted_mood_list = predict_mood(RendomFrest_model, mlb, new_data_df)
    cleaned_predicted_mood_list = clean_predicted_mood(predicted_mood_list)
    
    music_files = get_music_files(cleaned_predicted_mood_list)
    play_random_music(music_files, cleaned_predicted_mood_list)

# 머신러닝 모델 로드 함수
def load_random_forest_model():
    return joblib.load(RendomFrest_model_path)

# mlb 객체 로드 함수
def load_mlb_model():
    return joblib.load(mlb_path)

# 데이터 준비 함수
def prepare_new_data():
    data_df = pd.read_csv(csv_file_path)
    new_data = data_df.iloc[0].to_dict()
    new_data.pop('Filename', None)
    return pd.DataFrame([new_data])

# 분위기 예측 함수
def predict_mood(model, mlb, data_df):
    predicted_mood = model.predict(data_df)
    return mlb.inverse_transform(predicted_mood)

# 예측된 분위기 정제 함수
def clean_predicted_mood(predicted_mood_list):
    cleaned_predicted_mood_list = []
    for mood_tuple in predicted_mood_list:
        for mood in mood_tuple:
            if isinstance(mood, str):
                cleaned_mood = mood.strip(" '\"{}").strip()
                cleaned_predicted_mood_list.append(cleaned_mood)
    return cleaned_predicted_mood_list

# 해당 분위기에 대한 음악 파일 경로 수집 함수
def get_music_files_for_mood(mood):
    mood_folder = os.path.join(music_folder_path, mood)
    if os.path.exists(mood_folder):
        return [os.path.join(mood_folder, file) for file in os.listdir(mood_folder) if file.endswith(('.mp3', '.wav'))]
    else:
        return []

# 각 분위기에 대한 음악 파일 리스트 수집 함수
def get_music_files(cleaned_predicted_mood_list):
    music_files = []
    for mood in cleaned_predicted_mood_list:
        music_files.extend(get_music_files_for_mood(mood))
    return music_files

# 랜덤 음악 파일 선택 및 재생 함수
def play_random_music(music_files, cleaned_predicted_mood_list):
    selected_music_file = random.choice(music_files) if music_files else None
    pygame.init()
    
    if selected_music_file:
        pygame.mixer.music.load(selected_music_file)
        pygame.mixer.music.play()
        mood_folder = os.path.basename(os.path.dirname(selected_music_file))
        
        print("recommender song list:", cleaned_predicted_mood_list)
        print("recommender song count:", len(music_files))
        print("selected Mood:", mood_folder)
        print("Playing Music File:", selected_music_file)

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("No music files found for the given moods.")
