import os
import pandas as pd

# 청크 크기 설정
chunk_size = 1000000

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
    'src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_01.csv',
    'src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_03.csv',
    'src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_04.csv'
]
data_19_filters = [None, '시도명 == "경기도"', '시도명 == "제주특별자치도"']

# 2017 데이터 파일 경로와 필터
data_17_files = [
    'src/상가업소_201706/상가업소_201706_01.csv',
    'src/상가업소_201706/상가업소_201706_03.csv',
    'src/상가업소_201706/상가업소_201706_04.csv'
]
data_17_filters = [None, '시도명 == "경기도"', '시도명 == "제주특별자치도"']

# 2021 데이터 파일 경로
data_21_files = [
    'src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_경기_202106.csv',
    'src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_부산_202106.csv',
    'src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_서울_202106.csv',
    'src/상가업소_202106/소상공인시장진흥공단_상가(상권)정보_제주_202106.csv'
]

# 2023 데이터 파일 경로
data_23_files = [
    'src/상가업소_202306/소상공인시장진흥공단_상가(상권)정보_경기_202306.csv',
    'src/상가업소_202306/소상공인시장진흥공단_상가(상권)정보_부산_202306.csv',
    'src/상가업소_202306/소상공인시장진흥공단_상가(상권)정보_서울_202306.csv',
    'src/상가업소_202306/소상공인시장진흥공단_상가(상권)정보_제주_202306.csv'
]

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

# 2021 데이터 로드 및 합치기
combined_2021 = load_and_combine_csv(data_21_files, chunk_size)

# 2023 데이터 로드 및 합치기
combined_2023 = load_and_combine_csv(data_23_files, chunk_size)

# 분석에 필요한 column 추출 및 중복 제거
data_19 = combined_2019[['상가업소번호', '상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '시도명', '위도', '경도']].drop_duplicates(subset=['상가업소번호'])
data_17 = combined_2017[['상가업소번호', '상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '시도명', '위도', '경도']].drop_duplicates(subset=['상가업소번호'])
data_21 = combined_2021[['상가업소번호', '상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '시도명', '위도', '경도']].drop_duplicates(subset=['상가업소번호'])
data_23 = combined_2023[['상가업소번호', '상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '시도명', '위도', '경도']].drop_duplicates(subset=['상가업소번호'])

# 지역별로 데이터 필터링 및 저장
def save_by_region(data, year):
    regions = ["경기도", "제주특별자치도", "부산광역시", "서울특별시"]
    folder_path = f"./src/상가업소_{year}"
    os.makedirs(folder_path, exist_ok=True)  # 연도별 폴더 생성
    for region in regions:
        region_data = data[data['시도명'] == region]
        filename = os.path.join(folder_path, f"{year}_{region}.csv")
        region_data.to_csv(filename, index=False, encoding='utf-8-sig')

# 2017, 2019, 2021, 2023 데이터 지역별 저장
save_by_region(data_17, "201706")
save_by_region(data_19, "201906")
save_by_region(data_21, "202106")
save_by_region(data_23, "202306")