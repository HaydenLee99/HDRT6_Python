import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import csv

def main():
    config = {
        'host':'127.0.0.1',
        'password':'123',
        'user':'root',
        'database' : 'test',
        'port':3306,
        'charset':'utf8'
    }

    try:
        print("\tmain을 실행합니다.\n")
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        sql="""
            select jikwonno, jikwonname, busername, jikwonjik, jikwongen,jikwonpay
            from jikwon inner join buser on jikwon.busernum=buser.buserno
        """
        cursor.execute(sql)
        print("\tdatabase 정보를 읽어왔습니다.")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwongen','jikwonpay'])
        print("\tdatabase 정보를 dataframe 형으로 바꿔 일부 출력합니다.")
        print("\tcursor가 소진되었습니다.")
        print(df1.head(3))
        print('연봉의 총합 : ', df1['jikwonpay'].sum())

        print("csv file i/o run")
        cursor.execute(sql)
        print("\tdatabase 정보를 읽어왔습니다.")
        with open('pandasdb2.csv', mode='w', encoding='utf-8') as fobj:
            writer = csv.writer(fobj)
            for row in cursor.fetchall():
                writer.writerow(row)
        print("\tdatabase 정보를 pandasdb2.csv로 저장했습니다.")
        df2 = pd.read_csv('pandasdb2.csv', header=None, names=['번호','이름','부서','직급','성별','연봉'])
        print("\tpandasdb2.csv를 읽어왔습니다.")
        print(df2.head(3))

        print("pandas의 read_sql 함수 이용")
        df = pd.read_sql(sql, conn)
        df.columns = ['번호','이름','부서','직급','성별','연봉']
        print(df.head(3))
    
        jik_ypay = df.groupby(['직급'])['연봉'].mean()
        # print(jik_ypay)
        plt.pie(jik_ypay, explode=(0,0,0,0,0.1),labels=jik_ypay.index,shadow=True,counterclock=False)
        plt.show()
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        print("\n\tmain을 종료합니다.")

if __name__ == "__main__":
    main()
    