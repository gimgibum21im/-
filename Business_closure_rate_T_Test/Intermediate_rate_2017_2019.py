import os
import pandas as pd

categories = ['소매', '음식', '관광/여가/오락', '숙박']

# 데이터를 불러오는 함수 정의
def load_data(year, region):
    filename = f"./src/상가업소_{year}/{year}_{region}.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        print(f"파일을 찾을 수 없습니다: {filename}")
        return pd.DataFrame()

# 데이터 로드
regions = ['경기도', '서울특별시', '부산광역시', '제주특별자치도']  # 분석할 지역 목록
data_17 = pd.concat([load_data(201706, region) for region in regions], ignore_index=True)
data_19 = pd.concat([load_data(201906, region) for region in regions], ignore_index=True)

# 폐업률 차집합 구하는 코드
closed_stores = data_17[~data_17[['상가업소번호']].apply(tuple, axis=1).isin(data_19[['상가업소번호']].apply(tuple, axis=1))] 

print("\n=====\n")

middle_categories=['음/식료품소매', '가전제품소매']
group_mapping = {
    '식료품 소매' : ['음/식료품소매'],
    '가전제품소매' : ['가전제품소매'],
    '식당': ['한식', '중식', '일식/수산물'],  # 한식, 중식, 일식을 식당으로 묶음
    '기타간이': ['기타음식업'],          # 기타간이 유지
    '카페': ['커피점/카페']                 # 카페 유지
}
# 각 중분류별 폐업률 계산
for group, subcategories in group_mapping.items():
    total_stores_in_group = data_17[data_17['상권업종중분류명'].isin(subcategories)]
    closed_stores_in_group = closed_stores[closed_stores['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_group) > 0:  # 중분류에 데이터가 있는지 확인
        closure_rate_group = len(closed_stores_in_group) / len(total_stores_in_group) * 100
        print(f"'{group}' 업종의 폐업률: {closure_rate_group:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")





# 개업률
open_stores = data_19[~data_19[['상가업소번호']].apply(tuple, axis=1).isin(data_17[['상가업소번호']].apply(tuple, axis=1))]


# 각 중분류별 개업률 계산
for group, subcategories in group_mapping.items():
    total_stores_in_group = data_17[data_17['상권업종중분류명'].isin(subcategories)]
    open_stores_in_group = open_stores[open_stores['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_group) > 0:  # 중분류에 데이터가 있는지 확인
        open_rate_group = len(open_stores_in_group) / len(total_stores_in_group) * 100
        print(f"'{group}' 업종의 개업률: {open_rate_group:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")
