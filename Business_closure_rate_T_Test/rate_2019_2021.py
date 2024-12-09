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
data_19 = pd.concat([load_data(201906, region) for region in regions], ignore_index=True)
data_21 = pd.concat([load_data(202106, region) for region in regions], ignore_index=True)

# 전체 대분류 업종 폐업률 및 개업률 초기화
overall_closure_open_rates = {category: {'폐업': 0, '총점포': 0, '개업': 0} for category in categories + ['스포츠/운동']}
detailed_closure_open_rates = []

# 지역별 계산
for region in regions:
    print(f"\n지역: {region}\n{'=' * 20}")

    region_data_19 = data_19[data_19['시도명'] == region]  # 19년도 지역 데이터
    region_data_21 = data_21[data_21['시도명'] == region]  # 21년도 지역 데이터

    closed_stores_in_region = region_data_19[~region_data_19[['상가업소번호']].apply(tuple, axis=1).isin(region_data_21[['상가업소번호']].apply(tuple, axis=1))]
    open_stores_in_region = region_data_21[~region_data_21[['상가업소번호']].apply(tuple, axis=1).isin(region_data_19[['상가업소번호']].apply(tuple, axis=1))]

    for category in categories:
        if category == '관광/여가/오락':
            total_stores_in_category_19 = region_data_19[
                (region_data_19['상권업종대분류명'] == category) & (region_data_19['상권업종중분류명'] != '스포츠/운동')]
            closed_stores_in_category = closed_stores_in_region[
                (closed_stores_in_region['상권업종대분류명'] == category) & (closed_stores_in_region['상권업종중분류명'] != '스포츠/운동')]
            open_stores_in_category = open_stores_in_region[
                (open_stores_in_region['상권업종대분류명'] == category) & (open_stores_in_region['상권업종중분류명'] != '스포츠/운동')]
        else:
            total_stores_in_category_19 = region_data_19[region_data_19['상권업종대분류명'] == category]
            closed_stores_in_category = closed_stores_in_region[closed_stores_in_region['상권업종대분류명'] == category]
            open_stores_in_category = open_stores_in_region[open_stores_in_region['상권업종대분류명'] == category]

        if len(total_stores_in_category_19) > 0:
            closure_rate = len(closed_stores_in_category) / len(total_stores_in_category_19) * 100
            open_rate = len(open_stores_in_category) / len(total_stores_in_category_19) * 100
        else:
            closure_rate = open_rate = None

        detailed_closure_open_rates.append({
            '지역': region,
            '업종': category,
            '폐업률(%)': closure_rate,
            '개업률(%)': open_rate
        })

        # 전체 데이터 업데이트
        overall_closure_open_rates[category]['폐업'] += len(closed_stores_in_category)
        overall_closure_open_rates[category]['총점포'] += len(total_stores_in_category_19)
        overall_closure_open_rates[category]['개업'] += len(open_stores_in_category)

        print(f"{category} 업종 - 폐업률: {closure_rate:.2f}% 개업률: {open_rate:.2f}%" if closure_rate is not None else f"{category} 업종 - 데이터 없음")
    # '스포츠/운동' 업종 추가 계산
    total_stores_in_sports = region_data_19[
        (region_data_19['상권업종중분류명'] == '스포츠/운동') | 
        (region_data_19['상권업종대분류명'] == '스포츠') | 
        (region_data_19['상권업종중분류명'] == '학원-예능취미체육')
    ]

    closed_stores_in_sports = closed_stores_in_region[
        (closed_stores_in_region['상권업종중분류명'] == '스포츠/운동') | 
        (closed_stores_in_region['상권업종대분류명'] == '스포츠') | 
        (closed_stores_in_region['상권업종중분류명'] == '학원-예능취미체육')
    ]

    open_stores_in_sports = open_stores_in_region[
        (open_stores_in_region['상권업종중분류명'] == '스포츠/운동') | 
        (open_stores_in_region['상권업종대분류명'] == '스포츠') | 
        (open_stores_in_region['상권업종중분류명'] == '학원-예능취미체육')
    ]

    if len(total_stores_in_sports) > 0:
        closure_rate = len(closed_stores_in_sports) / len(total_stores_in_sports) * 100
        open_rate = len(open_stores_in_sports) / len(total_stores_in_sports) * 100
    else:
        closure_rate = open_rate = None

    detailed_closure_open_rates.append({
        '지역': region,
        '업종': '스포츠/운동',
        '폐업률(%)': closure_rate,
        '개업률(%)': open_rate
    })

    overall_closure_open_rates['스포츠/운동']['폐업'] += len(closed_stores_in_sports)
    overall_closure_open_rates['스포츠/운동']['총점포'] += len(total_stores_in_sports)
    overall_closure_open_rates['스포츠/운동']['개업'] += len(open_stores_in_sports)

    print(f"스포츠/운동 업종 - 폐업률: {closure_rate:.2f}% 개업률: {open_rate:.2f}%" if closure_rate is not None else f"스포츠/운동 업종 - 데이터 없음")

# 전체 지역 합산 개업/폐업률 계산
overall_rates = []
print("\n전체 지역 합산 데이터\n" + "=" * 20)
for category, values in overall_closure_open_rates.items():
    if values['총점포'] > 0:
        overall_closure_rate = values['폐업'] / values['총점포'] * 100
        overall_open_rate = values['개업'] / values['총점포'] * 100
    else:
        overall_closure_rate = overall_open_rate = None

    overall_rates.append({
        '업종': category,
        '폐업률(%)': overall_closure_rate,
        '개업률(%)': overall_open_rate
    })

    print(f"{category} 업종 - 전체 폐업률: {overall_closure_rate:.2f}% 개업률: {overall_open_rate:.2f}%" if overall_closure_rate is not None else f"{category} 업종 - 데이터 없음")


# 데이터프레임 생성 및 저장
detailed_closure_open_df = pd.DataFrame(detailed_closure_open_rates)
overall_closure_open_df = pd.DataFrame(overall_rates)

detailed_closure_open_df.to_csv('./detailed_closure_open_19_21.csv', index=False)
overall_closure_open_df.to_csv('./overall_closure_open_19_21.csv', index=False)

print("\n지역별 및 전체 대분류 업종 폐업률 및 개업률 데이터가 CSV 파일로 저장되었습니다.")