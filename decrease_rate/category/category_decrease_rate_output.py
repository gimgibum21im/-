from category_decrease_rate import decrease_rate_df
import matplotlib.pyplot as plt
import numpy as np

#폰트설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False    # 마이너스 기호 깨짐 방지

#결과 출력 - table_decrease_rate
# 데이터 준비
columns = decrease_rate_df.columns
data = decrease_rate_df.values

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


#결과 출력 - bar_decrease_rate
index = np.arange(len(decrease_rate_df["업종"]))
bar_width = 0.4
decrease_rate_df.set_index("업종", inplace=True)
# 감소율
plt.bar(
    index, 
    decrease_rate_df["감소율 (%)"], 
    bar_width, 
    label="감소율 (%)", 
    color="red", 
    alpha=0.8
)

# 그래프 설정
plt.title("업종별 감소율 (%)")
plt.ylabel("감소율 (%)")
plt.xlabel("업종")
plt.xticks(index, decrease_rate_df.index, rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()