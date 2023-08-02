import pandas as pd
import json
from pandas import json_normalize


# json 불러오기
path = './생활 폐기물 이미지/Validation/[V라벨링]라벨링데이터/고철류/기타/12_X001_C045_0201/'
data = pd.read_json(path+'12_X001_C045_0201_0.Json')

# 데이터 가공
df = pd.DataFrame(data=data, columns=['FILE NAME', 'RESOLUTION', 'DAY/NIGHT', 'PLACE', 'PROJECT SORTING', 'BoundingCount'])
box = json_normalize(data['Bounding'])

# "BoundingCount" 크기 만큼 반복할 예정
bounding_len = int(df.loc[0]["BoundingCount"])

# 바운딩박스 폴리곤형태 처리
polygon_list = []
if box.loc[0]["Drawing"] == 'POLYGON':
    for i in range(bounding_len):
        # "PolygonPoint" 안에 있는 좌표값 추출
        points = data["Bounding"][i]["PolygonPoint"]
        x_values = [int(point[f"Point{i+1}"].split(",")[0]) for i, point in enumerate(points)]
        y_values = [int(point[f"Point{i+1}"].split(",")[1]) for i, point in enumerate(points)]

        x1, x2 = min(x_values), max(x_values)
        y1, y2 = min(y_values), max(y_values)

        polygon_values = pd.DataFrame({"CLASS": [box.loc[i]["CLASS"]],
            "DETAILS": [box.loc[i]["DETAILS"]],
            "DAMAGE": [box.loc[i]["DAMAGE"]],
            "TRANSPARENCY": [box.loc[i]["TRANSPARENCY"]],
            "Color": [box.loc[i]["Color"]],
            "Shape": [box.loc[i]["Shape"]],
            "Texture": [box.loc[i]["Texture"]],
            "Object Size": [box.loc[i]["Object Size"]],
            "Direction": [box.loc[i]["Direction"]],
            "Drawing": [box.loc[i]["Drawing"]],
            "PolygonCount": [box.loc[i]["PolygonCount"]],
            "x1": [x1],
            "y1": [y1],
            "x2": [x2],
            "y2": [y2]})
        polygon_list.append(polygon_values)
    polygon_values = pd.concat(polygon_list).reset_index(drop=True)
    print(polygon_values)

# 바운딩박스 박스형태 처리
if box.loc[0]["Drawing"] == 'BOX':
    box_values = pd.concat([df, box], axis=1)
    print(box_values)
# 결과
#result = pd.concat([df,polygon_values], axis=1)
#print(result)

# 폴리곤은 해결, 박스 1개짜리 해결, 박스 여러개짜리 해결해보기