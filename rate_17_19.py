import pandas as pd
from tabulate import tabulate
import time

# 청크 크기 설정
chunk_size = 1000000

start = time.time()

# 파일별로 데이터를 청크 단위로 읽고 합치기
def load_and_combine_csv(file_paths, chunk_size, region_filter=None):
    combined_data = []
    for file_path in file_paths:
        # 청크 단위로 읽기
        chunk_iter = pd.read_csv(file_path, chunksize=chunk_size, encoding='CP949' if '2017' in file_path else None)
        for chunk in chunk_iter:
            # 특정 지역 필터링이 필요한 경우 처리
            if region_filter:
                chunk = chunk.query(region_filter)
            combined_data.append(chunk)
    # 데이터 프레임으로 합치기
    return pd.concat(combined_data, ignore_index=True)

# 2019 데이터 파일 경로와 필터
data_19_files = [
    '2019/소상공인시장진흥공단_상가업소정보_201906_01.csv',
    '2019/소상공인시장진흥공단_상가업소정보_201906_03.csv',
    '2019/소상공인시장진흥공단_상가업소정보_201906_04.csv'
]
data_19_filters = [None, '시도명 == "경기도"', '시도명 == "제주특별자치도"']

# 2017 데이터 파일 경로와 필터
data_17_files = [
    '2017/상가업소_201706_01.csv',
    '2017/상가업소_201706_03.csv',
    '2017/상가업소_201706_04.csv'
]
data_17_filters = [None, '시도명 == "경기도"', '시도명 == "제주특별자치도"']

# 2019 데이터 로드 및 합치기
combined_2019_chunks = [
    load_and_combine_csv([file], chunk_size, region_filter)
    for file, region_filter in zip(data_19_files, data_19_filters)
]
combined_2019 = pd.concat(combined_2019_chunks, ignore_index=True)

# 2017 데이터 로드 및 합치기
combined_2017_chunks = [
    load_and_combine_csv([file], chunk_size, region_filter)
    for file, region_filter in zip(data_17_files, data_17_filters)
]
combined_2017 = pd.concat(combined_2017_chunks, ignore_index=True)

end = time.time()
print('Chunk 병합에 소요되는 시간 : ', (end - start) ,'sec')

# 분석에 필요한 column 추출
data_19=combined_2019[['상가업소번호','상호명','지점명','상권업종대분류명','상권업종중분류명','시도명']] 
data_17=combined_2017[['상가업소번호','상호명','지점명','상권업종대분류명','상권업종중분류명','시도명']] 
# 데이터 내 중복 제거
data_17 = data_17.drop_duplicates(subset=['상가업소번호'])
data_19 = data_19.drop_duplicates(subset=['상가업소번호'])

## print(data_17.상권업종대분류명.unique())

categories = ['소매', '음식','관광/여가/오락','숙박']

# 폐업률 차집함 구하는 코드
closed_stores_17_19 = data_17[~data_17[['상가업소번호']].apply(tuple, axis=1).isin(data_19[['상가업소번호']].apply(tuple, axis=1))] 

print("폐업한 가계수: ", len(closed_stores_17_19))
closed_rate=len(closed_stores_17_19)/len(data_17)*100
print(f"폐업률: {closed_rate:.2f}%")
print("\n=====\n")

# 대분류별 폐업률
# 각 대분류별 폐업률 계산
for category in categories:
    if category=='관광/여가/오락':
        total_stores_in_category_17 = data_17[(data_17['상권업종대분류명'] == category) & (data_17['상권업종중분류명'] != '스포츠/운동')]
        closed_stores_17_19_in_category = closed_stores_17_19[(closed_stores_17_19['상권업종대분류명'] == category) & (closed_stores_17_19['상권업종중분류명'] != '스포츠/운동')]
    
    else:
        total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
        closed_stores_17_19_in_category = closed_stores_17_19[closed_stores_17_19['상권업종대분류명'] == category]
    
    if len(total_stores_in_category_17) > 0:  # 대분류에 데이터가 있는지 확인
        closure_rate_category = len(closed_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        print(f"'{category}' 업종의 폐업률: {closure_rate_category:.2f}%")
    else:
        print(f"'{category}' 업종에 대한 데이터가 없습니다.")

total_stores_in_category_17 = data_17[(data_17['상권업종중분류명'] =='스포츠/운동') | (data_17['상권업종중분류명']=='학원-예능취미체육')]
closed_stores_17_19_in_category = closed_stores_17_19[(closed_stores_17_19['상권업종중분류명'] == '스포츠/운동') | (closed_stores_17_19['상권업종중분류명']=='학원-예능취미체육')]
    
if len(total_stores_in_category_17) > 0:  # 대분류에 데이터가 있는지 확인
    closure_rate_category = len(closed_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
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
    total_stores_in_group = data_17[data_17['상권업종중분류명'].isin(subcategories)]
    closed_stores_17_19_in_group = closed_stores_17_19[closed_stores_17_19['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_group) > 0:  # 중분류에 데이터가 있는지 확인
        closure_rate_group = len(closed_stores_17_19_in_group) / len(total_stores_in_group) * 100
        print(f"'{group}' 업종의 폐업률: {closure_rate_group:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")





# 개업률
open_stores_17_19 = data_19[~data_19[['상가업소번호']].apply(tuple, axis=1).isin(data_17[['상가업소번호']].apply(tuple, axis=1))]
print("개업한 가계수: ", len(open_stores_17_19))
open_rate=len(open_stores_17_19)/len(data_17)*100
print(f"개업률: {open_rate:.2f}%")
print("\n=====\n")


# 각 대분류별 개업률 계산
for category in categories:
    if category=='관광/여가/오락':
        total_stores_in_category_17 = data_17[(data_17['상권업종대분류명'] == category) & (data_17['상권업종중분류명'] != '스포츠/운동')]
        open_stores_17_19_in_category = open_stores_17_19[(open_stores_17_19['상권업종대분류명'] == category) & (open_stores_17_19['상권업종중분류명'] != '스포츠/운동')]
    
    else:
        total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
        open_stores_17_19_in_category = open_stores_17_19[open_stores_17_19['상권업종대분류명'] == category]
    
    if len(total_stores_in_category_17) > 0:  # 대분류에 데이터가 있는지 확인
        open_rate_category = len(open_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        print(f"'{category}' 업종의 개업률: {open_rate_category:.2f}%")
    else:
        print(f"'{category}' 업종에 대한 데이터가 없습니다.")

total_stores_in_category_17 = data_17[(data_17['상권업종중분류명'] =='스포츠/운동') | (data_17['상권업종중분류명']=='학원-예능취미체육')]
open_stores_17_19_in_category = open_stores_17_19[(open_stores_17_19['상권업종중분류명'] == '스포츠/운동') | (open_stores_17_19['상권업종중분류명']=='학원-예능취미체육')]
    
if len(total_stores_in_category_17) > 0:  # 대분류에 데이터가 있는지 확인
    open_rate_category = len(open_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
    print(f"'스포츠/운동' 업종의 개업률: {open_rate_category:.2f}%")
else:
    print(f"'스포츠/운동' 업종에 대한 데이터가 없습니다.")

print("\n=====\n")


# 각 중분류별 개업률 계산
for group, subcategories in group_mapping.items():
    total_stores_in_group = data_17[data_17['상권업종중분류명'].isin(subcategories)]
    open_stores_17_19_in_group = open_stores_17_19[open_stores_17_19['상권업종중분류명'].isin(subcategories)]
    
    
    if len(total_stores_in_group) > 0:  # 중분류에 데이터가 있는지 확인
        open_rate_group = len(open_stores_17_19_in_group) / len(total_stores_in_group) * 100
        print(f"'{group}' 업종의 개업률: {open_rate_group:.2f}%")
    else:
        print(f"'{group}' 업종에 대한 데이터가 없습니다.")
print("\n=====\n")




closure_open_rates = []

# 대분류별 폐업률 및 개업률 계산
for category in categories:
    if category == '관광/여가/오락':
        total_stores_in_category_17 = data_17[(data_17['상권업종대분류명'] == category) & (data_17['상권업종중분류명'] != '스포츠/운동')]
        closed_stores_17_19_in_category = closed_stores_17_19[(closed_stores_17_19['상권업종대분류명'] == category) & (closed_stores_17_19['상권업종중분류명'] != '스포츠/운동')]
        open_stores_17_19_in_category = open_stores_17_19[(open_stores_17_19['상권업종대분류명'] == category) & (open_stores_17_19['상권업종중분류명'] != '스포츠/운동')]
    else:
        total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
        closed_stores_17_19_in_category = closed_stores_17_19[closed_stores_17_19['상권업종대분류명'] == category]
        open_stores_17_19_in_category = open_stores_17_19[open_stores_17_19['상권업종대분류명'] == category]

    if len(total_stores_in_category_17) > 0:
        closure_rate = len(closed_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
        open_rate = len(open_stores_17_19_in_category) / len(total_stores_in_category_17) * 100
    else:
        closure_rate = open_rate = None

    closure_open_rates.append({'업종': category, '폐업률(%)': closure_rate, '개업률(%)': open_rate})

# 추가적으로 '스포츠/운동' 업종에 대해 계산
total_stores_in_sports = data_17[(data_17['상권업종중분류명'] == '스포츠/운동') | (data_17['상권업종중분류명'] == '학원-예능취미체육')]
closed_stores_in_sports = closed_stores_17_19[(closed_stores_17_19['상권업종중분류명'] == '스포츠/운동') | (closed_stores_17_19['상권업종중분류명'] == '학원-예능취미체육')]
open_stores_in_sports = open_stores_17_19[(open_stores_17_19['상권업종중분류명'] == '스포츠/운동') | (open_stores_17_19['상권업종중분류명'] == '학원-예능취미체육')]

if len(total_stores_in_sports) > 0:
    closure_rate = len(closed_stores_in_sports) / len(total_stores_in_sports) * 100
    open_rate = len(open_stores_in_sports) / len(total_stores_in_sports) * 100
else:
    closure_rate = open_rate = None

closure_open_rates.append({'업종': '스포츠/운동', '폐업률(%)': closure_rate, '개업률(%)': open_rate})

# 데이터프레임 생성 및 출력
closure_open_df = pd.DataFrame(closure_open_rates)
closure_open_df.to_csv('./closure_open_17_19.csv')