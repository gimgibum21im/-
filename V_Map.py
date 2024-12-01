import folium
import pandas as pd
from rate_17_19 import combined_2017, combined_2019


# 필요한 컬럼만 유지
columns_needed = ['상가업소번호', '위도', '경도', '시도명']
data_17 = combined_2017[columns_needed]
data_19 = combined_2019[columns_needed]

# 경기도 데이터 필터링
data_17_gyeonggi = data_17[data_17['시도명'] == '경기도']
data_19_gyeonggi = data_19[data_19['시도명'] == '경기도']

# 폐업한 가게 (2017에는 있었으나 2019에는 없는 가게)
closed_stores = data_17_gyeonggi[
    ~data_17_gyeonggi['상가업소번호'].isin(data_19_gyeonggi['상가업소번호'])
]

# 개업한 가게 (2019에는 있으나 2017에는 없는 가게)
open_stores = data_19_gyeonggi[
    ~data_19_gyeonggi['상가업소번호'].isin(data_17_gyeonggi['상가업소번호'])
]

# 유지된 가게 (2017과 2019에 모두 있는 가게)
active_stores = data_17_gyeonggi[
    data_17_gyeonggi['상가업소번호'].isin(data_19_gyeonggi['상가업소번호'])
]

# 지도 초기화 (경기도 중심)
gyeonggi_center = [37.413294, 127.5183]  # 경기도 중심 위도/경도
map_gyeonggi = folium.Map(location=gyeonggi_center, zoom_start=10)

# 점 추가 함수
def add_markers_to_map(df, color, map_object, batch_size=10000):
    """
    데이터를 지도에 추가하는 함수
    - df: 데이터프레임 (위도, 경도 포함)
    - color: 점 색상
    - map_object: folium 지도 객체
    - batch_size: 한 번에 처리할 데이터 수
    """
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i + batch_size]
        for _, row in batch.iterrows():
            if pd.notnull(row['위도']) and pd.notnull(row['경도']):
                folium.CircleMarker(
                    location=[row['위도'], row['경도']],
                    radius=3,
                    color=color,
                    fill=True,
                    fill_opacity=0.3
                ).add_to(map_object)

# 지도에 데이터 추가
add_markers_to_map(closed_stores, 'blue', map_gyeonggi)  # 폐업한 가게: 파란색
add_markers_to_map(open_stores, 'red', map_gyeonggi)     # 개업한 가게: 빨간색
add_markers_to_map(active_stores, 'black', map_gyeonggi) # 유지된 가게: 검은색

# 지도 저장
map_gyeonggi.save('gyeonggi_map.html')
print("지도 저장 완료: 'gyeonggi_map.html'")
