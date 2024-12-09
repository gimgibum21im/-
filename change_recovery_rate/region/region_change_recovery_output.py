import matplotlib.pyplot as plt
import numpy as np
from region_change_recovery_rate import df_analysis

# 결과 출력 - table_change_recovery
#폰트설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False    # 마이너스 기호 깨짐 방지

# 데이터 준비
columns = df_analysis.columns
data = df_analysis.values

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

plt.show()

# 결과 출력 - bar_change_rate
# 막대 폭 설정
bar_width = 0.4

# X축 인덱스 생성
x_indexes = np.arange(len(df_analysis["지역"]))

plt.figure(figsize=(10, 6))
plt.bar(df_analysis["지역"], df_analysis["변화율 (%)"], color="skyblue", alpha=0.8)
plt.title("지역별 업종 합계 변화율 (%)")
plt.xlabel("지역")
plt.ylabel("변화율 (%)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 결과 출력 - bar_change_recovery_rate
# 막대 폭 설정
bar_width = 0.4

# X축 인덱스 생성
x_indexes = np.arange(len(df_analysis["지역"]))

plt.figure(figsize=(12, 6))

# 변화율 막대
plt.bar(
    x_indexes, 
    df_analysis["변화율 (%)"], 
    width=bar_width, 
    color="skyblue", 
    alpha=0.8, 
    label="변화율 (%)"
)

# 회복률 막대
plt.bar(
    x_indexes + bar_width, 
    df_analysis["회복률 (%)"], 
    width=bar_width, 
    color="orange", 
    alpha=0.8, 
    label="회복률 (%)"
)

# 그래프 제목 및 레이블 설정
plt.title("지역별 업종 합계 변화율 및 회복률 (%)")
plt.xlabel("지역")
plt.ylabel("비율 (%)")
plt.xticks(ticks=x_indexes + bar_width / 2, labels=df_analysis["지역"], rotation=45)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 그래프 출력
plt.tight_layout()
plt.show()