from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
# flash : 임시 메시지 출력용 (내부적으로 session 저장해 둠)
# get_flashed_messages : 세션에 저장해둔 휘발성 메시지를 꺼내는 함수
import pymysql
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = "ad12ef1@!aa210"         # session/flash를 위한 쿠키 서명용 암호

load_dotenv()                             # .env 파일에 저장된 환경변수 읽기 함수

# MariaDB 연결 정보
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_NAME = os.getenv("DB_NAME")

def get_conn():
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

@app.get("/")
def root():
    return redirect(url_for("login_form"))

@app.get("/login")
def login_form():
    return render_template("login.html")

@app.post("/login")
def login_post():
    jikwonno_raw = (request.form.get("jikwonno") or "").strip()
    jikwonname = (request.form.get("jikwonname") or "").strip()
    
    if not jikwonno_raw.isdigit() or not jikwonname:
        flash("직원번호는 숫자로, 직원이름은 필수입니다.")
        return redirect(url_for("login_form"))

    jikwonno = int(jikwonno_raw)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # 로그인 체크
            cur.execute("""
                        select jikwonno, jikwonname, jikwonjik from jikwon
                        where jikwonno=%s and jikwonname=%s
                        """,(jikwonno, jikwonname))
            me = cur.fetchone()
            
            if not me:
                flash("로그인 실패.\n직원정보 불일치")
                return redirect(url_for("login_form"))
            
            # 로그인 성공의 경우
            cur.execute("""
                select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(jikwonibsail) as jikwonibsail_year
                from jikwon inner join buser on busernum = buserno
                order by jikwonno
            """)
            rows = cur.fetchall()

            session["jikwonno"] = me["jikwonno"]
            session["jikwonname"] = me["jikwonname"]
            session["jikwonjik"] = me["jikwonjik"]

            return render_template("jikwonlist.html", rows=rows, login_user=me)
            
    finally:
        conn.close()

@app.get("/gogek/<int:jikwonno>")
def gogek_list(jikwonno:int):
    if "jikwonno" not in session:
        flash("로그인 후 고객정보 이용하세요.")
        return redirect(url_for("login_form"))
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        select gogekno, gogekname, gogektel from gogek
                        where gogekdamsano=%s
                        order by gogekno
                        """, (jikwonno,))
            customers = cur.fetchall()

            cur.execute("""
                        select jikwonname, jikwonjik from jikwon
                        where jikwonno=%s
                        """, (jikwonno,))
            emp = cur.fetchone()
        return render_template(
            "gogeklist.html",
            customers=customers,
            empno=jikwonno,
            empname=(emp["jikwonname"] if emp else ""),
            empjik=(emp["jikwonjik"] if emp else "")
            )
    
    finally:
        conn.close()

@app.get("/jikwons")
def jikwon_list():
    if "jikwonno" not in session:
        flash("로그인 후 이용하세요")
        return redirect(url_for("login_form"))
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(jikwonibsail) as jikwonibsail_year
                        from jikwon inner join buser on busernum = buserno
                        order by jikwonno
                        """)
            rows = cur.fetchall()
            login_user = {
                "jikwonno" : session["jikwonno"],
                "jikwonname" : session["jikwonname"],
                "jikwonjik" : session["jikwonjik"]
            }
        return render_template(
            "jikwonlist.html",
            rows=rows,
            login_user=login_user
            )
    
    finally:
        conn.close()

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_form"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)