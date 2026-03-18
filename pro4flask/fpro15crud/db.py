import pymysql
import os

# MariaDB 연결 정보
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PWD = os.getenv("DB_PWD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_connFunc():
    return pymysql.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PWD,
        database = DB_NAME,
        charset = "utf8mb4",                            # utf8mb4 : 전세계 문자 + 이모지 처리 가능
        cursorclass = pymysql.cursors.DictCursor,       # Dictcursor : select 결과를 "dict type" 형태로 받게 해줌
        autocommit = True
    )
