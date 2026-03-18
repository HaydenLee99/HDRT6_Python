from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
import pymysql
import os
from datetime import date, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

PER_PAGE = 10


# ── DB 연결 ───────────────────────────────────────────────────────────────────
def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


# ── 관리자 권한 체크 ──────────────────────────────────────────────────────────
# 관리자 세션 확인 - 미로그인 또는 일반 유저 접근 차단
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('관리자만 접근할 수 있습니다.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ── 공통: 대기 중 신청 수 ─────────────────────────────────────────────────────
def get_pending_count(cur):
    cur.execute("SELECT COUNT(*) AS cnt FROM flight_request WHERE status = '대기'")
    return cur.fetchone()['cnt']


# ── 공통: 좌표 → SVG % 변환 ──────────────────────────────────────────────────
def to_map_xy(lat, lng):
    LAT_MIN, LAT_MAX = 33.0, 38.7
    LNG_MIN, LNG_MAX = 125.0, 130.0
    try:
        x = round((float(lng) - LNG_MIN) / (LNG_MAX - LNG_MIN) * 90 + 5, 2)
        y = round((1 - (float(lat) - LAT_MIN) / (LAT_MAX - LAT_MIN)) * 80 + 10, 2)
        return x, y
    except Exception:
        return 50, 50


# ──────────────────────────────────────────────────────────────────────────────
#  대시보드  /admin/
# ──────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/')
@admin_required
def admin_dashboard():
    conn = get_conn()
    cur  = conn.cursor()

    # 이번 달 통계
    cur.execute("""
        SELECT
            COUNT(*)                   AS total,
            SUM(status = '대기')       AS pending,
            SUM(status = '승인')       AS approved,
            SUM(status = '거절')       AS rejected
        FROM flight_request
        WHERE MONTH(start_date) = MONTH(CURDATE())
          AND YEAR(start_date)  = YEAR(CURDATE())
    """)
    stats = cur.fetchone()

    # 최근 허가 신청 5건
    # flight_request.user_id → users.user_id → users.name
    cur.execute("""
        SELECT
            fr.request_id,
            u.name      AS applicant_name,
            fr.purpose,
            fr.status,
            fr.start_date AS created_at
        FROM flight_request fr
        JOIN users u ON fr.user_id = u.user_id
        ORDER BY fr.request_id DESC
        LIMIT 5
    """)
    raw_recent = cur.fetchall()

    # 상태값 한글 → 영어 변환 (admin.html badge 용)
    status_map_to_en = {'대기': 'pending', '승인': 'approved', '거절': 'rejected'}
    recent_permits = []
    for r in raw_recent:
        r['status'] = status_map_to_en.get(r['status'], r['status'])
        recent_permits.append(r)

    # 최근 가입 회원 5명
    cur.execute("""
        SELECT login_id AS user_id, name, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT 5
    """)
    recent_users = cur.fetchall()

    pending_count = get_pending_count(cur)
    conn.close()

    return render_template('admin.html',
        active_tab='dashboard',
        pending_count=pending_count,
        stats=stats,
        recent_permits=recent_permits,
        recent_users=recent_users,
    )


# ──────────────────────────────────────────────────────────────────────────────
#  비행 허가 신청 목록  /admin/approval
# ──────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/approval')
@admin_required
def admin_approval():
    q      = request.args.get('q', '').strip()
    status = request.args.get('status', '')
    page   = int(request.args.get('page', 1))
    offset = (page - 1) * PER_PAGE

    # status 필터: 화면에서는 영어(pending/approved/rejected), DB는 한글
    status_map_to_kr = {'pending': '대기', 'approved': '승인', 'rejected': '거절'}

    conditions, params = [], []
    if q:
        conditions.append("(u.name LIKE %s OR fr.purpose LIKE %s)")
        params += [f'%{q}%', f'%{q}%']
    if status and status in status_map_to_kr:
        conditions.append("fr.status = %s")
        params.append(status_map_to_kr[status])

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    conn = get_conn()
    cur  = conn.cursor()

    cur.execute(f"""
        SELECT COUNT(*) AS cnt
        FROM flight_request fr
        JOIN users u ON fr.user_id = u.user_id
        {where}
    """, params)
    total_count = cur.fetchone()['cnt']
    total_pages = max(1, -(-total_count // PER_PAGE))

    cur.execute(f"""
        SELECT
            fr.request_id               AS permit_id,
            u.name                      AS applicant_name,
            u.login_id                  AS applicant_id,
            u.phone                     AS applicant_phone,
            fr.purpose                  AS flight_area,
            fr.purpose,
            fr.start_date,
            fr.end_date,
            COALESCE(fr.start_time,'')  AS start_time,
            COALESCE(fr.end_time,'')    AS end_time,
            fr.drone_type,
            COALESCE(fr.flight_altitude,0) AS flight_altitude,
            fr.status,
            fr.latitude,
            fr.longitude,
            COALESCE(fr.radius,500)     AS radius,
            COALESCE(fr.photo_request,0) AS photo_request,
            fr.reject_reason
        FROM flight_request fr
        JOIN users u ON fr.user_id = u.user_id
        {where}
        ORDER BY fr.request_id DESC
        LIMIT %s OFFSET %s
    """, params + [PER_PAGE, offset])
    raw_permits = cur.fetchall()

    # 상태값 한글 → 영어 변환 (admin.html badge 용)
    status_map_to_en = {'대기': 'pending', '승인': 'approved', '거절': 'rejected'}
    permits = []
    for p in raw_permits:
        p['status'] = status_map_to_en.get(p['status'], p['status'])
        permits.append(p)

    pending_count = get_pending_count(cur)
    conn.close()

    return render_template('admin.html',
        active_tab='approval',
        pending_count=pending_count,
        permits=permits,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
    )


# ── 개별 승인 / 거절 ─────────────────────────────────────────────────────────
@admin_bp.route('/approval/<int:permit_id>/approve')
@admin_required
def admin_permit_approve(permit_id):
    admin_id = session.get('admin_id', 1)
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "UPDATE flight_request SET status = '승인', admin_id = %s WHERE request_id = %s",
        (admin_id, permit_id)
    )
    conn.commit()
    conn.close()
    flash('✅ 허가가 승인되었습니다.', 'success')
    return redirect(url_for('admin.admin_approval'))


@admin_bp.route('/approval/<int:permit_id>/reject', methods=['POST'])
@admin_required
def admin_permit_reject(permit_id):
    reason   = request.form.get('reason', '').strip()
    admin_id = session.get('admin_id', 1)
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "UPDATE flight_request SET status = '거절', admin_id = %s, reject_reason = %s WHERE request_id = %s",
        (admin_id, reason or None, permit_id)
    )
    conn.commit()
    conn.close()
    flash('❌ 허가가 거절되었습니다.', 'error')
    return redirect(url_for('admin.admin_approval'))


# ── 일괄 승인 / 거절 ─────────────────────────────────────────────────────────
@admin_bp.route('/approval/bulk', methods=['POST'])
@admin_required
def admin_approval_bulk():
    action     = request.form.get('action')
    permit_ids = request.form.getlist('permit_ids')

    if not permit_ids:
        flash('선택된 항목이 없습니다.', 'error')
        return redirect(url_for('admin.admin_approval'))
    if action not in ('approve', 'reject', 'delete'):
        flash('잘못된 요청입니다.', 'error')
        return redirect(url_for('admin.admin_approval'))

    conn = get_conn()
    cur  = conn.cursor()
    placeholders = ','.join(['%s'] * len(permit_ids))

    if action == 'delete':
        cur.execute(
            f"DELETE FROM flight_request WHERE request_id IN ({placeholders})",
            permit_ids
        )
        conn.commit()
        conn.close()
        flash(f'{len(permit_ids)}건이 삭제되었습니다.', 'info')
        return redirect(url_for('admin.admin_approval'))

    status   = '승인' if action == 'approve' else '거절'
    admin_id = session.get('admin_id', 1)

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        f"UPDATE flight_request SET status = %s, admin_id = %s WHERE request_id IN ({placeholders})",
        [status, admin_id] + permit_ids
    )
    conn.close()

    label = '승인' if action == 'approve' else '거절'
    flash(f'{len(permit_ids)}건이 일괄 {label} 처리되었습니다.', 'success')
    return redirect(url_for('admin.admin_approval'))


# ──────────────────────────────────────────────────────────────────────────────
#  허가 지역 지도  /admin/map
# ──────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/map')
@admin_required
def admin_map():
    date_from = request.args.get('date_from', '').strip()
    date_to   = request.args.get('date_to',   '').strip()

    # 기본값: 파라미터가 없으면 오늘 ~ 오늘+7일
    today = date.today()
    if not date_from and not date_to:
        date_from = today.strftime('%Y-%m-%d')
        date_to   = (today + timedelta(days=7)).strftime('%Y-%m-%d')

    conn = get_conn()
    cur  = conn.cursor()

    # 날짜 범위 필터: 신청 기간이 선택 범위와 겹치는 건 조회
    where  = ""
    params = []
    if date_from and date_to:
        where  = "WHERE fr.start_date <= %s AND fr.end_date >= %s"
        params = [date_to, date_from]
    elif date_from:
        where  = "WHERE fr.end_date >= %s"
        params = [date_from]
    elif date_to:
        where  = "WHERE fr.start_date <= %s"
        params = [date_to]

    cur.execute(f"""
        SELECT
            fr.request_id   AS permit_id,
            u.name          AS applicant_name,
            fr.purpose      AS flight_area,
            fr.status,
            fr.latitude,
            fr.longitude,
            COALESCE(fr.radius, 500) AS radius,
            fr.start_date,
            fr.end_date
        FROM flight_request fr
        JOIN users u ON fr.user_id = u.user_id
        {where}
        ORDER BY fr.request_id DESC
    """, params)
    raw = cur.fetchall()

    status_map_to_en = {'대기': 'pending', '승인': 'approved', '거절': 'rejected'}
    map_permits = []
    for p in raw:
        p['status']  = status_map_to_en.get(p['status'], p['status'])
        p['map_x'], p['map_y'] = to_map_xy(p['latitude'], p['longitude'])
        map_permits.append(p)

    pending_count = get_pending_count(cur)
    conn.close()

    return render_template('admin.html',
        active_tab='map',
        pending_count=pending_count,
        map_permits=map_permits,
        api_key=os.getenv("VWORLD_API_KEY", ""),
        date_from=date_from,
        date_to=date_to,
    )


# ──────────────────────────────────────────────────────────────────────────────
#  회원 정보 조회  /admin/members
# ──────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/members')
@admin_required
def admin_members():
    q           = request.args.get('q', '').strip()
    drone       = request.args.get('drone', '')
    user_status = request.args.get('user_status', '')   # 가입 승인 상태 필터
    page        = int(request.args.get('page', 1))
    offset      = (page - 1) * PER_PAGE

    conditions, params = [], []
    if q:
        conditions.append("(u.login_id LIKE %s OR u.name LIKE %s)")
        params += [f'%{q}%', f'%{q}%']
    if drone == 'registered':
        conditions.append("d.drone_id IS NOT NULL")
    elif drone == 'unregistered':
        conditions.append("d.drone_id IS NULL")
    if user_status:
        conditions.append("u.status = %s")
        params.append(user_status)

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    conn = get_conn()
    cur  = conn.cursor()

    # 가입 대기 회원 수 (사이드바 뱃지용)
    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE status = '대기'")
    member_pending_count = cur.fetchone()['cnt']

    cur.execute(f"""
        SELECT COUNT(*) AS cnt
        FROM users u
        LEFT JOIN drone d ON u.user_id = d.user_id
        {where}
    """, params)
    total_users = cur.fetchone()['cnt']
    total_pages = max(1, -(-total_users // PER_PAGE))

    cur.execute(f"""
        SELECT
            u.user_id,
            u.login_id,
            u.name,
            u.birth                  AS birth_date,
            u.phone,
            u.status,
            u.created_at,
            (d.drone_id IS NOT NULL) AS has_drone
        FROM users u
        LEFT JOIN drone d ON u.user_id = d.user_id
        {where}
        ORDER BY
            CASE u.status WHEN '대기' THEN 0 ELSE 1 END,
            u.created_at DESC
        LIMIT %s OFFSET %s
    """, params + [PER_PAGE, offset])
    users = cur.fetchall()

    pending_count = get_pending_count(cur)
    conn.close()

    return render_template('admin.html',
        active_tab='members',
        pending_count=pending_count,
        member_pending_count=member_pending_count,
        users=users,
        total_users=total_users,
        total_pages=total_pages,
        page=page,
    )


# ── 회원 가입 승인  GET /admin/members/<id>/approve ──────────────────────────
@admin_bp.route('/members/<int:user_id>/approve')
@admin_required
def admin_member_approve(user_id):
    admin_id = session.get('admin_id', 1)
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "UPDATE users SET status = '승인', reject_reason = NULL WHERE user_id = %s",
        (user_id,)
    )
    cur.execute(
        "INSERT INTO user_approval_log (user_id, action, reason, admin_id) VALUES (%s, '승인', NULL, %s)",
        (user_id, admin_id)
    )
    conn.close()
    flash('✅ 회원 가입이 승인되었습니다.', 'success')
    return redirect(url_for('admin.admin_members'))


# ── 회원 가입 거절 (사유 입력)  POST /admin/members/<id>/reject ───────────────
@admin_bp.route('/members/<int:user_id>/reject', methods=['POST'])
@admin_required
def admin_member_reject(user_id):
    reason   = request.form.get('reason', '').strip()
    admin_id = session.get('admin_id', 1)

    if not reason:
        flash('거절 사유를 입력해주세요.', 'error')
        return redirect(url_for('admin.admin_members'))

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "UPDATE users SET status = '거절', reject_reason = %s WHERE user_id = %s",
        (reason, user_id)
    )
    cur.execute(
        "INSERT INTO user_approval_log (user_id, action, reason, admin_id) VALUES (%s, '거절', %s, %s)",
        (user_id, reason, admin_id)
    )
    conn.close()
    flash('❌ 회원 가입이 거절되었습니다.', 'error')
    return redirect(url_for('admin.admin_members'))


# ──────────────────────────────────────────────────────────────────────────────
#  공지사항 관리  /admin/notice
# ──────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/notice')
@admin_required
def admin_notice():
    q      = request.args.get('q', '').strip()
    page   = int(request.args.get('page', 1))
    offset = (page - 1) * PER_PAGE

    conditions, params = [], []
    if q:
        conditions.append("title LIKE %s")
        params.append(f'%{q}%')

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    conn = get_conn()
    cur  = conn.cursor()

    cur.execute(f"SELECT COUNT(*) AS cnt FROM notice {where}", params)
    total_notices = cur.fetchone()['cnt']
    total_pages   = max(1, -(-total_notices // PER_PAGE))

    # notice 테이블엔 is_pinned 없으므로 0 고정
    cur.execute(f"""
        SELECT notice_id, title, created_at, 0 AS is_pinned
        FROM notice
        {where}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, params + [PER_PAGE, offset])
    notices = cur.fetchall()

    pending_count = get_pending_count(cur)
    conn.close()

    return render_template('admin.html',
        active_tab='notice',
        pending_count=pending_count,
        notices=notices,
        total_notices=total_notices,
        total_pages=total_pages,
        page=page,
    )


# ── 공지사항 등록 ─────────────────────────────────────────────────────────────
@admin_bp.route('/notice/create', methods=['POST'])
@admin_required
def admin_notice_create():
    title   = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        flash('제목과 내용을 모두 입력해주세요.', 'error')
        return redirect(url_for('admin.admin_notice'))

    # notice.admin_id → admins 테이블 FK
    # session에 admin_id 저장해두거나, 임시로 1 고정
    admin_id = session.get('admin_id', 1)

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO notice (title, content, admin_id) VALUES (%s, %s, %s)",
        (title, content, admin_id)
    )
    conn.close()

    flash('📢 공지사항이 등록되었습니다.', 'success')
    return redirect(url_for('admin.admin_notice'))


# ── 공지사항 삭제 ─────────────────────────────────────────────────────────────
@admin_bp.route('/notice/delete/<int:notice_id>')
@admin_required
def admin_notice_delete(notice_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("DELETE FROM notice WHERE notice_id = %s", (notice_id,))
    conn.close()

    flash('공지사항이 삭제되었습니다.', 'info')
    return redirect(url_for('admin.admin_notice'))


# ── 공지사항 수정 ─────────────────────────────────────────────────────────────
@admin_bp.route('/notice/edit/<int:notice_id>', methods=['GET', 'POST'])
@admin_required
def admin_notice_edit(notice_id):
    conn = get_conn()
    cur  = conn.cursor()

    if request.method == 'POST':
        title   = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        cur.execute(
            "UPDATE notice SET title = %s, content = %s WHERE notice_id = %s",
            (title, content, notice_id)
        )
        conn.close()
        flash('공지사항이 수정되었습니다.', 'success')
        return redirect(url_for('admin.admin_notice'))

    cur.execute("SELECT * FROM notice WHERE notice_id = %s", (notice_id,))
    notice = cur.fetchone()
    conn.close()

    if not notice:
        flash('존재하지 않는 공지사항입니다.', 'error')
        return redirect(url_for('admin.admin_notice'))

    from flask import jsonify
    return jsonify({
        'notice_id': notice['notice_id'],
        'title':     notice['title'],
        'content':   notice['content'],
    })


# ── 로그아웃 ─────────────────────────────────────────────────────────────────
@admin_bp.route('/logout')
def admin_logout():
    session.clear()
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('login'))


# ──────────────────────────────────────────────────────────────────────────────
#  사전 확인 관리  /admin/precheck
# ──────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/precheck')
@admin_required
def admin_precheck():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM pre_check ORDER BY sort_order, check_id")
    items = cur.fetchall()
    pending_count = get_pending_count(cur)
    conn.close()
    return render_template('admin.html',
        active_tab='precheck',
        pending_count=pending_count,
        precheck_items=items,
    )

@admin_bp.route('/precheck/create', methods=['POST'])
@admin_required
def admin_precheck_create():
    icon    = request.form.get('icon', '✅').strip()
    content = request.form.get('content', '').strip()
    if not content:
        flash('내용을 입력해주세요.', 'error')
        return redirect(url_for('admin.admin_precheck'))
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM pre_check")
    next_order = cur.fetchone()['COALESCE(MAX(sort_order),0)+1']
    cur.execute("INSERT INTO pre_check (icon, content, sort_order) VALUES (%s, %s, %s)",
                (icon, content, next_order))
    conn.commit()
    conn.close()
    flash('✅ 사전 확인 항목이 등록되었습니다.', 'success')
    return redirect(url_for('admin.admin_precheck'))

@admin_bp.route('/precheck/delete/<int:check_id>')
@admin_required
def admin_precheck_delete(check_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("DELETE FROM pre_check WHERE check_id = %s", (check_id,))
    conn.commit()
    conn.close()
    flash('삭제되었습니다.', 'info')
    return redirect(url_for('admin.admin_precheck'))
