import matplotlib.pyplot as plt
from category_change_recovery_rate import change_rate_df

#폰트설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False    # 마이너스 기호 깨짐 방지

#결과 출력 - table_change_recovery
# 데이터 준비
columns = change_rate_df.columns
data = change_rate_df.values

# 그래프 크기 설정
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("tight")  # 축 제거
ax.axis("off")  # 축 제거

# 표 생성
table = ax.table(
    cellText=data,
    colLabels=columns,
    cellLoc="center",
    loc="center",
    colColours=["#404040"] * len(columns)  # 헤더 색상
)

# 스타일 설정
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(columns))))  # 컬럼 폭 자동 조정

for (row, col), cell in table.get_celld().items():
    if row == 0:  # 헤더 행
        cell.set_fontsize(12)
        cell.set_height(0.15)  # 헤더 높이
        cell.set_text_props(weight="bold", color="white")  # 헤더 텍스트 스타일
    else:
        cell.set_height(0.1)  # 데이터 행 높이

# 출력
plt.show()

# 시각화 - 변화율 및 회복률
change_rate_df.set_index("업종", inplace=True)
plt.figure(figsize=(12, 6))
bar_width = 0.4
index = range(len(change_rate_df))

# 변화율
plt.bar(index, change_rate_df["변화율 (%)"], bar_width, label="변화율 (%)", color="skyblue", alpha=0.8)

# 회복률
plt.bar(
    [i + bar_width for i in index],
    change_rate_df["회복률 (%)"],
    bar_width,
    label="회복률 (%)",
    color="orange",
    alpha=0.8,
)

# 그래프 설정
plt.title("업종별 변화율 및 회복률 (%)")
plt.ylabel("비율 (%)")
plt.xlabel("업종")
plt.xticks([i + bar_width / 2 for i in index], change_rate_df.index, rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
