import pandas as pd

# 파일 불러오기
data_19_1 = pd.read_csv('소상공인시장진흥공단_상가업소정보_201906_01.csv')
data_19_2 = pd.read_csv('소상공인시장진흥공단_상가업소정보_201906_03.csv').query('시도명 == "경기도"')
data_19_3 = pd.read_csv('소상공인시장진흥공단_상가업소정보_201906_04.csv').query('시도명 == "제주특별자치도"')
data_17_1 = pd.read_csv('상가업소_201706_01.csv', encoding='CP949')
data_17_2 = pd.read_csv('상가업소_201706_03.csv', encoding='CP949').query('시도명 == "경기도"')
data_17_3 = pd.read_csv('상가업소_201706_04.csv', encoding='CP949').query('시도명 == "제주특별자치도"')

combined_2019 = pd.concat([data_19_1, data_19_2, data_19_3], ignore_index=True)
combined_2017 = pd.concat([data_17_1, data_17_2, data_17_3], ignore_index=True)


# 분석에 필요한 column 추출
data_19=combined_2019[['상가업소번호','상호명','지점명','상권업종대분류명','상권업종중분류명','시도명']] 
data_17=combined_2017[['상가업소번호','상호명','지점명','상권업종대분류명','상권업종중분류명','시도명']] 
# 데이터 내 중복 제거
data_17 = data_17.drop_duplicates(subset=['상가업소번호'])
data_19 = data_19.drop_duplicates(subset=['상가업소번호'])

# print(data_17.상권업종대분류명.unique())

categories = ['소매', '음식','관광/여가/오락','숙박']

# 폐업률 차집합 구하는 코드
closed_stores_17_19 = data_17[~data_17[['상가업소번호']].apply(tuple, axis=1).isin(data_19[['상가업소번호']].apply(tuple, axis=1))] 
print("폐업한 가계수: ", len(closed_stores_17_19))
closed_rate=len(closed_stores_17_19)/len(data_17)*100
print(f"폐업률: {closed_rate:.2f}%")
print("\n=====\n")

# 대분류별 폐업률
# 각 대분류별 폐업률 계산
for category in categories:
    total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
    closed_stores_17_19_in_category = closed_stores_17_19[closed_stores_17_19['상권업종대분류명'] == category]
    
    if len(total_stores_in_category_17) > 0:  # 대분류에 데이터가 있는지 확인
        closure_rate_category = len(closed_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        print(f"'{category}' 업종의 폐업률: {closure_rate_category:.2f}%")
    else:
        print(f"'{category}' 업종에 대한 데이터가 없습니다.")
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
    closed_stores_17_19_in_group = closed_stores_17_19[closed_stores_17_19['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_category_17) > 0:  # 중분류에 데이터가 있는지 확인
        closure_rate_category = len(closed_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        print(f"'{group}' 업종의 폐업률: {closure_rate_category:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")



# 개업률
open_stores_17_19 = data_19[~data_19[['상가업소번호']].apply(tuple, axis=1).isin(data_17[['상가업소번호']].apply(tuple, axis=1))]
print("개업한 가계수: ", len(open_stores_17_19))
open_rate=len(open_stores_17_19)/len(data_17)*100
print(f"개업률: {open_rate:.2f}%")
print("\n=====\n")



# 각 대분류별 폐업률 계산
for category in categories:
    total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
    open_stores_17_19_in_category = open_stores_17_19[open_stores_17_19['상권업종대분류명'] == category]
    
    if len(total_stores_in_category_17) > 0:  # 대분류에 데이터가 있는지 확인
        open_rate_category = len(open_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        print(f"'{category}' 업종의 폐업률: {open_rate_category:.2f}%")
    else:
        print(f"'{category}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")


# 각 중분류별 개업률 계산
for group, subcategories in group_mapping.items():
    total_stores_in_group = data_17[data_17['상권업종중분류명'].isin(subcategories)]
    open_stores_17_19_in_group = open_stores_17_19[open_stores_17_19['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_category_17) > 0:  # 중분류에 데이터가 있는지 확인
        open_rate_category = len(open_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        print(f"'{group}' 업종의 개업률: {closure_rate_category:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")
        