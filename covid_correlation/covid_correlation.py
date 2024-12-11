import pandas as pd
import os
import requests
import xml.etree.ElementTree as ET
from scipy.stats import pearsonr

def load_data(year, region):
    filename = f"./src/상가업소_{year}/{year}_{region}.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        print(f"파일을 찾을 수 없습니다: {filename}")
        return pd.DataFrame()

# 데이터 로드
regions = ['경기도', '서울특별시', '부산광역시', '제주특별자치도']  # 분석할 지역 목록
merged_data_2019 = pd.concat([load_data(201906, region) for region in regions], ignore_index=True)
merged_data_2021 = pd.concat([load_data(202106, region) for region in regions], ignore_index=True)
merged_data_2023 = pd.concat([load_data(202306, region) for region in regions], ignore_index=True)

# API URL
url = "http://apis.data.go.kr/1352000/ODMS_COVID_04/callCovid04Api"

# 조회할 지역과 연도 설정
locations1 = ["부산", "제주", "경기", "서울"]
locations2 = ["부산광역시", "제주특별자치도", "경기도", "서울특별시"]
years = ["2021", "2023"]

# 기본 파라미터 (서비스 키만 고정)
base_params = {
    "serviceKey": "RrWYWh5Xu3V/zMGI/LHAzuwp96e7Qb87SrmVGq1jGGp7UebO+BD8JQuTaD4sxngSt3P3hfKPN5gjkgzXYXKBsQ==",
    "type": "xml",  # JSON 응답 요청
}

# 결과를 저장할 리스트
results = []

# 데이터 조회
for year in years:
    for location in locations１:
        # 연도와 지역에 따라 파라미터 동적으로 설정
        
        params = base_params.copy()
        params.update({"std_day": f"{year}-06-01", "gubun": location})

        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                defCnt = root.find('.//defCnt').text
                if defCnt is None or not defCnt.isdigit():
                    defCnt = 0  # 데이터가 없거나 잘못된 경우 기본값 0 설정
                else:
                    defCnt = int(defCnt)
            except Exception as e:
                defCnt = 0  # 오류 발생 시 기본값 0 설정
                print(f"오류 발생: {e}")

            # 결과를 리스트에 저장
            results.append({"year": year, "location": location, "cases": defCnt})
        else:
            print(f"{year}년 {location} 데이터 조회 중 오류 발생: {response.status_code}")

# 결과 출력 (옵션)
covid_df = pd.DataFrame(results)

# 각 연도별 상가업소 수 변화 (예: 2019-2021, 2021-2023)
# 상가업소 수 데이터에서 각 시도별로 2019, 2021, 2023 데이터를 필터링
business_changes = []

# 각 연도의 상가업소 수를 추출하고 변화량 계산

for location in locations２:
    # 예: 경기
    business_2019 = merged_data_2019[merged_data_2019['시도명']== location].shape[0]
    business_2021 = merged_data_2021[merged_data_2021['시도명']== location].shape[0]
    business_2023 = merged_data_2023[merged_data_2023['시도명']== location].shape[0]

    change_19_21 = business_2021 - business_2019
    change_21_23 = business_2023 - business_2021


    business_changes.append({
        "location": location,
        "change_19_21": change_19_21,
        "change_21_23": change_21_23
    })

# # 비즈니스 변화 데이터를 DataFrame으로 변환
business_df = pd.DataFrame(business_changes)
# 상관 분석 준비
covid_cases_list = []
business_change_list = []

for year in years:
    for location in locations２:
        # 코로나 확진자 수 가져오기
    
        covid_cases = covid_df[(covid_df['year'] == year) & (covid_df['location'] == location[0:2])]['cases'].values
        if len(covid_cases) == 0:
            covid_case=0  # 데이터가 없으면 스킵
        covid_cases = int(covid_cases[0])  # 리스트에서 값 추출 후 정수 변환
        
        # 상가업소 변화량 가져오기
        if year == "2021":
            business_change = business_df[business_df['location'] == location]['change_19_21'].values
        elif year == "2023":
            business_change = business_df[business_df['location'] == location]['change_21_23'].values
        else:
            continue

        if len(business_change) == 0:
            continue  # 데이터가 없으면 스킵
        business_change = int(business_change[0])  # 리스트에서 값 추출 후 정수 변환
        
        # 리스트에 값 추가
        covid_cases_list.append(covid_cases)
        business_change_list.append(business_change)
print("\n==========\n")
print ("covid_cases_list:", covid_cases_list)
print ("business_change_list: ",business_change_list)
# 최종 상관분석
correlation, p_value = pearsonr(covid_cases_list, business_change_list)
print("\n==========\n")
# 결과 출력
if len(covid_cases_list) > 1 and len(business_change_list) > 1:
    correlation, p_value = pearsonr(covid_cases_list, business_change_list)
    print(f"상관 분석 결과 (상관 계수): {correlation}")
else:
    print("상관 분석을 위한 데이터가 충분하지 않습니다.")
print("\n==========\n")
print(f"p-value: {p_value} \n")

# p-value로 유의성 판단
if p_value < 0.05:
    print("상관 관계는 통계적으로 유의미합니다.")
else:
    print("상관 관계는 통계적으로 유의미하지 않습니다.")
