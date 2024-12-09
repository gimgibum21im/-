import pandas as pd

# 파일 불러오기

data_19_1 = pd.read_csv('src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_01.csv')
data_19_2 = pd.read_csv('src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_03.csv')
data_19_3 = pd.read_csv('src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_04.csv')

data_21_1 = pd.read_csv("src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_경기_202106.csv")
data_21_2 = pd.read_csv("src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_부산_202106.csv")
data_21_3 = pd.read_csv("src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_서울_202106.csv")
data_21_4 = pd.read_csv("src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_제주_202106.csv")
filtered_2019_2 = data_19_2[data_19_2['시도명'] == '경기도']
filtered_2019_3 = data_19_3[data_19_3['시도명'] == '제주특별자치도']

combined_2019 = pd.concat([data_19_1, filtered_2019_2, filtered_2019_3], ignore_index=True)
combined_2021 = pd.concat([data_21_1, data_21_2, data_21_3, data_21_4], ignore_index=True)

# 분석에 필요한 column 추출
data_19=combined_2019[['상가업소번호','상호명','지점명','상권업종대분류명','상권업종중분류명','시도명']] 
data_21=combined_2021[['상가업소번호','상호명','지점명','상권업종대분류명','상권업종중분류명','시도명']] 
# 데이터 내 중복 제거
data_21 = data_21.drop_duplicates(subset=['상가업소번호'])
data_19 = data_19.drop_duplicates(subset=['상가업소번호'])

# print(data_21.상권업종대분류명.unique())

categories = ['소매', '음식','관광/여가/오락','숙박']

# 폐업률 차집함 구하는 코드
closed_stores = data_19[~data_19[['상가업소번호']].apply(tuple, axis=1).isin(data_21[['상가업소번호']].apply(tuple, axis=1))] 
print("폐업한 가계수: ", len(closed_stores))
closed_rate=len(closed_stores)/len(data_19)*100
print(f"폐업률: {closed_rate:.2f}%")
print("\n=====\n")

# 대분류별 폐업률
for category in categories:
    if category=='관광/여가/오락':
        total_stores_in_category_19 = data_19[(data_19['상권업종대분류명'] == category) & (data_19['상권업종중분류명'] != '스포츠/운동')]
        closed_stores_in_category = closed_stores[(closed_stores['상권업종대분류명'] == category) & (closed_stores['상권업종중분류명'] != '스포츠/운동')]
    
    else:
        total_stores_in_category_19 = data_19[data_19['상권업종대분류명'] == category]
        closed_stores_in_category = closed_stores[closed_stores['상권업종대분류명'] == category]
    
    if len(total_stores_in_category_19) > 0:  # 대분류에 데이터가 있는지 확인
        closure_rate_category = len(closed_stores_in_category) / len(total_stores_in_category_19) * 100
        print(f"'{category}' 업종의 폐업률: {closure_rate_category:.2f}%")
    else:
        print(f"'{category}' 업종에 대한 데이터가 없습니다.")

total_stores_in_category_19 = data_19[(data_19['상권업종중분류명'] =='스포츠/운동') | (data_19['상권업종대분류명']=='스포츠') | (data_19['상권업종중분류명']=='학원-예능취미체육') ]
closed_stores_in_category = closed_stores[(closed_stores['상권업종중분류명'] == '스포츠/운동')|(closed_stores['상권업종대분류명']=='스포츠') | (closed_stores['상권업종중분류명']=='학원-예능취미체육')]
    
if len(total_stores_in_category_19) > 0:  # 대분류에 데이터가 있는지 확인
    closure_rate_category = len(closed_stores_in_category) / len(total_stores_in_category_19) * 100
    print(f"'스포츠/운동' 업종의 폐업률: {closure_rate_category:.2f}%")
else:
    print(f"'스포츠/운동' 업종에 대한 데이터가 없습니다.")
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
    total_stores_in_group = data_19[data_19['상권업종중분류명'].isin(subcategories)]
    closed_stores_in_group = closed_stores[closed_stores['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_group) > 0:  # 중분류에 데이터가 있는지 확인
        closure_rate_group = len(closed_stores_in_group) / len(total_stores_in_group) * 100
        print(f"'{group}' 업종의 폐업률: {closure_rate_group:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")


# 개업률
open_stores = data_21[~data_21[['상가업소번호']].apply(tuple, axis=1).isin(data_19[['상가업소번호']].apply(tuple, axis=1))]
print("개업한 가계수: ", len(open_stores))
open_rate=len(open_stores)/len(data_19)*100
print(f"개업률: {open_rate:.2f}%")
print("\n=====\n")


# 각 대분류별 개업률 계산
for category in categories:
    if category=='관광/여가/오락':
        total_stores_in_category_19 = data_19[(data_19['상권업종대분류명'] == category) & (data_19['상권업종중분류명'] != '스포츠/운동')]
        open_stores_in_category = open_stores[(open_stores['상권업종대분류명'] == category) & (open_stores['상권업종중분류명'] != '스포츠/운동')]
    
    else:
        total_stores_in_category_19 = data_19[data_19['상권업종대분류명'] == category]
        open_stores_in_category = open_stores[open_stores['상권업종대분류명'] == category]
    
    if len(total_stores_in_category_19) > 0:  # 대분류에 데이터가 있는지 확인
        open_rate_category = len(open_stores_in_category) / len(total_stores_in_category_19) * 100
        print(f"'{category}' 업종의 개업률: {open_rate_category:.2f}%")
    else:
        print(f"'{category}' 업종에 대한 데이터가 없습니다.")

total_stores_in_category_19 = data_19[(data_19['상권업종중분류명'] =='스포츠/운동') | (data_19['상권업종대분류명']=='스포츠') | (data_19['상권업종중분류명']=='학원-예능취미체육')]
open_stores_in_category = open_stores[(open_stores['상권업종중분류명'] == '스포츠/운동')|(open_stores['상권업종대분류명']=='스포츠')| (open_stores['상권업종중분류명']=='학원-예능취미체육')]

if len(total_stores_in_category_19) > 0:  # 대분류에 데이터가 있는지 확인
    open_rate_category = len(open_stores_in_category) / len(total_stores_in_category_19) * 100
    print(f"'스포츠/운동' 업종의 개업률: {open_rate_category:.2f}%")
else:
    print(f"'스포츠/운동' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")


# 각 중분류별 개업률 계산
for group, subcategories in group_mapping.items():
    total_stores_in_group = data_19[data_19['상권업종중분류명'].isin(subcategories)]
    open_stores_in_group = open_stores[open_stores['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_group) > 0:  # 중분류에 데이터가 있는지 확인
        open_rate_group = len(open_stores_in_group) / len(total_stores_in_group) * 100
        print(f"'{group}' 업종의 개업률: {open_rate_group:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")

