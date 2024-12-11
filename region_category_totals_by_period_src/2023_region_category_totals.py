import pandas as pd
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# 파일 경로 설정 
file_paths_2023 = {
    "경기": "src/상가업소_202306/202306_경기도.csv",
    "부산": "src/상가업소_202306/202306_부산광역시.csv",
    "서울": "src/상가업소_202306/202306_서울특별시.csv",
    "제주": "src/상가업소_202306/202306_제주특별자치도.csv"
}

# 업종별 대분류 및 중분류 매핑 (2023년 기준)
category_mapping_2023 = {
    "음식": ["음식"],
    "소매": ["소매"],
    "스포츠": ["스포츠 서비스"],
    "오락": ["유원지·오락"],
    "숙박": ["숙박"]
}

# 데이터 병합용 리스트
filtered_data_list_2023 = []

# 파일별 데이터 처리
for region, path in file_paths_2023.items():
    data = pd.read_csv(path, encoding="utf-8")
    
    # 예술·스포츠 대분류 처리
    data["분류"] = data.apply(
        lambda row: next((key for key, values in category_mapping_2023.items()
                          if row["상권업종대분류명"] == "예술·스포츠" and row["상권업종중분류명"] in values), None)
        if row["상권업종대분류명"] == "예술·스포츠"
        else next((key for key, values in category_mapping_2023.items()
                   if row["상권업종대분류명"] in values), None),
        axis=1
    )
    
    # 유효한 업종만 필터링
    filtered_data = data.dropna(subset=["분류"])
    filtered_data_list_2023.append(filtered_data)

# 모든 데이터를 병합
merged_data_2023 = pd.concat(filtered_data_list_2023, ignore_index=True)

# 지역 및 업종별 데이터 집계
region_category_totals_2023 = merged_data_2023.pivot_table(
    index="분류",
    columns="시도명",
    aggfunc="size",
    fill_value=0
)

# 총계 계산
region_category_totals_2023["합계"] = region_category_totals_2023.sum(axis=1)
total_row_2023 = pd.DataFrame(region_category_totals_2023.sum(axis=0)).T
total_row_2023.index = ["합계"]

# 총계 행 추가
region_category_totals_2023 = pd.concat([region_category_totals_2023, total_row_2023])

# 전체 데이터 개수 분의 업종 합계를 계산한 열 추가
total_data_count = region_category_totals_2023.loc["합계", "합계"]
region_category_totals_2023["비율"] = (region_category_totals_2023["합계"] / total_data_count).round(6)


# 결과 출력

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False    # 마이너스 기호 깨짐 방지

# 데이터 준비
columns = region_category_totals_2023.columns
data = region_category_totals_2023.reset_index().values

# 그래프 크기 설정
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis("tight")  # 축 제거
ax.axis("off")    # 축 제거

# 표 생성
table = ax.table(
    cellText=data,
    colLabels=["2023"] + list(columns),
    cellLoc="center",
    loc="center",
    colColours=["#404040"] * (len(columns) + 1)  # 헤더 색상 + ["#f0f0f0"]
)

# 스타일 설정
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(columns) + 1)))  # 컬럼 폭 자동 조정

# 각 행 높이 설정
for (row, col), cell in table.get_celld().items():
    if row == 0:  # 헤더 행
        cell.set_fontsize(12)
        cell.set_height(0.15)  # 헤더 높이
        cell.set_text_props(weight="bold", color="white")  # 헤더 텍스트 스타일
    else:
        cell.set_height(0.1)  # 데이터 행 높이

# 출력
plt.show()
