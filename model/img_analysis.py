import colorsys
import numpy as np
from PIL import Image
import csv
import os
import pandas as pd

csv_file_path = r"model\input_image_analysis_results.csv"  # 결과 CSV 파일 경로 변경 필요
test = ""
# 이미지 분석을 위한 함수를 정의합니다.
def Analyze_Image(image_path):
     # 이미지를 불러와서 RGB로 변환합니다.
    image = Image.open(image_path)
    image = image.convert("RGB")
    global test
    test = image_path
    # 이미지를 numpy array로 변환합니다.
    image_array = np.array(image)

    # 색상 분석 로직
    return Analyze_colors(image_array)

def Analyze_colors(image_array):

    color_counters = {
        "Dark": 0, "Mid": 0, "Bright": 0,
        "Warm": 0, "Cool": 0,
        "Red": 0, "Orange": 0, "Brown": 0, "Gold": 0, "Yellow": 0, "Lime": 0, "Green": 0,
        "Mint": 0, "SeaBlue": 0, "Sky": 0, "Blue": 0, "Purple": 0, "Pink": 0,
        "Black": 0, "White": 0, "Grey": 0
    }

    warm_colors = set(['Red', 'Orange', 'Brown', 'Gold', 'Yellow', 'Lime', 'Pink'])
    cool_colors = set(['Green', 'Mint', 'SeaBlue', 'Sky', 'Blue', 'Purple', 'Black', 'White', 'Grey'])

    for row in image_array:
        for pixel in row:
            r, g, b = pixel
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

            check_sv = (s >= 0.2 and v >= 0.2)

            # 밝기
            if v <= 0.3:
                color_counters["Dark"] += 1
            elif v >= 0.7:
                color_counters["Bright"] += 1
            else:
                color_counters["Mid"] += 1
            
            # 색온도
            if (h <= 82/360 or h >= 338/360):
                color_counters["Warm"] += 1
            else:
                color_counters["Cool"] += 1
            
            # 지배색
            if 344/360 <= h or h <= 14/360 and check_sv:
                color_counters["Red"] += 1
            elif 15/360 <= h <= 38/360 and check_sv:
                color_counters["Orange"] += 1
            elif 15/360 <= h <= 45/360 and 0.25 <= s <= 0.75 and 0.3 <= v <= 0.7:
                color_counters["Brown"] += 1
            elif 39/360 <= h <= 50/360 and check_sv:
                color_counters["Gold"] += 1
            elif 51/360 <= h <= 63/360 and check_sv:
                color_counters["Yellow"] += 1
            elif 64/360 <= h <= 83/360 and check_sv:
                color_counters["Lime"] += 1
            elif 84/360 <= h <= 160/360 and check_sv:
                color_counters["Green"] += 1
            elif 161/360 <= h <= 175/360 and check_sv:
                color_counters["Mint"] += 1
            elif 176/360 <= h <= 185/360 and check_sv:
                color_counters["SeaBlue"] += 1
            elif 186/360 <= h <= 205/360 and check_sv:
                color_counters["Sky"] += 1
            elif 206/360 <= h <= 260/360 and check_sv:
                color_counters["Blue"] += 1
            elif 261/360 <= h <= 290/360 and check_sv:
                color_counters["Purple"] += 1
            elif 291/360 <= h <= 343/360 and check_sv:
                color_counters["Pink"] += 1
            else:
                if v < 0.2:
                    color_counters["Black"] += 1
                elif v > 0.8:
                    color_counters["White"] += 1
                else:
                    color_counters["Grey"] += 1

    color_counters['Warm'] = sum([color_counters[color] for color in warm_colors])
    color_counters['Cool'] = sum([color_counters[color] for color in cool_colors])

    total_pixels = image_array.shape[0] * image_array.shape[1]
    color_ratios = {k: v / total_pixels for k, v in color_counters.items()}
    
    return color_ratios

def Analyze_Image_To_CSV(image_path, color_ratios):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    if os.path.splitext(image_path)[1].lower() in image_extensions:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Filename', "Warm", "Cool",
                "Bright", "Mid", "Dark",
                "Red", "Orange", "Brown", "Gold", "Yellow", "Lime", "Pink", "Green", "Mint", "SeaBlue", "Sky", "Blue", "Purple", 
                "Black", "White", "Grey"
            ]

            
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # 이미지 분석
            color_ratios = Analyze_Image(image_path)
            
            # CSV 파일에 결과를 기록하기 위해 새로운 row 생성
            row = {
                'Filename': os.path.basename(image_path),
                'Warm': color_ratios['Warm'],
                'Cool': color_ratios['Cool'],
                'Bright': color_ratios['Bright'],
                'Mid': color_ratios['Mid'],
                'Dark': color_ratios['Dark'],
                'Red': color_ratios['Red'],
                'Orange': color_ratios['Orange'],
                'Brown': color_ratios['Brown'],
                'Gold': color_ratios['Gold'],
                'Yellow': color_ratios['Yellow'],
                'Lime': color_ratios['Lime'],
                'Green': color_ratios['Green'],
                'Mint': color_ratios['Mint'],
                'SeaBlue': color_ratios['SeaBlue'],
                'Sky': color_ratios['Sky'],
                'Blue': color_ratios['Blue'],
                'Purple': color_ratios['Purple'],
                'Pink': color_ratios['Pink'],
                'Black': color_ratios['Black'],
                'White': color_ratios['White'],
                'Grey': color_ratios['Grey'],
            }
            
            writer.writerow(row)

