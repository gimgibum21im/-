import pandas as pd

# CSV 파일 경로 설정
#file_path = "소상공인시장진흥공단_상가(상권)정보_20240930\소상공인시장진흥공단_상가(상권)정보_경기_202409.csv "  # CSV 파일 이름 또는 경로

#file_path1 = r"BCS\2017\상가업소_201703_01.csv"
file_path2 = r"BCS\2017\상가업소_201703_02.csv"
#file_path3 = r"BCS\2017\상가업소_201703_03.csv"
#file_path4 = r"BCS\2017\상가업소_201703_04.csv"

file_path1 = r"BCS\2019\소상공인시장진흥공단_상가업소정보_201906_01.csv"
#file_path2 = r"BCS\2019\소상공인시장진흥공단_상가업소정보_201906_02.csv"
#file_path3 = r"BCS\2019\소상공인시장진흥공단_상가업소정보_201906_03.csv"
#file_path4 = r"BCS\2019\소상공인시장진흥공단_상가업소정보_201906_04.csv"

# CSV 파일 읽기 2017
#data1 = pd.read_csv(file_path1, dtype=str, encoding='cp949')  # 파일에 맞는 인코딩 지정 
data2 = pd.read_csv(file_path2, dtype=str, encoding='cp949')  # 파일에 맞는 인코딩 지정 
#data3 = pd.read_csv(file_path3, dtype=str, encoding='cp949')  # 파일에 맞는 인코딩 지정 
#data4 = pd.read_csv(file_path4, dtype=str, encoding='cp949')  # 파일에 맞는 인코딩 지정 


# CSV 파일 읽기 2019
data1 = pd.read_csv(file_path1, dtype=str, encoding='utf-8')  # 파일에 맞는 인코딩 지정 
#data2 = pd.read_csv(file_path2, dtype=str, encoding='utf-8')  # 파일에 맞는 인코딩 지정 
#data3 = pd.read_csv(file_path3, dtype=str, encoding='utf-8')  # 파일에 맞는 인코딩 지정 
#data4 = pd.read_csv(file_path4, dtype=str, encoding='utf-8')  # 파일에 맞는 인코딩 지정 

#print(data.head())  # 데이터의 처음 5행 출력
print("###########열 종류###########")
print(data1.columns)
print()
print("###########상권엄종대분류명###########")
print(data1['상권업종대분류명'].drop_duplicates().tolist()) # 중복제거, 특정 열 값 다 가져오기
print()
print("###########상권엄종중분류명###########")
print(data1['상권업종중분류명'].drop_duplicates().tolist()) # 중복제거, 특정 열 값 다 가져오기
print()

all_col_mid2017 = data2['상권업종중분류명'].drop_duplicates().tolist().sort()
all_col_mid2019 = data1['상권업종중분류명'].drop_duplicates().tolist().sort()

print(all_col_mid2017 == all_col_mid2019)


'''
def exist(all_col_mid, k):
    for c in all_col_mid:
        if c == k:
            return True
    return False
def printOut(data):
    all_col_mid = data['상권업종중분류명'].drop_duplicates().tolist()
    #소매
    print("식료품:", exist(all_col_mid, "식료품 소매"))
    print("가전·통신 소매:",exist(all_col_mid, "가전·통신 소매"))
    #음식
    print("한식:", exist(all_col_mid, "한식"))
    print("일식:",exist(all_col_mid, "일식"))
    print("중식:",exist(all_col_mid, "중식"))
    print("기타 간이:",exist(all_col_mid, "기타 간이"))
    print("카페:",exist(all_col_mid, "카페"))

    #여가
    print("스포츠 서비스:",exist(all_col_mid, "스포츠 서비스"))
    print("유원지·오락:",exist(all_col_mid, "유원지·오락"))
    print("#######################################")

printOut(data1)
printOut(data2)
printOut(data3)
printOut(data4)
'''