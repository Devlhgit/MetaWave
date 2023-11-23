import os
from joblib import load
import random
import pygame
import pandas as pd
<<<<<<< HEAD
from img_analysis import analyze_image, analyze_image_to_csv
=======
from img_analysis import Analyze_Image, Analyze_Image_To_CSV
>>>>>>> H


input_image_path = r"C:\Users\gjaischool\Desktop\data\imgData96015\images\marina\032e9f8d41ae897b486a1d21889db454c.jpg"
RendomFrest_model_path = r"model\model.pkl"
mlb_path = r"model\mlb.pkl"
csv_file_path = r"model\input_image_analysis_results.csv"
music_folder_path = r"C:\Users\gjaischool\Desktop\jamendo"

<<<<<<< HEAD

color_ratios = analyze_image(global_image_path)
analyze_image_to_csv(global_image_path, color_ratios)
=======
color_ratios = Analyze_Image(input_image_path)
Analyze_Image_To_CSV(input_image_path, color_ratios)
>>>>>>> H

# 모델 로드
RendomFrest_model = load(RendomFrest_model_path)

# mlb 객체 로드
mlb = load(mlb_path)

data_df = pd.read_csv(csv_file_path)

new_data = data_df.iloc[0].to_dict()

# 'Filename' 열 제거
new_data.pop('Filename', None)

# DataFrame으로 변환
new_data_df = pd.DataFrame([new_data])

# 특성 순서와 이름을 맞추기
new_data = new_data_df[[
    'Warm', 'Cool',
    'Bright', 'Mid', 'Dark',
    'Red', 'Orange', 'Brown', 'Gold', 'Yellow',
    'Lime', 'Pink', 'Green', 'Mint', 'SeaBlue',
    'Sky', 'Blue', 'Purple',
    "Black", "White", "Grey"
]]


# 첫 번째 모델을 사용하여 예측 수행
predicted_mood = RendomFrest_model[0].predict(new_data)


# 예측된 라벨을 분위기 이름으로 매핑
predicted_mood_list = mlb.inverse_transform(predicted_mood)

# 결과 해석
cleaned_predicted_mood_list = []
for mood_tuple in predicted_mood_list:
    for mood in mood_tuple:
        if isinstance(mood, str):
            cleaned_mood = mood.strip(" '\"{}").strip()
            cleaned_predicted_mood_list.append(cleaned_mood)

# 각 분위기에 대한 음악 파일 리스트를 가져오는 함수
def get_music_files_for_mood(mood):
    mood_folder = os.path.join(music_folder_path, mood)
    if os.path.exists(mood_folder):
        return [os.path.join(mood_folder, file) for file in os.listdir(mood_folder) if file.endswith(('.mp3', '.wav'))]
    else:
        return []

# 각 분위기에 대한 음악 파일 리스트
music_files = []
for mood in cleaned_predicted_mood_list:
    music_files.extend(get_music_files_for_mood(mood))

# 랜덤 음악 파일 선택
selected_music_file = random.choice(music_files) if music_files else None

# 선택된 음악 파일 재생
if selected_music_file:
    pygame.mixer.init()
    pygame.mixer.music.load(selected_music_file)
    pygame.mixer.music.play()
    mood_folder = os.path.basename(os.path.dirname(selected_music_file))

    print("Recommended song list: ", cleaned_predicted_mood_list)
    print("Recommended song count: ", len(music_files))
    print("Selected Mood: ", mood_folder)
    print("Playing Music File:", selected_music_file)

    # 재생 중 대기 (필요에 따라 조정)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
else:
    print("No music files found for the given moods.")