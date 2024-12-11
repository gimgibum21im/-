import matplotlib.pyplot as plt
from decrease_t_test import df_2019, df_2021
import numpy as np

# 데이터 준비
selected_industries = ["스포츠", "음식"]
filtered_2019 = df_2019.loc[selected_industries]
filtered_2021 = df_2021.loc[selected_industries]

# 한글 폰트 설정 (Mac OS 기준)
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False  # 마이너스(-) 기호 깨짐 방지

# 스포츠 데이터 시각화
regions = filtered_2019.columns
x = np.arange(len(regions))  # X축 위치
width = 0.35  # 막대 너비

plt.figure(figsize=(10, 6))
plt.bar(x - width / 2, filtered_2019.loc["스포츠"], width, label="2019", alpha=0.8, color="skyblue")
plt.bar(x + width / 2, filtered_2021.loc["스포츠"], width, label="2021", alpha=0.8, color="orange")
plt.title("스포츠 업종 지역별 업종 수 (2019 vs 2021)")
plt.xlabel("지역")
plt.ylabel("업종 수")
plt.xticks(x, regions, rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 음식 데이터 시각화
plt.figure(figsize=(10, 6))
plt.bar(x - width / 2, filtered_2019.loc["음식"], width, label="2019", alpha=0.8, color="skyblue")
plt.bar(x + width / 2, filtered_2021.loc["음식"], width, label="2021", alpha=0.8, color="orange")
plt.title("음식 업종 지역별 업종 수 (2019 vs 2021)")
plt.xlabel("지역")
plt.ylabel("업종 수")
plt.xticks(x, regions, rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
