from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os
import pygame
import random

# 클래스 레이블을 저장할 리스트
class_labels = []

# 폴더 경로 설정
folder_path = r'model\categorized_images'
loaded_model = load_model(r'model\vgg16_model.h5')

# 폴더 내의 모든 하위 폴더를 순회하여 클래스 레이블 생성
for folder_name in os.listdir(folder_path):
    if os.path.isdir(os.path.join(folder_path, folder_name)):
        class_labels.append(folder_name)



# 이미지정규화
def classify_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    predictions = loaded_model.predict(img_array)
    predicted_class = np.argmax(predictions)
    return predicted_class

# 음악 파일과 테마 리스트 생성
def get_music_files_with_themes(theme_folder):
    music_files_with_themes = []
    for file in os.listdir(theme_folder):
        if file.endswith(('.mp3', '.wav')):
            music_files_with_themes.append((os.path.join(theme_folder, file), predic_theme))
    return music_files_with_themes

# 무작위 음악 파일과 테마 출력 및 재생 함수
def play_random_music_with_theme(music_files_with_themes):
    pygame.mixer.init()
    music_path, theme = random.choice(music_files_with_themes)
    print(f"Playing theme: {theme} - {os.path.basename(music_path)}")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# 이미지첨부가되면...->
# 입력될 이미지의 경로입니다.
input_img_path = r'C:\Users\GAIS\Desktop\1.jpg'
result = classify_image(input_img_path)
# 예측된 무드와 노래의 태깅
predic_theme = class_labels[result -1]
# 무작위 음악과 테마 재생
music_files_with_themes = get_music_files_with_themes(os.path.join(r'c:\Users\GAIS\mtg-jamendo-dataset\classified_music_data', predic_theme))

# play_random_music_with_theme(music_files_with_themes)