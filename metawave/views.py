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


# 웹 페이지의 메인 페이지 처리 함수
def mainPage(request):
    if request.method == "POST":
        pictures = request.FILES['picture']        

        # 이미지데이터 저장
        picture_instance = inputPicture(picture=pictures)
        picture_instance.save()

        # 전역변수 선언
        global global_image_path
        global_image_path = f'C:\\Users\\GAIS\\Documents\\GitHub\\MetaWave\\media\\pictures\\{pictures}'

        # 이미지 분석 및 음악 재생 함수 호출
        analyze_and_play_music()

    return render(request, "mainPage.html")



# 이미지 분석 및 음악 재생 함수
def analyze_and_play_music():
    # 이미지 분석을 통한 색상 비율 계산
    color_ratios = analyze_image(global_image_path)
    analyze_image_to_csv(global_image_path, color_ratios)


    # 머신러닝 모델 로드
    RendomFrest_model = joblib.load(RendomFrest_model_path)
    # mlb 객체 로드
    mlb = joblib.load(mlb_path)
    data_df = pd.read_csv(csv_file_path)
    # 데이터의 첫 행을 새로운 데이터 예시로 사용
    new_data = data_df.iloc[0].to_dict()
    # 'Filename' 열 제거
    new_data.pop('Filename', None)
    # DataFrame으로 변환
    new_data_df = pd.DataFrame([new_data])


    # 분위기 예측
    predicted_mood = RendomFrest_model.predict(new_data_df)
    # 예측된 라벨을 분위기 이름으로 매핑
    predicted_mood_list = mlb.inverse_transform(predicted_mood)


    # 예측된 분위기 정제
    cleaned_predicted_mood_list = []
    for mood_tuple in predicted_mood_list:
        for mood in mood_tuple:
            if isinstance(mood, str):
                cleaned_mood = mood.strip(" '\"{}").strip()
                cleaned_predicted_mood_list.append(cleaned_mood)


    # 해당 분위기에 대한 음악 파일 경로 수집
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
    # pygame 초기화
    pygame.init()
    # 선택된 음악 파일 재생
    if selected_music_file:
        pygame.mixer.music.load(selected_music_file)
        pygame.mixer.music.play()
        mood_folder = os.path.basename(os.path.dirname(selected_music_file))

        print("recommender song list : ", cleaned_predicted_mood_list)
        print("recommender song count : ", len(music_files))
        print("selected Mood : ", mood_folder)
        print("Playing Music File:", selected_music_file)

        # 재생 중 대기 (필요에 따라 조정)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    else:
        print("No music files found for the given moods.")