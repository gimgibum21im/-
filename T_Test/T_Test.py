import pandas as pd
from scipy.stats import ttest_ind

# 파일에서 데이터 불러오기
data_17_19 = pd.read_csv('overall_closure_open_17_19.csv')
data_19_21 = pd.read_csv('overall_closure_open_19_21.csv')  # 19~21 데이터를 담고 있는 파일명

# 카테고리 목록
categories = ['소매', '음식', '관광/여가/오락', '숙박', '스포츠/운동']

# 폐업률 데이터 정리
closure_rates_17_19 = {row['업종']: row['폐업률(%)'] for _, row in data_17_19.iterrows() if row['업종'] in categories}
closure_rates_19_21 = {row['업종']: row['폐업률(%)'] for _, row in data_19_21.iterrows() if row['업종'] in categories}

# 개업률 데이터 정리
opening_rates_17_19 = {row['업종']: row['개업률(%)'] for _, row in data_17_19.iterrows() if row['업종'] in categories}
opening_rates_19_21 = {row['업종']: row['개업률(%)'] for _, row in data_19_21.iterrows() if row['업종'] in categories}

# T-검정을 위한 데이터 준비: 폐업률
categories_with_data_closure = set(closure_rates_17_19.keys()) & set(closure_rates_19_21.keys())
closure_data_17_19 = [closure_rates_17_19[cat] for cat in categories_with_data_closure]
closure_data_19_21 = [closure_rates_19_21[cat] for cat in categories_with_data_closure]

# T-검정: 폐업률
t_stat_closure, p_value_closure = ttest_ind(closure_data_17_19, closure_data_19_21, equal_var=False)
print("폐업률 T-검정 결과:")
print("t-통계량:", t_stat_closure)
print("p-값:", p_value_closure)

if p_value_closure < 0.05:
    print("17-19와 19-21의 폐업률 간에 통계적으로 유의미한 차이가 있습니다.")
else:
    print("17-19와 19-21의 폐업률 간에 통계적으로 유의미한 차이가 없습니다.")

# T-검정을 위한 데이터 준비: 개업률
categories_with_data_opening = set(opening_rates_17_19.keys()) & set(opening_rates_19_21.keys())
opening_data_17_19 = [opening_rates_17_19[cat] for cat in categories_with_data_opening]
opening_data_19_21 = [opening_rates_19_21[cat] for cat in categories_with_data_opening]

# T-검정: 개업률
t_stat_opening, p_value_opening = ttest_ind(opening_data_17_19, opening_data_19_21, equal_var=False)
print("\n개업률 T-검정 결과:")
print("t-통계량:", t_stat_opening)
print("p-값:", p_value_opening)

if p_value_opening < 0.05:
    print("17-19와 19-21의 개업률 간에 통계적으로 유의미한 차이가 있습니다.")
else:
    print("17-19와 19-21의 개업률 간에 통계적으로 유의미한 차이가 없습니다.")