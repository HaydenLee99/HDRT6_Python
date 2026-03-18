# pip install dotenv
# pip install pymysql
# pip install astral
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session, jsonify
import pymysql
import os
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime,timedelta
import requests
from astral import LocationInfo
from astral.sun import sun
import pytz
import time
import threading
import atexit
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

app = Flask(__name__)

# 변경 후
app.secret_key = os.getenv("FLASK_SECRET_KEY") or os.urandom(24)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "airspace_db")
DB_AIRSPACE = os.getenv("DB_AIRSPACE", "airspace_db")
API_KEY_WEA = os.getenv("API_KEY_WEA")
API_KEY_WEAS = os.getenv("API_KEY_WEAS")

# ── 파일 업로드 설정 ──────────────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",                          # utf8mb4 : '전 세계 문자 (한글 포함) + 이모지'까지 처리
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_airspace_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_AIRSPACE,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
# ──────────────────────────────────────────────────────────────
#  관리자 Blueprint 등록
# ──────────────────────────────────────────────────────────────
from admin_routes import admin_bp
app.register_blueprint(admin_bp)   # /admin/* 라우트 자동 등록

# ##############################################################################################
#                                       메인 페이지
# ##############################################################################################
@app.route("/")
def index():
    api_key = os.getenv("VWORLD_API_KEY")
    drone_weight = None
    if session.get('user_id'):
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT max_takeoff_weight FROM drone WHERE user_id=%s",
                            (session['user_id'],))
                row = cur.fetchone()
                if row and row['max_takeoff_weight']:
                    drone_weight = float(row['max_takeoff_weight'])
            conn.close()
        except:
            pass
    return render_template("main.html", api_key=api_key, drone_weight=drone_weight)


# ##############################################################################################
#                                       비행가능 확인 페이지
# ##############################################################################################
@app.route("/flight_check")
def flight_check():
    return render_template("main.html")  # 추후 별도 템플릿으로 분리


# ##############################################################################################
#                                       비행 허가 페이지
# ##############################################################################################
@app.route("/permit")
def permit():
    return render_template("main.html")  # 추후 별도 템플릿으로 분리


# ##############################################################################################
#                                       공지사항 페이지
# ##############################################################################################
@app.route("/notice")
def notice():
    return render_template("main.html")  # 추후 별도 템플릿으로 분리


# ##############################################################################################
#                                       회원가입
# ##############################################################################################
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        birth = request.form["birth"]
        phone = request.form["phone"]
        login_id = request.form["login_id"]
        password = request.form["password"]

        drone_type         = request.form.get("drone_type")         or None
        weight             = request.form.get("weight")             or None
        size               = request.form.get("size")               or None
        max_takeoff_weight = request.form.get("max_takeoff_weight") or None

        conn = get_conn()
        cur = conn.cursor()

        # 아이디 중복 체크
        cur.execute("SELECT user_id FROM users WHERE login_id = %s", (login_id,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template("register.html", error="이미 사용 중인 아이디입니다.")

        sql_user = """
        INSERT INTO users (login_id,password,name,birth,phone)
        VALUES (%s,%s,%s,%s,%s)
        """
        cur.execute(sql_user,(login_id,password,name,birth,phone))
        user_id = cur.lastrowid

        if any([drone_type, weight, size, max_takeoff_weight]):
            sql_drone = """
            INSERT INTO drone (user_id,drone_type,weight,size,max_takeoff_weight)
            VALUES (%s,%s,%s,%s,%s)
            """
            cur.execute(sql_drone,(user_id,drone_type,weight,size,max_takeoff_weight))

        cur.close()
        conn.close()

        flash("회원가입 완료")
        return redirect(url_for("login"))

    return render_template("register.html")


# ##############################################################################################
#                                       로그인
# ##############################################################################################
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login_id = request.form["login_id"]
        password = request.form["password"]

        conn = get_conn()
        cur = conn.cursor()

        # 1) 일반 유저 확인
        cur.execute(
            "SELECT * FROM users WHERE login_id=%s AND password=%s",
            (login_id, password)
        )
        user = cur.fetchone()

        # 2) 유저가 없으면 관리자 확인
        if not user:
            cur.execute(
                "SELECT * FROM admins WHERE login_id=%s AND password=%s",
                (login_id, password)
            )
            admin = cur.fetchone()
        else:
            admin = None

        cur.close()
        conn.close()

        if user:
            if user["status"] != "승인":
                flash("관리자 승인 후 로그인 가능합니다.")
            else:
                session["user_id"]  = user["user_id"]
                session["name"]     = user["name"]
                session["is_admin"] = False
                flash("로그인 성공")
                return redirect(url_for("index"))

        elif admin:
            session["admin_id"] = admin["admin_id"]
            session["name"]     = admin["admin_name"]
            session["is_admin"] = True
            flash("관리자로 로그인 되었습니다.")
            return redirect(url_for("admin.admin_dashboard"))

        else:
            flash("아이디 또는 비밀번호 오류")

    return render_template("login.html")

# 로그아웃
@app.route("/logout")
def logout():

    session.clear()

    flash("로그아웃 완료")

    return redirect(url_for("index"))


# ##############################################################################################
#                                       마이페이지
# ##############################################################################################
@app.route("/mypage")
def mypage():
    if "user_id" not in session:
        flash("로그인 필요")
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id = %s", (session["user_id"],))
    user = cur.fetchone()

    cur.execute("SELECT * FROM drone WHERE user_id = %s", (session["user_id"],))
    drone = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("mypage.html",
        login_id           = user["login_id"],
        name               = user["name"],
        birth              = user["birth"],
        phone              = user["phone"],
        drone_type         = (drone["drone_type"]         if drone else None) or "",
        weight             = (drone["weight"]             if drone else None) or "",
        size               = (drone["size"]               if drone else None) or "",
        max_takeoff_weight = (drone["max_takeoff_weight"] if drone else None) or "",
    )

@app.route("/mypage/update", methods=["POST"])
def mypage_update():
    if "user_id" not in session:
        flash("로그인 필요")
        return redirect(url_for("login"))

    name       = request.form.get("name")
    birth      = request.form.get("birth")
    phone      = request.form.get("phone")
    password   = request.form.get("password")

    drone_type         = request.form.get("drone_type")         or None
    weight             = request.form.get("weight")             or None
    size               = request.form.get("size")               or None
    max_takeoff_weight = request.form.get("max_takeoff_weight") or None

    conn = get_conn()
    cur  = conn.cursor()

    if password:
        cur.execute("""
            UPDATE users SET name=%s, birth=%s, phone=%s, password=%s
            WHERE user_id=%s
        """, (name, birth, phone, password, session["user_id"]))
    else:
        cur.execute("""
            UPDATE users SET name=%s, birth=%s, phone=%s
            WHERE user_id=%s
        """, (name, birth, phone, session["user_id"]))

    cur.execute("SELECT drone_id FROM drone WHERE user_id=%s", (session["user_id"],))
    drone = cur.fetchone()

    has_drone_data = any([drone_type, weight, size, max_takeoff_weight])

    if has_drone_data:
        if drone:
            cur.execute("""
                UPDATE drone SET drone_type=%s, weight=%s, size=%s, max_takeoff_weight=%s
                WHERE user_id=%s
            """, (drone_type, weight, size, max_takeoff_weight, session["user_id"]))
        else:
            cur.execute("""
                INSERT INTO drone (user_id, drone_type, weight, size, max_takeoff_weight)
                VALUES (%s, %s, %s, %s, %s)
            """, (session["user_id"], drone_type, weight, size, max_takeoff_weight))
    else:
        # 전부 비어있으면 드론 레코드 삭제
        if drone:
            cur.execute("DELETE FROM drone WHERE user_id=%s", (session["user_id"],))

    cur.close()
    conn.close()

    session["name"] = name
    return """
        <script>
            alert('✅ 정보가 저장되었습니다.');
            location.href = '/mypage';
        </script>
    """
    return redirect(url_for("mypage"))


# ##############################################################################################
#                                       관리자 전용
# ##############################################################################################
# @app.route("/admin")
# def admin():
#     # TODO: 관리자 권한 확인 로직 구현
#     return render_template("main.html")  # 추후 admin.html 로 분리

# test 위해서 잠시 주석처리

# ##############################################################################################
#                                       지도 API
# ##############################################################################################

CATEGORY_MAP = {
    "FORBIDDEN":  "forbidden",
    "RESTRICTED": "restricted",
    "DANGER":     "danger",
    "CAUTION":    "danger",
    "SPECIAL":    "restricted",
}

@app.route("/api/zones")
def api_zones():
    try:
        conn = get_airspace_conn()
        with conn.cursor() as cur:
            sql = """
                SELECT
                    z.zone_id, z.zone_name, z.zone_category, z.zone_code,
                    g.polygon_index, g.ring_index, g.point_order,
                    g.longitude, g.latitude
                FROM airspace_zone     z
                JOIN airspace_geometry g ON z.zone_id = g.zone_id
                WHERE z.is_active = 1
                AND z.zone_category IN ('FORBIDDEN', 'RESTRICTED', 'DANGER', 'CAUTION', 'SPECIAL')
                ORDER BY z.zone_id, g.polygon_index, g.ring_index, g.point_order
            """
            cur.execute(sql)
            rows = cur.fetchall()
        conn.close()

        poly_map = {}
        for row in rows:
            key = (row["zone_id"], row["polygon_index"])
            if key not in poly_map:
                poly_map[key] = {
                    "id":       row["zone_id"],
                    "name":     row["zone_name"],
                    "code":     row["zone_code"] or "",
                    "type":     CATEGORY_MAP.get(row["zone_category"], "restricted"),
                    "category": row["zone_category"],
                    "coords":   []
                }
            poly_map[key]["coords"].append([row["longitude"], row["latitude"]])

        return jsonify({"ok": True, "zones": list(poly_map.values())})

    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


@app.route("/api/zone_log", methods=["POST"])
def api_zone_log():
    if "user_id" not in session:
        return jsonify({"ok": False, "msg": "로그인 필요"})

    data = request.get_json()
    lat  = data.get("latitude")
    lng  = data.get("longitude")

    if lat is None or lng is None:
        return jsonify({"ok": False, "msg": "좌표 누락"})

    try:
        conn = get_conn()
        with conn.cursor() as cur:
            sql = """
                INSERT INTO flight_zone_log (user_id, latitude, longitude)
                VALUES (%s, %s, %s)
            """
            cur.execute(sql, (session["user_id"], lat, lng))
        conn.close()
        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})

# ── /api/address  (vworld CORS 우회 프록시) ────────────────
@app.route("/api/address")
def api_address():
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "msg": "잘못된 좌표"})

    def point_in_polygon(px, py, coords):
        n = len(coords)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = coords[i]
            xj, yj = coords[j]
            if ((yi > py) != (yj > py)) and \
               (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    try:
        from collections import defaultdict
        conn = get_airspace_conn()
        with conn.cursor() as cur:
            # ① 바운딩박스로 후보 구역 추리기
            cur.execute("""
                SELECT district_id FROM admin_district_bbox
                WHERE min_lng <= %s AND max_lng >= %s
                AND min_lat <= %s AND max_lat >= %s
            """, (lng, lng, lat, lat))
            candidates = [r["district_id"] for r in cur.fetchall()]

            if not candidates:
                conn.close()
                return jsonify({"ok": False, "msg": "행정구역 없음"})

            # ② 후보 구역 좌표만 가져오기
            fmt = ",".join(["%s"] * len(candidates))
            cur.execute(f"""
                SELECT d.district_id, d.sido, d.sigungu, d.emd,
                g.polygon_index, g.point_order,
                g.longitude, g.latitude
                FROM admin_geometry g
                JOIN admin_district d ON g.district_id = d.district_id
                WHERE g.district_id IN ({fmt})
                ORDER BY g.district_id, g.polygon_index, g.point_order
            """, candidates)
            rows = cur.fetchall()
        conn.close()

        # ③ 폴리곤 조립
        polygons = defaultdict(lambda: {"info": None, "coords": defaultdict(list)})
        for row in rows:
            did = row["district_id"]
            polygons[did]["info"] = (row["sido"], row["sigungu"], row["emd"])
            polygons[did]["coords"][row["polygon_index"]].append(
                (row["longitude"], row["latitude"])
            )

        # ④ Ray Casting — 통과 후보 중 폴리곤 중심이 가장 가까운 것 선택
        best      = None
        best_dist = float('inf')

        for did, data in polygons.items():
            for coords in data["coords"].values():
                if len(coords) < 3:
                    continue
                if point_in_polygon(lng, lat, coords):
                    cx = sum(c[0] for c in coords) / len(coords)
                    cy = sum(c[1] for c in coords) / len(coords)
                    dist = (cx - lng) ** 2 + (cy - lat) ** 2
                    if dist < best_dist:
                        best_dist = dist
                        sido, sigungu, emd = data["info"]
                        best = " ".join(p for p in [sido, sigungu, emd] if p)

        if best:
            return jsonify({"ok": True, "address": best})
        return jsonify({"ok": False, "msg": "행정구역 없음"})

    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})

# ##############################################################################################
#                                       날씨 기능 (기상청 API -> DB -> Web)
# ##############################################################################################

session_weather = requests.Session()

retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=0.5,
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session_weather.mount("https://", adapter)
session_weather.mount("http://", adapter)

# 실수 문자열 변환
def to_float(v):

    if v is None:
        return None
    
    v = v.strip()
    if v in ("", "-"):
        return None
    
    try:
        return float(v)
    except ValueError:
        return None
    
# 정수 문자열 변환
def to_int(v):

    if v is None:
        return None
    
    v = v.strip()
    if v in ("", "-"):
        return None
    
    try:
        return int(v)
    except ValueError:
        return None

# ── 관측소(station)와 기상 정보(weather_info) DB 처리 ────────────────────────────────────

# 기상 정보 DB 초기화
def clear_weather():

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM weather_info")
            print("weather_info 초기화 완료")

    finally:
        conn.close()


# 기상 정보 DB 용량 관리 (6시간 이전)
def cleanup_weather():

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM weather_info WHERE TM < NOW() - INTERVAL 6 HOUR")

    finally:
        conn.close()


# 기상 정보 DB 저장
def save_weather_to_db(weather_data:dict):

    conn = get_conn()
    try:
        with conn.cursor() as cur:

            sql = """
            INSERT INTO weather_info
            (STN, TM, WS, WD, RN, TYPE)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                WS = VALUES(WS),
                WD = VALUES(WD),
                RN = VALUES(RN),
                TYPE = VALUES(TYPE)
            """

            for stn, data in weather_data.items():
                cur.execute(sql, (stn, data["TM"], data["WS"], data["WD"], data["RN"], data["TYPE"]))

    finally:
        conn.close()


# 최신 기상 정보 DB 조회
def get_weather_from_db(stn:str):

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT STN, TM, WS, WD, RN, TYPE
                FROM weather_info
                WHERE STN=%s
                ORDER BY TM DESC
                LIMIT 1
            """, (stn,))

            row = cur.fetchone()
            if not row:
                return None

            tm = row["TM"]
            return {
                "TM": tm,
                "year": tm.year,
                "month": tm.month,
                "day": tm.day,
                "hour": tm.hour,
                "WS": row["WS"],
                "WD": row["WD"],
                "RN": row["RN"],
                "TYPE": row["TYPE"]
                }
        
    finally:
        conn.close()


# 관측소 DB 로드
def load_station_data():

    station_dict = {}
    try:

        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT STN, STN_NAME, LAT, LON, TYPE FROM station")

            for row in cur.fetchall():
                station_dict[str(row["STN"])] = {
                    "stn_name": row["STN_NAME"],
                    "lat": float(row["LAT"]),
                    "lon": float(row["LON"]),
                    "type": row["TYPE"]
                }

    except Exception as e:
        print("관측소 데이터 로드 오류:", e)
        station_dict = {}

    finally:
        conn.close()
        
    return station_dict


# 서버 시작 시 관측소 DB 로드
try:
    station_dict = load_station_data()
    print(f"관측소 데이터 로드: {len(station_dict)}건")

except Exception as e:
    print("관측소 로드 실패:", e)
    station_dict = {}


# ── 입력 좌표에서 최근방 관측소 찾기 ───────────────────────────────
def nearest_station_wind(lat:float, lon:float):

    min_dist = float("inf")
    nearest  = None

    for stn, info in station_dict.items():
        dist = (lat - info["lat"])**2 + (lon - info["lon"])**2

        if dist < min_dist:
            min_dist = dist
            nearest  = stn

    return nearest


def nearest_station_rain(lat:float, lon:float):

    min_dist = float("inf")
    nearest  = None

    for stn, info in station_dict.items():
        # 지상 관측소만 강수 데이터를 가짐.
        if info["type"] != "GROUND": continue

        dist = (lat - info["lat"])**2 + (lon - info["lon"])**2
        if dist < min_dist:
            min_dist = dist
            nearest  = stn

    return nearest


# ── 기상청 API ───────────────────────────────

# 지상 관측
def get_ground_weather(tm:str):

    url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php"
    params = {"tm": tm, "stn": "0", "help": "0", "authKey": API_KEY_WEA}

    try:
        res = session_weather.get(url, params=params, timeout=(5,15))
        res.raise_for_status()
    except Exception as e:
        print("지상 관측 API 오류:", e)
        return {}

    result = {}
    for line in res.text.splitlines():

        line = line.strip()
        if not line or line.startswith("#"):
            continue

        data = line.split()

        # 관측 지점 코드
        stn = data[1]

        # 관측 일시
        TM = datetime.strptime(data[0], "%Y%m%d%H%M")
        
        # 풍향 (36방위 -> deg)
        WD = to_int(data[2])
        if 0 <= WD <=36: WD = WD*10
        else: WD = None

        # 풍속 (m/s)
        WS = to_float(data[3])
        if WS < 0: WS = None
        else: WS = WS

        # 강수 (mm)
        RN = to_float(data[10])
        if RN < 0: RN = None
        else: RN = RN

        result[stn] = {
            "TM": TM,
            "WD": WD,
            "WS": WS,
            "RN": RN,
            "TYPE": "GROUND"
        }

    return result


# 해상 관측
def get_sea_weather(tm:str):

    url = "https://apihub.kma.go.kr/api/typ01/url/kma_buoy.php"
    params = {"tm": tm, "stn": "0", "help": "0", "authKey": API_KEY_WEAS}

    try:
        res = session_weather.get(url, params=params, timeout=(5,15))
        res.raise_for_status()
    except Exception as e:
        print("해상 관측 API 오류:", e)
        return {}

    result = {}
    for line in res.text.splitlines():

        line = line.strip()
        if not line or line.startswith("#"):
            continue

        data = line.split()

        # 관측 지점 코드
        stn = data[1]

        # 관측 일시
        TM = datetime.strptime(data[0], "%Y%m%d%H%M")

        # 풍향 (deg)
        WD = to_int(data[2])
        if 0 <= WD <=360: WD = WD
        else: WD = None

        # 풍속 (m/s)
        WS = to_float(data[3])
        if WS < 0: WS = None
        else: WS = WS

        result[stn] = {
            "TM": TM,
            "WD": WD,
            "WS": WS,
            "RN": None,
            "TYPE": "SEA"
        }

    return result


# 기상 정보 DB 업데이트
def update_weather():
    try:
        now = datetime.now()
        tm_now = now.strftime("%Y%m%d%H00")

        # 지상/해상 API 호출
        ground_now = get_ground_weather(tm_now)
        time.sleep(1)
        sea_now = get_sea_weather(tm_now)


        weather = {**ground_now, **sea_now}

        if not weather:
            print("날씨 데이터 없음")
            return False

        save_weather_to_db(weather)
        cleanup_weather()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 날씨 업데이트 완료 : {len(weather)}건")
        return True

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 날씨 업데이트 오류: {e}")
        return False


# 서버 시작시, 초기 기상 정보 DB 데이터
def initial_weather_load():

    now = datetime.now()

    tm_now = now.strftime("%Y%m%d%H00")
    tm_prev = (now - timedelta(hours=1)).strftime("%Y%m%d%H00")

    ground_prev = get_ground_weather(tm_prev)
    sea_prev = get_sea_weather(tm_prev)
    time.sleep(1)

    ground_now = get_ground_weather(tm_now)
    sea_now = get_sea_weather(tm_now)
    time.sleep(1)

    weather = {
        **ground_prev,
        **sea_prev,
        **ground_now,
        **sea_now
    }

    save_weather_to_db(weather)

    print(f"초기 데이터 저장 : {len(weather)}건")


# 스케줄러
def weather_scheduler():
    while True:
        now = datetime.now()

        # 다음 정각+2분
        next_run = now.replace(minute=2, second=0, microsecond=0)
        if now.minute >= 2:
            next_run += timedelta(hours=1)

        wait_seconds = (next_run - now).total_seconds()
        print(f"[{now.strftime('%H:%M:%S')}] 다음 정규 업데이트: {next_run.strftime('%H:%M:%S')}")
        time.sleep(wait_seconds)

        # 기본 업데이트 시도
        success = update_weather()

        # 실패 시 1분 간격 재시도, 최대 5회
        retry_count = 0
        while not success and retry_count < 5:
            retry_count += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 업데이트 실패, 재시도 {retry_count}/5 (1분 후)")
            time.sleep(60)
            success = update_weather()


# ── 서버 시작 시 스레드 실행 ──
def start_weather_thread():
    t = threading.Thread(target=weather_scheduler, daemon=True)
    t.start()
    print("기상 정보 업데이트 스레드 시작")


# ── 일출 / 일몰 계산 ──────────────────────────────────────
def get_sun_time(lat:float, lon:float):
    city = LocationInfo(latitude=lat, longitude=lon, timezone="Asia/Seoul")
    s    = sun(city.observer, date=datetime.now().date(),
                tzinfo=pytz.timezone("Asia/Seoul"))
    return s["sunrise"].time(), s["sunset"].time()


# ── 비행 가능 여부 판단 ───────────────────────────────────

def flight_status(sunrise, sunset, wind:float, rain:float):
    
    # 주야간 조건
    now = datetime.now().time()
    if (wind is None and rain is None) or (wind is None and rain == 0.0) or (rain is None and wind == 0.0):
        return "비행 판단 불가", "기상 데이터를 불러올 수 없습니다."
    if not (sunrise <= now <= sunset):
        return "비행 불가", "야간 비행 불가(일몰 후 ~ 일출 전)"
    
    # 강수 조건
    if rain is not None and rain > 0:
        return "비행 위험", f"강수({rain}mm) 상황으로 비행 불가"
    
    # 풍속 조건
    if wind is not None and wind >=10:
        return "비행 금지", f"강풍({wind}m/s) 상황으로 비행 불가"
    if wind is not None and wind >=8:
        return "비행 위험", f"강풍({wind}m/s) 상황으로 비행 위험"
    if wind is not None and wind >= 6:
        return "비행 주의", f"강풍({wind}m/s) 상황으로 비행 주의"
    if wind is not None and wind >= 4:
        return "비행 가능", f"다소 바람이 있어 비행 주의 ({wind}m/s)"

    return "비행 가능", "안전한 비행 조건입니다."


# API
@app.route("/api/weather")
def api_weather():
    try:
        lat = float(request.args.get("lat", 37.5665))
        lon = float(request.args.get("lon", 126.9780))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "msg": "잘못된 좌표"})

    sunrise, sunset = get_sun_time(lat, lon)

    # 가장 가까운 관측소 찾기
    stn_rain = nearest_station_rain(lat, lon) or "108"
    stn_wind = nearest_station_wind(lat, lon) or "108"

    stn_name = station_dict.get(stn_wind, {}).get("stn_name", "Unknown")

    # DB에서 최신 데이터 조회
    weather_rain = get_weather_from_db(stn_rain)
    weather_wind = get_weather_from_db(stn_wind)

    if not weather_rain or not weather_wind:
        return jsonify({"ok": False, "msg": "해당 지역 기상 데이터 조회 불가"})

    # 비행 가능 여부 판단
    status, reason = flight_status(
        sunrise, sunset,
        weather_wind.get("WS") or weather_wind.get("wind"),
        weather_rain.get("RN") or weather_rain.get("rain")
    )

    return jsonify({
        "ok": True,
        "lat": lat,
        "lon": lon,
        "stn_name": stn_name,
        "year": weather_rain.get("year"),
        "month": weather_rain.get("month"),
        "day": weather_rain.get("day"),
        "hour": weather_rain.get("hour"),
        "wind_dir": weather_wind.get("WD") or weather_wind.get("wind_dir"),
        "wind": weather_wind.get("WS") or weather_wind.get("wind"),
        "rain": weather_rain.get("RN") or weather_rain.get("rain"),
        "sunrise": sunrise.strftime("%H:%M"),
        "sunset": sunset.strftime("%H:%M"),
        "status": status,
        "reason": reason
    })

# 서버 종료 처리
def shutdown_cleanup():

    print("서버 종료 → weather_info clear")
    clear_weather()


atexit.register(shutdown_cleanup)

# ##############################################################################################
#                                    사전 확인 API  ← 팀원 추가
# ##############################################################################################
@app.route("/api/prechecks")
def api_prechecks():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT check_id, icon, content
                FROM pre_check
                ORDER BY sort_order, check_id
            """)
            rows = cur.fetchall()
        conn.close()
        return jsonify({"ok": True, "items": [
            {"id": r["check_id"], "icon": r["icon"], "content": r["content"]}
            for r in rows
        ]})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                    비행 허가 신청 API  (FormData 방식 — 파일 업로드 포함)
# ##############################################################################################
@app.route("/api/permit/submit", methods=["POST"])
def api_permit_submit():
    if "user_id" not in session:
        return jsonify({"ok": False, "msg": "로그인이 필요합니다."})
    try:
        user_id        = session["user_id"]
        purpose        = request.form.get("purpose", "").strip()
        drone_type     = request.form.get("drone_type", "").strip()
        start_date     = request.form.get("start_date", "").strip()
        end_date       = request.form.get("end_date", "").strip()
        start_time     = request.form.get("start_time", "").strip() or None
        end_time       = request.form.get("end_time", "").strip() or None
        latitude       = request.form.get("latitude")
        longitude      = request.form.get("longitude")
        radius         = request.form.get("radius", 500)
        flight_altitude= request.form.get("flight_altitude", None)

        if not all([purpose, start_date, end_date]):
            return jsonify({"ok": False, "msg": "필수 항목(사용 목적, 비행 기간)을 모두 입력해주세요."})

        lat = float(latitude)  if latitude  else None
        lng = float(longitude) if longitude else None
        r   = int(radius)      if radius    else 500
        alt = int(flight_altitude) if flight_altitude else None

        conn = get_conn()
        with conn.cursor() as cur:
            photo_req = 1 if request.form.get('photo_request','0') == '1' else 0
            try:
                cur.execute("""
                    INSERT INTO flight_request
                        (user_id, purpose, drone_type, start_date, end_date,
                         start_time, end_time, latitude, longitude, radius,
                         flight_altitude, photo_request, status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'대기')
                """, (user_id, purpose, drone_type, start_date, end_date,
                       start_time, end_time, lat, lng, r, alt, photo_req))
            except Exception:
                cur.execute("""
                    INSERT INTO flight_request
                        (user_id, purpose, drone_type, start_date, end_date,
                         latitude, longitude, radius, status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'대기')
                """, (user_id, purpose, drone_type, start_date, end_date, lat, lng, r))
            request_id = cur.lastrowid

            # 파일 저장
            files = request.files.getlist("attachments")
            for f in files:
                if f and f.filename and allowed_file(f.filename):
                    safe = secure_filename(f.filename)
                    saved = f"{request_id}_{safe}"
                    f.save(os.path.join(UPLOAD_FOLDER, saved))
                    cur.execute("""
                        INSERT INTO permit_files (request_id, original_name, saved_name, file_size)
                        VALUES (%s, %s, %s, %s)
                    """, (request_id, f.filename, saved, len(f.read()) if hasattr(f, 'read') else 0))
        conn.close()
        return jsonify({"ok": True, "msg": "신청이 완료되었습니다.", "request_id": request_id})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                    허가 신청 수정 API  (대기 상태만 가능)
# ##############################################################################################
@app.route("/api/my_permits/<int:req_id>/update", methods=["POST"])
def api_permit_update(req_id):
    if "user_id" not in session:
        return jsonify({"ok": False, "msg": "로그인이 필요합니다."})
    try:
        data           = request.get_json()
        purpose        = data.get("purpose", "").strip()
        drone_type     = data.get("drone_type", "").strip()
        start_date     = data.get("start_date", "").strip()
        end_date       = data.get("end_date", "").strip()
        latitude       = data.get("latitude")
        longitude      = data.get("longitude")
        radius         = data.get("radius", 500)
        flight_altitude= data.get("flight_altitude", None)

        if not all([purpose, start_date, end_date]):
            return jsonify({"ok": False, "msg": "필수 항목을 입력해주세요."})

        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE flight_request
                SET purpose=%s, drone_type=%s, start_date=%s, end_date=%s,
                    latitude=%s, longitude=%s, radius=%s, flight_altitude=%s
                WHERE request_id=%s AND user_id=%s AND status='대기'
            """, (purpose, drone_type, start_date, end_date,
                   latitude, longitude, radius, flight_altitude,
                   req_id, session["user_id"]))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({"ok": False, "msg": "수정할 수 없습니다. 대기 중인 신청만 수정 가능합니다."})
        conn.close()
        return jsonify({"ok": True, "msg": "수정이 완료되었습니다."})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                    허가 신청 첨부파일 목록 API
# ##############################################################################################
@app.route("/api/my_permits/<int:req_id>/files")
def api_permit_files(req_id):
    """특정 허가 신청의 첨부파일 목록 반환 (유저 본인 또는 관리자)"""
    is_admin = session.get("is_admin", False)
    user_id  = session.get("user_id")
    if not is_admin and not user_id:
        return jsonify({"ok": False, "msg": "로그인이 필요합니다."})
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            # 본인 신청 또는 관리자만 조회 가능
            if not is_admin:
                cur.execute("SELECT request_id FROM flight_request WHERE request_id=%s AND user_id=%s",
                            (req_id, user_id))
                if not cur.fetchone():
                    conn.close()
                    return jsonify({"ok": False, "msg": "권한이 없습니다."})
            cur.execute("""
                SELECT file_id, original_name, saved_name, file_size, uploaded_at
                FROM permit_files WHERE request_id=%s ORDER BY file_id
            """, (req_id,))
            files = [{
                "file_id":       r["file_id"],
                "original_name": r["original_name"],
                "saved_name":    r["saved_name"],
                "file_size":     r["file_size"],
                "download_url":  f"/api/permit/download/{r['saved_name']}"
            } for r in cur.fetchall()]
        conn.close()
        return jsonify({"ok": True, "files": files})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                    첨부파일 다운로드 API
# ##############################################################################################
@app.route("/api/permit/download/<path:filename>")
def api_permit_download(filename):
    """첨부파일 다운로드 (관리자 또는 본인)"""
    is_admin = session.get("is_admin", False)
    user_id  = session.get("user_id")
    if not is_admin and not user_id:
        return jsonify({"ok": False, "msg": "로그인이 필요합니다."}), 403
    try:
        from flask import send_from_directory
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception:
        return jsonify({"ok": False, "msg": "파일을 찾을 수 없습니다."}), 404


# ##############################################################################################
#                                   내 허가 신청 구역 API (메인 지도 연동)  ← 내 버전
# ##############################################################################################
@app.route("/api/my_permits")
def api_my_permits():
    """로그인한 유저의 허가 신청 목록 반환 (지도 표시용)"""
    if "user_id" not in session:
        return jsonify({"ok": True, "permits": []})
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT request_id, purpose, start_date, end_date,
                       COALESCE(start_time,'') AS start_time,
                       COALESCE(end_time,'') AS end_time,
                       latitude, longitude, radius,
                       COALESCE(drone_type,'') AS drone_type,
                       COALESCE(flight_altitude,0) AS flight_altitude,
                       COALESCE(photo_request,0) AS photo_request,
                       status,
                       COALESCE(reject_reason, '') AS reject_reason
                FROM flight_request
                WHERE user_id = %s
                  AND latitude  IS NOT NULL
                  AND longitude IS NOT NULL
                ORDER BY request_id DESC
            """, (session["user_id"],))
            rows = cur.fetchall()
        conn.close()
        permits = [{
            "id":               r["request_id"],
            "purpose":          r["purpose"],
            "start_date":       str(r["start_date"]),
            "end_date":         str(r["end_date"]),
            "start_time":       r["start_time"],
            "end_time":         r["end_time"],
            "lat":              float(r["latitude"]),
            "lng":              float(r["longitude"]),
            "radius":           r["radius"] or 500,
            "drone_type":       r["drone_type"],
            "flight_altitude":  r["flight_altitude"],
            "status":           r["status"],
            "reject_reason":    r.get("reject_reason", "") or "",
            "photo_request":    int(r.get("photo_request", 0) or 0)
        } for r in rows]
        return jsonify({"ok": True, "permits": permits})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                   전체 허가 신청 구역 API (관리자 전용)  ← 내 버전
# ##############################################################################################
@app.route("/api/all_permits")
def api_all_permits():
    """관리자: 모든 유저의 허가 신청 목록 반환 (메인 지도 표시용)"""
    if not session.get("is_admin"):
        return jsonify({"ok": False, "msg": "관리자 권한 필요"})
    try:
        date_from = request.args.get("date_from", "").strip()
        date_to   = request.args.get("date_to",   "").strip()

        # 날짜 범위 필터: 신청 기간이 선택 범위와 겹치는 건 조회
        where_extra = ""
        params = []
        if date_from and date_to:
            where_extra = "AND fr.start_date <= %s AND fr.end_date >= %s"
            params = [date_to, date_from]
        elif date_from:
            where_extra = "AND fr.end_date >= %s"
            params = [date_from]
        elif date_to:
            where_extra = "AND fr.start_date <= %s"
            params = [date_to]

        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT fr.request_id, u.name AS user_name, fr.purpose,
                       fr.start_date, fr.end_date,
                       fr.latitude, fr.longitude,
                       COALESCE(fr.radius, 500) AS radius,
                       fr.status
                FROM flight_request fr
                JOIN users u ON fr.user_id = u.user_id
                WHERE fr.latitude  IS NOT NULL
                  AND fr.longitude IS NOT NULL
                  {where_extra}
                ORDER BY fr.request_id DESC
            """, params)
            rows = cur.fetchall()
        conn.close()

        # 한글 상태 → 영어 변환 (JS colorMap key와 일치)
        status_map = {'승인': 'approved', '대기': 'pending', '거절': 'rejected'}
        permits = [{
            "id":        r["request_id"],
            "user_name": r["user_name"],
            "purpose":   r["purpose"],
            "start_date": str(r["start_date"]),
            "end_date":   str(r["end_date"]),
            "lat":    float(r["latitude"]),
            "lng":    float(r["longitude"]),
            "radius": r["radius"] or 500,
            "status": status_map.get(r["status"], "pending")
        } for r in rows]
        return jsonify({"ok": True, "permits": permits})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                       공지사항 API
# ##############################################################################################
@app.route("/api/notices")
def api_notices():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT notice_id, title, content, created_at
                FROM notice
                ORDER BY notice_id DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
        conn.close()
        notices = []
        for r in rows:
            notices.append({
                "id":         r["notice_id"],
                "title":      r["title"],
                "content":    r["content"] or "",
                "created_at": r["created_at"].strftime("%Y.%m.%d") if r["created_at"] else "-"
            })
        return jsonify({"ok": True, "notices": notices})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})


# ##############################################################################################
#                                       실행 코드
# ##############################################################################################
if __name__ == "__main__":

    clear_weather()             # DB 초기화
    initial_weather_load()      # 초기 데이터 로드
    start_weather_thread()      # 업데이트 스케줄러 스레드 시작

    # Flask 서버 실행
    app.run(host="0.0.0.0", port=5000, debug=False)