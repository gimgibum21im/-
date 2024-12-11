# 실행 순서(필수)
1. **프로젝트 최상단에 src 폴더 (src/상가업소_연도/상가 데이터)**  
2. **refactoring 폴더** 내 **comebine_csv.py** 실행
3. **Business_closure_rate_T_Test 폴더** 내 **rate_2017_2019.py/rate_2019_2021.py** 실행


<br/>

# 프로젝트 개요
### 코로나19 팬데믹과 상권 변화 분석

코로나19 팬데믹은 전 세계적으로 경제와 사회 전반에 큰 영향을 미쳤다. 
특히, 비대면 소비 트렌드 확산과 사회적 거리 두기 정책 등으로 오프라인 상권은 큰 변화를 겪게 될 것으로 예상하였다.
팬데믹 전후 상권 변화를 심층적으로 살펴보고, 지역별 및 업종별 감소율, 회복률, 폐업률, 개업률을 도출해 
팬데믹 이후 상권 변화의 양상을 파악하는 것을 목표로 한다.




#### **사용 데이터**
- **소상공인시장진흥공단 상가(상권)정보 데이터**
  - 분석 시기: 2017년 6월, 2019년 6월, 2021년 6월, 2023년 6월
  - 항목: 상호명, 업종 코드, 경도/위도 등
- **보건복지부 코로나19 시도별 발생 현황 API**
  - 확진자 수 데이터 제공


#### **분석 계획**
1. **표본 지역, 업종 선정 및 전처리**
2. **가설 설정**
3. **감소율 및 회복률 분석**
4. **코로나 영향 요인 분석**
6. **결과 검증**


<br/>


# 코드 설명

- **refactoring 폴더**
    - combine_csv.py
        - 상가업소 데이터를 청크 단위로 읽고 결합한 뒤, 필요한 열만 추출하여 중복 제거 후 지역별로 나눠 CSV 파일로 저장함.

<br/>

- **Business_closure_rate_T_Test 폴더**
    - rate_2017_2019.py
        - 2017년과 2019년 사이 주요 지역의 대분류 업종별 폐업률 및 개업률을 계산하고 CSV로 저장함.
    - rate_2019_2021.py
        - 2019년과 2021년 사이 주요 지역의 대분류 업종별 폐업률 및 개업률을 계산하고 CSV로 저장함.
    - Intermediate_rate_2017_2019.py
        - 2017년과 2019년 사이 주요 지역의 중분류(소매, 음식) 업종별 폐업률 및 개업률을 계산함.
    - Intermediate_rate_2019_2021.py
        - 2019년과 2021년 사이 주요 지역의 중분류(소매, 음식) 업종별 폐업률 및 개업률을 계산함.
    - Entire_T_test.py
        - 2017 ~ 2019년과 2019 ~ 2021년의 업종별 폐업률 및 개업률에 대해 T-검정을 수행하여 통계적 차이를 확인함.
    - category_T_test.py
        - 2017 ~ 2019년 사이와 2019년 ~ 2021년 사이 각 업종의 폐업률 및 개업률에 대해 T-검정을 수행하여 통계적으로 유의미한 변화를 검증함.

<br/>

- **change_recovery_rate 폴더**
    - recovery_t_test.py
        - 해당 파일을 실행시키면 **회복률**에 대한 **T-Test 결과**와 **시각화**된 그래프들을 볼 수 있음.
    - bar_sell_ente_extra.py
        - 해당 파일을 실행시키면 **오락**, **소매**에 대한 **분석 결과**와 **시각화**된 그래프를 볼 수 있음.
    - **category 폴더**
        - category_change_recovery_rate.py
            - 업종별 **회복률**, **변화율** 분석 모듈 파일
        - category_change_recovery_rate_output.py
            - category_change_recovery_rate.py 모듈의 결과 출력 파일로 실행하면 **시각화** 된 그래프들을 볼 수 있음.
    - **region 폴더**
        - region_change_recovery_rate.py
            - 지역별 **회복률**, **변화율** 분석 모듈 파일
        - region_change_recovery_output.py
            - region_change_recovery_rate.py 모듈의 결과 출력 파일로 실행하면 **시각화** 된 그래프들을 볼 수 있음.

<br/>

- **decrease_rate 폴더**
    - decrease_t_test.py
        - 해당 파일을 실행시키면 **감소율**에 대한 **T-Test** 결과와 **시각화**된 그래프들을 볼 수 있음.
    - bar_sport_food_extra.py
        - 해당 파일을 실행시키면 **스포츠**, **음식**에 대한 **분석 결과**와 **시각화**된 그래프들을 볼 수 있음.
    - **category 폴더**
        - category_decrease_rate.py
            - 업종별 **감소율** 분석 모듈 파일
        - category_decrease_rate_output.py
            - category_decrease_rate.py 모듈의 결과 출력 파일로 실행하면 **시각화** 된 그래프들을 볼 수 있음.
    - **region 폴더**
        - region_decrease_rate.py
            - 지역별 **감소율** 분석 모듈 파일
            - region_decrease_rate_output.py
                - region_decrease_rate.py 모듈의 결과 출력 파일로 실행하면 **시각화** 된 그래프들을 볼 수 있음.

<br/>

- **region_category_totals_by_period_src 폴더**
    - **소상공인 데이터셋인 csv 파일**에서 표본을 뽑아내는 파일을 모아놓은 폴더로 하위 파일들을 실행시키면 연도별로 **시각화된 표본**을 볼 수 있음.

<br/>

- **covid_correlation 폴더**
    - covid_correlation
        - 2021, 2023년 상가수와 코로나 확진자 수를 기반으로 둘의 상관분석을 진행 한 후 t 검정을 진행하였음.
