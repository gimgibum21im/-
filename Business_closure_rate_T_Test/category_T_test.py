import pandas as pd
from scipy.stats import ttest_ind

# 데이터 파일 읽기
data_17_19 = pd.read_csv('./src/detailed_closure_open_17_19.csv')
data_19_21 = pd.read_csv('./src/detailed_closure_open_19_21.csv')

# 분석에 포함할 업종과 지역 추출
categories = data_17_19['업종'].unique()
regions = data_17_19['지역'].unique()

# 분석할 업종 목록
categories = ['소매', '음식', '관광/여가/오락', '숙박', '스포츠/운동']

# 결과 저장 딕셔너리
results = {}

# 각 업종에 대해 지역 데이터를 병합하고 T-검정 수행
for category in categories:
    # 17~19 데이터에서 해당 업종의 폐업률 데이터
    closure_17_19 = data_17_19[data_17_19['업종'] == category]['폐업률(%)']
    print(closure_17_19)
    # 19~21 데이터에서 해당 업종의 폐업률 데이터
    closure_19_21 = data_19_21[data_19_21['업종'] == category]['폐업률(%)']
    print(closure_19_21)
    # T-검정 수행
    t_stat, p_value = ttest_ind(closure_17_19, closure_19_21, equal_var=False)
    
    # 결과 저장
    results[category] = {'t-통계량': t_stat, 'p-값': p_value}

# 결과 출력
for category, result in results.items():
    print(f"\n업종: {category}")
    print(f"t-통계량: {result['t-통계량']:.3f}")
    print(f"p-값: {result['p-값']:.3f}")
    if result['p-값'] < 0.05:
        print(f"⇒ 17-19와 19-21의 {category} 업종 폐업률 간에 통계적으로 유의미한 차이가 있습니다.")
    else:
        print(f"⇒ 17-19와 19-21의 {category} 업종 폐업률 간에 통계적으로 유의미한 차이가 없습니다.")


print("\n" + "=" * 20 + "\n")

# 결과 저장 딕셔너리 (개업률 분석용)
opening_results = {}

# 각 업종에 대해 지역 데이터를 병합하고 T-검정 수행 (개업률)
for category in categories:
    # 17~19 데이터에서 해당 업종의 개업률 데이터
    opening_17_19 = data_17_19[data_17_19['업종'] == category]['개업률(%)']
    
    # 19~21 데이터에서 해당 업종의 개업률 데이터
    opening_19_21 = data_19_21[data_19_21['업종'] == category]['개업률(%)']
    
    # T-검정 수행
    t_stat, p_value = ttest_ind(opening_17_19, opening_19_21, equal_var=False)
    
    # 결과 저장
    opening_results[category] = {'t-통계량': t_stat, 'p-값': p_value}

# 결과 출력
for category, result in opening_results.items():
    print(f"\n업종: {category}")
    print(f"t-통계량: {result['t-통계량']:.3f}")
    print(f"p-값: {result['p-값']:.3f}")
    if result['p-값'] < 0.05:
        print(f"⇒ 17-19와 19-21의 {category} 업종 개업률 간에 통계적으로 유의미한 차이가 있습니다.")
    else:
        print(f"⇒ 17-19와 19-21의 {category} 업종 개업률 간에 통계적으로 유의미한 차이가 없습니다.")
