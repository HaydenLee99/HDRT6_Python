# DB(RDBMS) 연동 관련 Quiz
import MySQLdb
import pickle
import time

# myde.dat 파일 정보
# config = {
#     'host'      : '127.0.0.1', 
#     'user'      : 'root', 
#     'password'  : '123', 
#     'database'  : 'test', 
#     'port'      : 3306,
#     'charset'   : 'utf8'
# }

with open('mydb.dat', mode='rb') as obj:
    config = pickle.load(obj)

def get_connection():
    return MySQLdb.connect(**config)

def Quiz1():
    # jikwon 테이블 자료 출력하라. 키보드로부터 부서번호를 입력받아, 해당 부서에 직원 자료 출력
    # 출력) 부서번호 입력 : _______
    # 출력) 직원번호 직원명 근무지역 직급
    # 출력) 1 홍길동 서울 이사
    # 출력) ...
    # 출력) 인원 수 : __
    try:
        conn = get_connection()
        cursor = conn.cursor()

        bu_no = input('부서번호 입력:')
        # print(bu_no)
        sql =   """select jikwonno as 직원번호, jikwonname as 직원명, buserloc as 근무지역, jikwonjik as 직급 from jikwon
                inner join buser on busernum = buserno
                where busernum=%s"""
        # print(sql)
        cursor.execute(sql, (bu_no,))
        datas = cursor.fetchall()

        if len(datas) == 0:
            print(bu_no+"번 부서는 없습니다.")
            return

        for 직원번호, 직원명, 근무지역, 직급 in datas:
            print(직원번호, 직원명, 근무지역, 직급)

        print('인원 수 : ', len(datas))

    except Exception as e:
        print ('err : ', e)
        # conn.rollback
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def Quiz2():
    # 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
    # 출력) 직원번호 입력 : _______
    # 출력) 직원명 입력 : _______
    # 출력) 직원번호 직원명 부서명 부서전화 직급 성별
    # 출력) 1 홍길동 총무부 111-1111 이사 남
    try:
        conn = get_connection()
        cursor = conn.cursor()
        jik_no = input('직원번호 입력 : ')
        jik_name = input('직원명 입력 : ')
        sql = """
        select         
        jikwonno as 직원번호, 
        jikwonname as 직원명, 
        busername as 부서명, 
        busertel as 부서전화, 
        jikwonjik as 직급, 
        jikwongen as 성별
        from jikwon
        inner join buser on busernum = buserno
        where jikwonno=%s and jikwonname=%s
        """
        cursor.execute(sql, (jik_no, jik_name))
        datas = cursor.fetchall()
        if len(datas) == 0:
            print("로그인 실패.")
            return 
        for 직원번호, 직원명, 부서명, 부서전화, 직급, 성별 in datas:
            print(직원번호, 직원명, 부서명, 부서전화, 직급, 성별)
    except Exception as e:
        print ('err : ', e)
        # conn.rollback
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def Quiz2_1():
    # 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
    # 해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순으로 출력. 직급이 같으면 이름별 오름차순한다.
    # 출력) 직원번호 입력 : _______
    # 출력) 직원명 입력 : _______
    # 출력) 직원번호 직원명 부서명 부서전화 직급 성별
    # 출력) 1 홍길동 총무부 111-1111 이사 남
    # 출력) ...
    # 출력) 직원 수 : 
    # 이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.
    # 출력) 고객번호 고객명 고객전화 나이
    # 출력) 1 사오정 555-5555 34
    # 출력) 관리 고객 수 : 
    try:
        conn = get_connection()
        cursor = conn.cursor()
        jik_no = input('직원번호 입력 : ')
        jik_name = input('직원명 입력 : ')

        sql = """select 
        jikwonno as 직원번호, 
        jikwonname as 직원명, 
        busername as 부서명, 
        busertel as 부서전화, 
        jikwonjik as 직급, 
        jikwongen as 성별
        from jikwon
        inner join buser on busernum = buserno
        where busernum=(select busernum from jikwon where jikwonno=%s and jikwonname=%s)
        order by jikwonjik, jikwonname 
        """
        cursor.execute(sql,(jik_no,jik_name))
        buser_datas = cursor.fetchall()
        if len(buser_datas) == 0:
            print("로그인 실패.")
            return 
        for 직원번호, 직원명, 부서명, 부서전화, 직급, 성별 in buser_datas:
            print(직원번호, 직원명, 부서명, 부서전화, 직급, 성별)
        print('직원 수 : ',len(buser_datas))
        print()

        gogek_sql = """select 
        gogekno as 고객번호, 
        gogekname as 고객명,  
        gogektel as 고객전화, 
        case 
        when substr(gogekjumin, 8, 1) in ('1','2') 
            then year(curdate()) - (1900 + substr(gogekjumin,1,2))
        when substr(gogekjumin, 8, 1) in ('3','4') 
            then year(curdate()) - (2000 + substr(gogekjumin,1,2))
        end as 나이
        from jikwon
        inner join buser on busernum = buserno
        left outer join gogek on jikwonno = gogekdamsano
        where jikwonno=%s and jikwonname=%s
        """
        # print(gogek_sql)
        cursor.execute(gogek_sql,(jik_no,jik_name))
        gogek_datas = cursor.fetchall()
        if len(gogek_datas) == 0:
            print("담당고객 없음.")
            return 
        for 고객번호, 고객명, 고객전화, 나이 in gogek_datas:
            print(고객번호, 고객명, 고객전화, int(나이))
        print('관리 고객 수 : ',len(gogek_datas))

    except Exception as e:
        print ('err : ', e)
        # conn.rollback
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def Quiz3():
    # 성별 직원 현황 출력 : 성별(남/여) 단위로 직원 수와 평균 급여 출력
    # 출력) 성별 직원수 평균급여
    # 출력) 남 3 8500
    # 출력) 여 2 7800

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """select 
        jikwongen as 성별, 
        count(*) as 직원수, 
        avg(jikwonpay) as 평균급여 
        from jikwon
        group by jikwongen
        order by jikwongen 
        """
        cursor.execute(sql)

        for 성별, 직원수, 평균급여 in cursor:
            print(성별, 직원수, int(평균급여))

    except Exception as e:
        print ('err : ', e)
        # conn.rollback
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def Quiz4():
    # 직원별 관리 고객 수 출력 (관리 고객이 없으면 출력에서 제외)
    # 출력) 직원번호 직원명 관리 고객 수
    # 출력) 1 홍길동 3
    # 출력) 2 한송이 1

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """select 
        jikwonno as 직원번호, 
        jikwonname as 직원명, 
        count(*) as '관리 고객 수'
        from jikwon
        inner join gogek on jikwonno = gogekdamsano
        group by jikwonno
        """
        cursor.execute(sql)

        for (직원번호, 직원명, 관리고객수) in cursor:
            print(직원번호, 직원명, 관리고객수)

    except Exception as e:
        print ('err : ', e)
        # conn.rollback
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print('Quiz 1번 실행')
    Quiz1() 
    time.sleep(1)
    print('\nQuiz 2번 실행')
    Quiz2() 
    time.sleep(1)
    print('\nQuiz 2-1번 실행')
    Quiz2_1()
    time.sleep(1)
    print('\nQuiz 3번 실행')
    Quiz3()
    time.sleep(1)
    print('\nQuiz 4번 실행')
    Quiz4()
    time.sleep(1)
    print('\n종료')
