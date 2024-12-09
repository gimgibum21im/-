import pandas as pd
import matplotlib.pyplot as plt


busan_19 = pd.read_csv('C:/Users/김유정/대학/2024-2/전통/기말프로젝트/소상공인시장진흥공단_상가업소정보_201906/소상공인시장진흥공단_상가업소정보_201906_01.csv')
# print(busan_19.상권업종대분류명.unique())
data_19=busan_19[['상가업소번호','상호명','지점명','상권업종대분류명','시도명']] 
busan_17 = pd.read_csv('C:/Users/김유정/대학/2024-2/전통/기말프로젝트/상가업소_201706/상가업소_201706_01.csv', encoding='CP949')
# print(busan_17.상권업종대분류명.unique())

# 분석에 필요한 column 추출?
data_17=busan_17[['상가업소번호','상호명','지점명','상권업종대분류명','시도명']] 
print(data_17)

# 차집함 구하는 코드
closed_stores = data_17[~data_17[['상가업소번호']].apply(tuple, axis=1).isin(data_19[['상가업소번호']].apply(tuple, axis=1))] 
print(len(closed_stores))
closed_rate=len(closed_stores)/len(data_17)*100
print(f"폐업률: {closed_rate:.2f}%")

open_stores = data_19[~data_19[['상가업소번호']].apply(tuple, axis=1).isin(data_17[['상가업소번호']].apply(tuple, axis=1))]
print(len(open_stores))
open_rate=len(open_stores)/len(data_17)*100
print(f"개업률: {open_rate:.2f}%")

# #대분류별 폐업률
# closure_rate_by_category = closed_stores['상권업종대분류명'].value_counts() / data_17['상권업종대분류명'].value_counts() * 100
# print("카테고리별 폐업률:")
# print(closure_rate_by_category)

# 업종별 폐업률 계산
closed_rate_by_category = closed_stores['상권업종대분류명'].value_counts() / data_17['상권업종대분류명'].value_counts() * 100

# 시각화
closed_rate_by_category.sort_values().plot(kind='bar', color='skyblue', figsize=(10, 6))
plt.title('업종별 폐업률 (2017~2019)', fontsize=15)
plt.ylabel('폐업률 (%)', fontsize=12)
plt.xlabel('업종 대분류', fontsize=12)
plt.xticks(rotation=45)
plt.show()


