from scipy.stats import ttest_1samp
import pandas as pd
import matplotlib.pyplot as plt

#폰트설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False    # 마이너스 기호 깨짐 방지

# 데이터 준비
data_2019 = {
    "업종": ["소매", "숙박", "스포츠", "오락", "음식"],
    "경기도": [205799, 6385, 4362, 19123, 206724],
    "부산광역시": [52808, 2193, 790, 4685, 52028],
    "서울특별자치도": [124782, 3047, 1846, 11545, 131687],
    "제주특별자치도": [13307, 2826, 286, 893, 17596]
}

data_2021 = {
    "업종": ["소매", "숙박", "스포츠", "오락", "음식"],
    "경기도": [158674, 5503, 5530, 11080, 183836],
    "부산광역시": [44740, 1665, 1290, 2832, 49866],
    "서울특별자치도": [89857, 2322, 2516, 6603, 126203],
    "제주특별자치도": [12369, 2859, 387, 757, 20178]
}

# 데이터프레임 생성
df_2019 = pd.DataFrame(data_2019).set_index("업종")
df_2021 = pd.DataFrame(data_2021).set_index("업종")

# 감소율 계산
decrease_rate = ((df_2019 - df_2021) / df_2019 * 100).round(2)

# 기준값 설정 (5%)
benchmark = 5

if __name__ == '__main__':
    # 업종별 T-검정 수행
    t_test_results_by_category = []
    for category, row in decrease_rate.iterrows():
        numeric_data = row.astype(float)
        t_stat, p_value = ttest_1samp(numeric_data, benchmark)
        p_value_one_tailed = p_value / 2 if t_stat > 0 else 1 - (p_value / 2)
        t_test_results_by_category.append([
            category,
            round(t_stat, 4),
            round(p_value_one_tailed, 6),
            "귀무가설 기각 (평균 감소율이 5%보다 큼)" if p_value_one_tailed < 0.05 else "귀무가설 채택 (평균 감소율이 5%보다 크다고 볼 수 없음)"
        ])

    # 지역별 T-검정 수행
    t_test_results_by_region = []
    for region in df_2019.columns:
        t_stat, p_value = ttest_1samp(decrease_rate[region], benchmark)
        p_value_one_tailed = p_value / 2 if t_stat > 0 else 1 - (p_value / 2)
        t_test_results_by_region.append([
            region,
            round(t_stat, 4),
            round(p_value_one_tailed, 6),
            "귀무가설 기각 (평균 감소율이 5%보다 큼)" if p_value_one_tailed < 0.05 else "귀무가설 채택 (평균 감소율이 5%보다 크다고 볼 수 없음)"
        ])

    # 결과 출력
    def plot_table(data, title, col_labels, cell_height=0.1, header_height=0.15):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.axis("tight")  # 축 제거
        ax.axis("off")

        # 테이블 생성
        table = ax.table(
            cellText=data,
            colLabels=col_labels,
            cellLoc="center",
            loc="center",
            colColours=["#404040"] * 4  # 헤더 색상
        )
        # 스타일 설정
        table.auto_set_font_size(False)
        table.auto_set_column_width(col=list(range(5)))  # 컬럼 폭 자동 조정

        # 셀 크기 조정
        for i, cell in table.get_celld().items():
            row, col = i
            if row == 0:  # 헤더 행
                cell.set_height(header_height)
                cell.set_fontsize(12)
                cell.set_text_props(weight="bold")
            else:  # 데이터 행
                cell.set_height(cell_height)
                cell.set_fontsize(10)

        # 제목 추가
        ax.set_title(title, fontsize=16, pad=20)
        plt.show()

    # 업종별 결과 출력
    plot_table(
        t_test_results_by_category,
        "업종별 감소율 T-검정 결과",
        ["업종", "T-통계량", "p-value (단측)", "검정결과"],
    )

    # 지역별 결과 출력
    plot_table(
        t_test_results_by_region,
        "지역별 감소율 T-검정 결과",
        ["지역", "T-통계량", "p-value (단측)", "검정결과"],
    )