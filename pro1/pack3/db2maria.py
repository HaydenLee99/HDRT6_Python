# Remote Database 연동 프로그래밍
# MariaDB : driver file 설치 후 사용
# pip install mysqlclient
import MySQLdb
'''
conn = MySQLdb.connect(
    host='127.0.0.1', 
    user='root', 
    password='123', 
    database='test', 
    port=3306)

print(conn)

conn.close()
'''
# sangdata 자료 CRUD
config = {
    'host'      : '127.0.0.1', 
    'user'      : 'root', 
    'password'  : '123', 
    'database'  : 'test', 
    'port'      : 3306,
    'charset'   : 'utf8'
}

def myFunc():
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        # 자료 추가 INSERT
        # isql = "insert into sangdata(code, sang, su, dan) values(5,'신상1', 5, 7800)"
        # cursor.execute(isql)
        # conn.commit()
        # isql = "insert into sangdata values(%s,%s,%s,%s)"
        # sql_data = (6,'신상2', 11, 5000)
        # cursor.execute(isql, sql_data)
        # conn.commit()

        # 자료 수정
        # usql = "update sangdata set sang=%s, su=%s, dan=%s where code=%s"
        # sql_data = ('물티슈', 66, 1000, 5)
        # cursor.execute(usql, sql_data)
        # conn.commit()
        # sql_data = ('콜라', 77, 1000, 5)
        # cou = cursor.execute(usql, sql_data)
        # print('수정 건수 : ',cou)                   
        # INSERT: 성공 1 / 실패 0
        # UPDATE: 성공(수정행 수) 1 이상 / 실패 0
        # DELETE: 성공(삭제행 수) 1 이상 / 실패 0
        # conn.commit()

        # 자료 삭제 DELETE
        code = '6'
        # dsql = "delete from sangdata where code=" + code    # 문자열 더하기로 SQL문 완성은 secure coding 가이드라인 위배, SQL Injection
        dsql = "delete from sangdata where code=%s"
        cou = cursor.execute(dsql,(code,))                       # tuple로 합치는게 제일 안전함
        conn.commit()                                  # 삭제 후 반환값 얻기
        if cou != 0:
            print('삭제 성공')
        else:
            print('삭제 실패')
            
        # 자료 읽기 SELECT
        sql = "select code, sang, su, dan from sangdata"
        cursor.execute(sql)
        # for data in cursor.fetchall():
        #     print('%s %s %s %s'%data)
        # print()
        # for r in cursor:
        #     print(r[0], r[1], r[2], r[3])
        # print()
        for 코드, 상품, 수량, 단가 in cursor:
            print(코드, 상품, 수량, 단가)
        
    except Exception as e:
        print('err : ', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    myFunc() 
