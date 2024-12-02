import matplotlib.pyplot as plt
import pandas as pd

# 데이터 로드 및 경기도 필터링
data_17 = pd.read_csv('/상가업소_201706_03.csv', encoding='CP949').query('시도명 == "경기도"')
data_19 = pd.read_csv('/소상공인시장진흥공단_상가업소정보_201906_03.csv').query('시도명 == "경기도"')

columns_needed = ['상가업소번호', '위도', '경도']
data_17 = data_17[columns_needed]
data_19 = data_19[columns_needed]

# 폐업, 개업, 유지된 가게 데이터 생성
closed_stores = data_17[~data_17['상가업소번호'].isin(data_19['상가업소번호'])][['위도', '경도']]
open_stores = data_19[~data_19['상가업소번호'].isin(data_17['상가업소번호'])][['위도', '경도']]
active_stores = data_17[data_17['상가업소번호'].isin(data_19['상가업소번호'])][['위도', '경도']]

# 그래프 초기화
plt.figure(figsize=(10, 8))

# 폐업한 가게: 파란색
plt.scatter(closed_stores['경도'], closed_stores['위도'], color='blue', alpha=1, label='폐업한 가게', s=10)
# 개업한 가게: 빨간색
plt.scatter(open_stores['경도'], open_stores['위도'], color='red', alpha=1, label='개업한 가게', s=10)
# 유지된 가게: 검은색
plt.scatter(active_stores['경도'], active_stores['위도'], color='black', alpha=0.3, label='유지된 가게', s=10)

# 그래프 설정
plt.title("경기도 상가업소 상태 (폐업, 개업, 유지)", fontsize=15)
plt.xlabel('경도', fontsize=12)
plt.ylabel('위도', fontsize=12)
plt.legend()

# 그래프 표시
plt.show()