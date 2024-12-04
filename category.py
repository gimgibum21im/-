from rate_17_19 import data_17, closed_stores_17_19, open_stores_17_19
from rate_19_21 import data_19, closed_stores_19_21, open_stores_19_21
from scipy.stats import ttest_ind


categories = ['소매', '음식','관광/여가/오락','숙박']
target_regions = ['경기도', '제주특별자치도', '부산광역시', '서울']

# 17-19 데이터: 지역별 폐업률 정리
closure_rates_by_region_17_19 = {}
for category in categories:
    closure_rates_by_region_17_19[category] = {}
    total_stores_in_category_17 = data_17[data_17['상권업종대분류명'] == category]
    for region in target_regions:
        total_stores_in_region = total_stores_in_category_17[total_stores_in_category_17['지역명'] == region]
        closed_stores_in_region = closed_stores_17_19[
            (closed_stores_17_19['상권업종대분류명'] == category) &
            (closed_stores_17_19['지역명'] == region)
        ]
        if len(total_stores_in_region) > 0:
            closure_rate = len(closed_stores_in_region) / len(total_stores_in_region) * 100
            closure_rates_by_region_17_19[category][region] = closure_rate

# 19-21 데이터: 지역별 폐업률 정리
closure_rates_by_region_19_21 = {}
for category in categories:
    closure_rates_by_region_19_21[category] = {}
    total_stores_in_category_19 = data_19[data_19['상권업종대분류명'] == category]
    for region in target_regions:
        total_stores_in_region = total_stores_in_category_19[total_stores_in_category_19['지역명'] == region]
        closed_stores_in_region = closed_stores_19_21[
            (closed_stores_19_21['상권업종대분류명'] == category) &
            (closed_stores_19_21['지역명'] == region)
        ]
        if len(total_stores_in_region) > 0:
            closure_rate = len(closed_stores_in_region) / len(total_stores_in_region) * 100
            closure_rates_by_region_19_21[category][region] = closure_rate

# 업종별로 지역별 폐업률 비교
for category in categories:
    regions_with_data = set(closure_rates_by_region_17_19.get(category, {}).keys()) & \
                        set(closure_rates_by_region_19_21.get(category, {}).keys())
    closure_data_17_19 = [closure_rates_by_region_17_19[category][region] for region in regions_with_data]
    closure_data_19_21 = [closure_rates_by_region_19_21[category][region] for region in regions_with_data]

    if closure_data_17_19 and closure_data_19_21:  # 데이터가 존재하는 경우만 비교
        t_stat_closure, p_value_closure = ttest_ind(closure_data_17_19, closure_data_19_21, equal_var=False)
        print(f"\n[{category}] 폐업률 T-검정 결과:")
        print("t-통계량:", t_stat_closure)
        print("p-값:", p_value_closure)

        if p_value_closure < 0.05:
            print(f"{category}의 17-19와 19-21의 폐업률 간에 통계적으로 유의미한 차이가 있습니다.")
        else:
            print(f"{category}의 17-19와 19-21의 폐업률 간에 통계적으로 유의미한 차이가 없습니다.")
