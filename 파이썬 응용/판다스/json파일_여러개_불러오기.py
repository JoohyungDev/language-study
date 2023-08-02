import pandas as pd
import json
import os
from pandas import json_normalize

# 폴더 경로
dir_path = 'C:/Users/PJH/Desktop/생활 폐기물 이미지/Validation/[V라벨링]라벨링데이터'

# 비어있는 데이터 프레임 생성
result_df = pd.DataFrame()

# os.walk = 모든 하위 폴더를 순회, dirnames = 하위 디렉토리의 리스트 반환
for dirpath, dirnames, filenames in os.walk(dir_path):
    for file in filenames:
        if file.endswith('json'):
            file_path = os.path.join(dirpath, file)
            data = pd.read_json(file_path)
            # boundingbox를 제외한 값 불러오기
            selected_values = data.iloc[0, [0, 6, 16, 17, 18, 19]] 
            # boundingbox 괄호 해제
            bounding_df = json_normalize(data['Bounding'][0]) 
            # boundingbox 값만 불러오기
            bounding_values = bounding_df.iloc[0,[0,1,2,3,4,5,6,7,8,9,10,11,12,13]] 
            # bounding box가 아닌것 + bounding box
            result = pd.concat([selected_values, bounding_values], axis=0) 
            # 결과 데이터프레임에 삽입
            result_df = pd.concat([result_df, result], axis=1) 

print(result_df)