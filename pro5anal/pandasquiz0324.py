import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import os

config = {
    'host':'127.0.0.1',
    'password':'123',
    'user':'root',
    'database' : 'test',
    'port':3306,
    'charset':'utf8'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql="""
        select 
            jikwonno, jikwonname, busername, jikwonjik, busertel, jikwongen, jikwonpay, 
            gogekno, gogekname, gogektel 
        from jikwon 
        inner join buser on jikwon.busernum=buser.buserno
        left outer join gogek on jikwon.jikwonno=gogek.gogekdamsano
    """
    cursor.execute(sql)
    df_raw = pd.DataFrame(cursor.fetchall(), columns=['사번', '이름', '부서명', '직급', '부서전화', '성별', '연봉', '고객번호', '고객명', '고객전화'])
    df = df_raw.drop_duplicates(subset=['사번'])
    
except pymysql.OperationalError as e:
    print(e)

finally:
    cursor.close()
    conn.close()

# print(df)
# os._exit(0)

# pandas 문제 7)

#  a) MariaDB에 저장된 jikwon, buser, gogek 테이블을 이용하여 아래의 문제에 답하시오.
#    - 사번 이름 부서명 연봉 직급을 읽어 DataFrame을 작성
dfa = df[['사번', '이름', '부서명', '연봉', '직급']]
# print(dfa)

#    - DataFrame의 자료를 파일로 저장
dfa.to_csv('pandas7_a.csv', encoding='utf-8')

#    - 부서명별 연봉의 합, 연봉의 최대/최소값을 출력
dfa_b = dfa.groupby(['부서명'])['연봉']
print("부서명별 연봉의 합 :\n", dfa_b.sum())
print("부서명별 연봉의 최대 \n:", dfa_b.max())
print("부서명별 연봉의 최소 :\n",dfa_b.min())

#    - 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서, 직급))
print(pd.crosstab(dfa['부서명'], dfa['직급']))

# #    - 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력. 담당 고객이 없으면 "담당 고객  X"으로 표시
# dfa_g = df_raw[['사번', '이름', '고객번호', '고객명', '고객전화']].fillna("담당 고객  X")

# dfa_g2 = (dfa_g.groupby(['사번', '이름']).agg({
#                             '고객번호': lambda x: ','.join(map(str,x)),
#                             '고객명': lambda x: ','.join(x),
#                             '고객전화': lambda x: ','.join(x)}).reset_index())
# print(dfa_g2)

#    - 부서명별 연봉의 평균으로 가로 막대 그래프를 작성
plt.barh(dfa_b.mean().index, dfa_b.mean())
plt.show()


#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
#    - pivot_table을 사용하여 성별 연봉의 평균을 출력
dfb_pivot = df.pivot_table(values='연봉', index='성별', aggfunc='mean')
print(dfb_pivot)
#    - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
x=dfb_pivot.index.to_list()
y=dfb_pivot['연봉'].to_list()
plt.bar(x,y)
plt.show()
#    - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))
print(pd.crosstab(df['부서명'], df['성별']))


#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
#   조건 :  try ~ except MySQLdb.OperationalError as e:      사용
#   사번  직원명  부서명   직급  부서전화  성별
#   ...
#   인원수 : * 명
dfc = df[['사번', '이름', '부서명', '직급', '부서전화', '성별', '연봉']]
dfc = dfc.rename(columns={'이름': '직원명'})
# print(dfc)

while True:
    jikwonno = input('사번을 입력하세요. 종료:q\t')
    # jikwonno = 1
    if jikwonno == 'q':
        break
    if not jikwonno.isdigit(): 
        print('사번은 숫자만 입력하세요\n')
        continue

    jikwonname = input('이름을 입력하세요. 종료:q\t')
    # jikwonname = '홍길동'
    if jikwonname == 'q':
        break

    if any(dfc['사번'] == int(jikwonno)):
        name = dfc[dfc['사번'] == int(jikwonno)]['직원명'].iloc[0]
        if name == jikwonname:
            # 전직원 출력
            print(dfc.drop(columns=['연봉'], axis=1))
            print("인원수 : ", dfc['사번'].count(), "명")

            male = dfc[dfc['성별']=='남']['연봉']
            female = dfc[dfc['성별']=='여']['연봉']

            figure, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2)
            figure.set_size_inches(15,10)

            # - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
            sns.boxplot(y=male, ax=ax1)
            sns.boxplot(y=female, ax=ax2)

            ax1.set(xlabel='남성', ylabel='연봉[원]', title='남성 연봉 분포')
            ax2.set(xlabel='여성', ylabel='연봉[원]', title='여성 연봉 분포')

            # - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력
            sns.histplot(data=male, bins=10, ax=ax3)
            sns.histplot(data=female, bins=10, ax=ax4)

            ax3.set(xlabel='연봉[원]', ylabel='인원수[명]', title='남성 연봉 분포 비교')
            ax4.set(xlabel='연봉[원]', ylabel='인원수[명]', title='여성 연봉 분포 비교')

            plt.show()
            break
        else:
            print("사번과 이름 정보가 일치하지 않습니다.\n")
    else: print("존재하지 않는 사번 입니다.\n")


# pandas 문제 8)
# MariaDB에 저장된 jikwon, buser 테이블을 이용하여 아래의 문제에 답하시오.
# Django(Flask) 모듈을 사용하여 결과를 클라이언트 브라우저로 출력하시오.

#    1) 사번, 직원명, 부서명, 직급, 연봉, 근무년수를 DataFrame에 기억 후 출력하시오. (join)
#        : 부서번호, 직원명 순으로 오름 차순 정렬 
#    2) 부서명, 직급 자료를 이용하여  각각 연봉합, 연봉평균을 구하시오.
#    3) 부서명별 연봉합, 평균을 이용하여 세로막대 그래프를 출력하시오.
#    4) 성별, 직급별 빈도표를 출력하시오.
