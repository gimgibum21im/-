import pandas as pd

# 데이터 준비
region_data_2019 = {
    "지역": ["경기도", "부산광역시", "서울특별시", "제주특별자치도"],
    "합계": [442393, 112504, 272907, 34908]
}

region_data_2023 = {
    "지역": ["경기도", "부산광역시", "서울특별시", "제주특별자치도"],
    "합계": [351562, 102035, 269941, 40109]
}

# 데이터프레임 생성
df_2019 = pd.DataFrame(region_data_2019)
df_2023 = pd.DataFrame(region_data_2023)

# 변화율 계산
change_rate = ((df_2023["합계"] - df_2019["합계"]) / df_2019["합계"] * 100).round(2)

# 회복률 계산
recovery_rate = (df_2023["합계"] / df_2019["합계"] * 100).round(2)

# 데이터프레임 생성
df_analysis = pd.DataFrame({
    "지역": df_2019["지역"],
    "2019 합계": df_2019["합계"],
    "2023 합계": df_2023["합계"],
    "변화율 (%)": change_rate,
    "회복률 (%)": recovery_rate
})