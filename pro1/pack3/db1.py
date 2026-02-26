# 개인용 Database : SQLite3 - Python basic module
# https://www.sqlite.org/
# 임베디드 시스템, 모바일 기기 주로 사용
import sqlite3
print(sqlite3.sqlite_version)
conn = sqlite3.connect(':memory:')  # RAM에만 db 저장, 휘발성

try:
    cur = conn.cursor()             # SQL 문 처리를 위한 cursor 객체 생성

    # table 생성
    cur.execute("create table if not exists friends(name text, phone text, addr text)")

    # 자료 입력
    cur.execute("insert into friends values('홍길동','222-2222','서초1동')")
    cur.execute("insert into friends values(?,?,?)",('신기해','333-3333','역삼2동'))
    inputdatas = ('신기한','444-4444','역삼2동')
    cur.execute("insert into friends values(?,?,?)", inputdatas)
    conn.commit()

    # 자료 보기
    cur.execute("select * from friends")
    print(cur.fetchall())               # 모든 record(행) 읽기
    print()
    cur.execute("select name, phone, addr from friends")
    for r in cur:           # cur에 저장되어 있음
        # print(r)
        print(r[0]+' '+r[1]+' '+r[2])
except Exception as e:
    print('err : ',e)
    conn.rollback()
finally:
    conn.close()