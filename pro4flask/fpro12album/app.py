# ============================================================
# 라이브러리 import
# ============================================================

import os
import uuid                 # Universally Unique Identifier의 약자로 '고유한 문자열 ID' 생성
from flask import Flask, request, render_template, redirect, url_for, flash
import pymysql
from werkzeug.utils import secure_filename
from PIL import Image       # Python Imaging Library로 이미지 열기/저장, 크기 변경, 포맷 변환(JPG ↔ PNG ↔ WEBP), 썸네일 작성 등
from dotenv import load_dotenv

# ============================================================
# Flask 앱 설정
# ============================================================

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "DEV_SECRET_KEY")

load_dotenv()

# ============================================================
# DB 연결 설정
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_NAME = os.getenv("DB_NAME")


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PWD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


# ============================================================
# 업로드 설정
# ============================================================

UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
THUMB_DIR = os.path.join(app.root_path, "static", "uploads", "thumbs")

ALLOWED_EXT = {"jpg", "jpeg", "png", "gif", "webp"}
THUMB_MAX_SIZE = (240, 240)  # 썸네일 최대 크기


# ============================================================
# 썸네일 경로 생성 함수
# ============================================================

def thumb_rel_from_file_pathFunc(file_path: str) -> str:
    # file_path: "uploads/xxxx.jpg" -> thumb: "uploads/thumbs/xxxx.jpg"
    base = os.path.basename(file_path)
    return f"uploads/thumbs/{base}"

    # DB에는 원본경로만 저장
    # 썸네일 경로는 규칙으로 계산


# ============================================================
# 업로드 파일 확장자 검사
# ============================================================

def allowed_fileFunc(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ============================================================
# 이미지 저장 + 썸네일 생성
# ============================================================

def save_image_and_thumbFunc(file_storage):

    orig = secure_filename(file_storage.filename)
    ext = orig.rsplit(".", 1)[1].lower()

    saved_name = f"{uuid.uuid4().hex}.{ext}"

    file_abs = os.path.join(UPLOAD_DIR, saved_name)
    file_storage.save(file_abs)

    file_rel = f"uploads/{saved_name}"
    thumb_rel = thumb_rel_from_file_pathFunc(file_rel)

    thumb_abs = os.path.join(app.root_path, "static", thumb_rel)

    make_thumbnailFunc(file_abs, thumb_abs)

    return file_rel, thumb_rel


# ============================================================
# 썸네일 생성 함수
# ============================================================

def make_thumbnailFunc(src_abs: str, thumb_abs: str):

    with Image.open(src_abs) as ima:
        ima.thumbnail(THUMB_MAX_SIZE)
        ima.save(thumb_abs)


# ============================================================
# 파일 삭제 안전 함수
# ============================================================

def safe_removeFunc(rel_path: str):

    abs_path = os.path.join(app.root_path, "static", rel_path)

    try:
        if os.path.exists(abs_path):
            os.remove(abs_path)
    except:
        pass


# ============================================================
# 업로드 폴더 준비
# ============================================================

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)


# ============================================================
# 홈 페이지
# ============================================================

@app.get("/")
def home():
    return redirect(url_for("albums_list"))


# ============================================================
# 앨범 목록
# ============================================================

@app.get("/albums")
def albums_list():

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id, name, created_at FROM albums ORDER BY id DESC"
            )

            albums = cur.fetchall()

        return render_template("albums.html", albums=albums)

    finally:
        conn.close()


# ============================================================
# 앨범 추가
# ============================================================

@app.post("/albums/add")
def albums_add():

    name = (request.form.get("name") or "").strip()

    if not name:
        flash("앨범 이름은 필수입니다.")
        return redirect(url_for("albums_list"))

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "INSERT INTO albums(name) VALUES (%s)",
                (name,)
            )

        return redirect(url_for("albums_list"))

    finally:
        conn.close()


# ============================================================
# 앨범 수정 (폼)
# ============================================================

@app.get("/albums/edit/<int:album_id>")
def albums_edit_form(album_id: int):

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id, name FROM albums WHERE id=%s",
                (album_id,)
            )

            album = cur.fetchone()

        if not album:
            flash("해당 앨범이 없습니다.")
            return redirect(url_for("albums_list"))

        return render_template(
            "album_edit.html",
            album=album
        )

    finally:
        conn.close()


# ============================================================
# 앨범 수정 저장
# ============================================================

@app.post("/albums/edit/<int:album_id>")
def albums_edit_save(album_id: int):

    name = (request.form.get("name") or "").strip()

    if not name:
        flash("앨범 이름은 필수입니다.")
        return redirect(url_for("albums_edit_form", album_id=album_id))

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "UPDATE albums SET name=%s WHERE id=%s",
                (name, album_id)
            )

        return redirect(url_for("albums_list"))

    finally:
        conn.close()


# ============================================================
# 앨범 삭제
# ============================================================

@app.post("/albums/delete/<int:album_id>")
def albums_delete(album_id: int):

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM photos WHERE album_id=%s",
                (album_id,)
            )

            if cur.fetchone()["cnt"] > 0:

                flash("이 앨범에는 사진이 있어 삭제할 수 없습니다. (먼저 사진을 삭제하세요)")
                return redirect(url_for("albums_list"))

            cur.execute(
                "DELETE FROM albums WHERE id=%s",
                (album_id,)
            )

        return redirect(url_for("albums_list"))

    finally:
        conn.close()


# ============================================================
# 사진 목록
# ============================================================

@app.get("/albums/<int:album_id>/photos")
def photos_list(album_id: int):

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id, name FROM albums WHERE id=%s",
                (album_id,)
            )

            album = cur.fetchone()

            if not album:
                flash("해당 앨범이 없습니다.")
                return redirect(url_for("albums_list"))

            cur.execute("""
                SELECT id, album_id, title, file_path, created_at
                FROM photos
                WHERE album_id=%s
                ORDER BY id DESC
            """, (album_id,))

            photos = cur.fetchall()

        for p in photos:
            p["thumb_path"] = thumb_rel_from_file_pathFunc(p["file_path"])

        return render_template(
            "photos.html",
            album=album,
            photos=photos
        )

    finally:
        conn.close()


# ============================================================
# 사진 업로드
# ============================================================

@app.post("/albums/<int:album_id>/photos/add")
def photos_add(album_id: int):

    title = (request.form.get("title") or "").strip()
    file = request.files.get("photo")

    if not title:
        flash("사진 제목(title)은 필수입니다.")
        return redirect(url_for("photos_list", album_id=album_id))

    if not file or file.filename == "":
        flash("업로드할 파일을 선택하세요.")
        return redirect(url_for("photos_list", album_id=album_id))

    if not allowed_fileFunc(file.filename):
        flash("허용 확장자: jpg, jpeg, png, gif, webp")
        return redirect(url_for("photos_list", album_id=album_id))

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id FROM albums WHERE id=%s",
                (album_id,)
            )

            if not cur.fetchone():
                flash("앨범이 존재하지 않습니다.")
                return redirect(url_for("albums_list"))

        file_rel, _thumb_rel = save_image_and_thumbFunc(file)

        with conn.cursor() as cur:

            cur.execute(
                "INSERT INTO photos(album_id, title, file_path) VALUES (%s, %s, %s)",
                (album_id, title, file_rel)
            )

        return redirect(url_for("photos_list", album_id=album_id))

    finally:
        conn.close()


# ============================================================
# 사진 수정 폼
# ============================================================

@app.get("/photos/edit/<int:photo_id>")
def photo_edit_form(photo_id: int):

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id, album_id, title, file_path FROM photos WHERE id=%s",
                (photo_id,)
            )

            photo = cur.fetchone()

        if not photo:
            flash("해당 사진이 없습니다.")
            return redirect(url_for("albums_list"))

        photo["thumb_path"] = thumb_rel_from_file_pathFunc(photo["file_path"])

        return render_template(
            "photo_edit.html",
            photo=photo
        )

    finally:
        conn.close()


# ============================================================
# 사진 수정 저장
# ============================================================

@app.post("/photos/edit/<int:photo_id>")
def photo_edit_save(photo_id: int):

    title = (request.form.get("title") or "").strip()
    new_file = request.files.get("photo")

    if not title:
        flash("제목은 필수입니다.")
        return redirect(url_for("photo_edit_form", photo_id=photo_id))

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id, album_id, title, file_path FROM photos WHERE id=%s",
                (photo_id,)
            )

            old = cur.fetchone()

        if not old:
            flash("해당 사진이 없습니다.")
            return redirect(url_for("albums_list"))

        album_id = old["album_id"]
        old_file_path = old["file_path"]
        old_thumb_path = thumb_rel_from_file_pathFunc(old_file_path)

        if not new_file or new_file.filename == "":

            with conn.cursor() as cur:

                cur.execute(
                    "UPDATE photos SET title=%s WHERE id=%s",
                    (title, photo_id)
                )

            return redirect(url_for("photos_list", album_id=album_id))

        if not allowed_fileFunc(new_file.filename):
            flash("허용 확장자: jpg, jpeg, png, gif, webp")
            return redirect(url_for("photo_edit_form", photo_id=photo_id))

        new_file_rel, _new_thumb_rel = save_image_and_thumbFunc(new_file)

        with conn.cursor() as cur:

            cur.execute(
                "UPDATE photos SET title=%s, file_path=%s WHERE id=%s",
                (title, new_file_rel, photo_id)
            )

        safe_removeFunc(old_file_path)
        safe_removeFunc(old_thumb_path)

        return redirect(url_for("photos_list", album_id=album_id))

    finally:
        conn.close()


# ============================================================
# 사진 삭제
# ============================================================

@app.post("/photos/delete/<int:photo_id>")
def photos_delete(photo_id: int):

    conn = get_conn()

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT id, album_id, file_path FROM photos WHERE id=%s",
                (photo_id,)
            )

            row = cur.fetchone()

            if not row:
                flash("해당 사진이 없습니다.")
                return redirect(url_for("albums_list"))

            album_id = row["album_id"]
            file_path = row["file_path"]
            thumb_path = thumb_rel_from_file_pathFunc(file_path)

            cur.execute(
                "DELETE FROM photos WHERE id=%s",
                (photo_id,)
            )

        safe_removeFunc(file_path)
        safe_removeFunc(thumb_path)

        return redirect(url_for("photos_list", album_id=album_id))

    finally:
        conn.close()


# ============================================================
# 서버 실행
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)