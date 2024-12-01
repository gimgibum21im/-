from rate_17_19 import data_17, closed_stores_17_19, open_stores_17_19
from rate_19_21 import data_19, closed_stores_19_21, open_stores_19_21
from scipy.stats import ttest_ind


categories = ['소매', '음식','관광/여가/오락','숙박']

# 17-19 데이터: 업종별 폐업률 정리
closure_rates_17_19 = {}
for category in categories:
    total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
    closed_stores_in_category = closed_stores_17_19[closed_stores_17_19['상권업종대분류명'] == category]
    if len(total_stores_in_category_17) > 0:
        closure_rate = len(closed_stores_in_category) / len(total_stores_in_category_17) * 100
        closure_rates_17_19[category] = closure_rate

# 19-21 데이터: 업종별 폐업률 정리
closure_rates_19_21 = {}
for category in categories:
    total_stores_in_category_19 = data_19[data_19['상권업종대분류명'] == category]
    closed_stores_in_category = closed_stores_19_21[closed_stores_19_21['상권업종대분류명'] == category]
    if len(total_stores_in_category_19) > 0:
        closure_rate = len(closed_stores_in_category) / len(total_stores_in_category_19) * 100
        closure_rates_19_21[category] = closure_rate

# 17-19 데이터: 업종별 개업률 정리
opening_rates_17_19 = {}
for category in categories:
    total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
    open_stores_in_category = open_stores_17_19[open_stores_17_19['상권업종대분류명'] == category]
    if len(total_stores_in_category_17) > 0:
        open_rate = len(open_stores_in_category) / len(total_stores_in_category_17) * 100
        opening_rates_17_19[category] = open_rate

# 19-21 데이터: 업종별 개업률 정리
opening_rates_19_21 = {}
for category in categories:
    total_stores_in_category_19 = data_19[data_19['상권업종대분류명'] == category]
    open_stores_in_category = open_stores_19_21[open_stores_19_21['상권업종대분류명'] == category]
    if len(total_stores_in_category_19) > 0:
        open_rate = len(open_stores_in_category) / len(total_stores_in_category_19) * 100
        opening_rates_19_21[category] = open_rate



# 시기별 폐업률 비교
categories_with_data_closure = set(closure_rates_17_19.keys()) & set(closure_rates_19_21.keys())
closure_data_17_19 = [closure_rates_17_19[cat] for cat in categories_with_data_closure]
closure_data_19_21 = [closure_rates_19_21[cat] for cat in categories_with_data_closure]

t_stat_closure, p_value_closure = ttest_ind(closure_data_17_19, closure_data_19_21, equal_var=False)
print("폐업률 T-검정 결과:")
print("t-통계량:", t_stat_closure)
print("p-값:", p_value_closure)

if p_value_closure < 0.05:
    print("17-19와 19-21의 폐업률 간에 통계적으로 유의미한 차이가 있습니다.")
else:
    print("17-19와 19-21의 폐업률 간에 통계적으로 유의미한 차이가 없습니다.")

# 시기별 개업률 비교
categories_with_data_opening = set(opening_rates_17_19.keys()) & set(opening_rates_19_21.keys())
opening_data_17_19 = [opening_rates_17_19[cat] for cat in categories_with_data_opening]
opening_data_19_21 = [opening_rates_19_21[cat] for cat in categories_with_data_opening]

t_stat_opening, p_value_opening = ttest_ind(opening_data_17_19, opening_data_19_21, equal_var=False)
print("\n개업률 T-검정 결과:")
print("t-통계량:", t_stat_opening)
print("p-값:", p_value_opening)

if p_value_opening < 0.05:
    print("17-19와 19-21의 개업률 간에 통계적으로 유의미한 차이가 있습니다.")
else:
    print("17-19와 19-21의 개업률 간에 통계적으로 유의미한 차이가 없습니다.")
