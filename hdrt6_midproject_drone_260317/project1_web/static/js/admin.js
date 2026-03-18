/* ============================================================
   admin.js — 관리자 페이지 전용 스크립트
============================================================ */

/* ─── 날짜 input 연도 4자리 제한 ─── */
function limitYear(input) {
    if (!input.value) return;
    const parts = input.value.split('-');
    if (parts[0] && parts[0].length > 4) {
        parts[0] = parts[0].slice(0, 4);
        input.value = parts.join('-');
    }
}

/* ─── 관리자 지도 날짜 유효성 ─── */
function validateAdminMapDate(form) {
    const from = form.querySelector('[name="date_from"]').value;
    const to   = form.querySelector('[name="date_to"]').value;
    if (from && to && from > to) {
        showToast('시작 날짜는 종료 날짜보다 이전이어야 합니다.', 'warn');
        return false;
    }
    return true;
}

/* ─── 토스트 알림 ─── */
function showToast(msg, type) {
    type = type || 'info';
    const wrap = document.getElementById('toastWrap');
    if (!wrap) return;
    const toast = document.createElement('div');
    toast.className   = 'toast ' + type;
    toast.textContent = msg;
    wrap.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 3000);
}

/* ─── 상세 모달: data-* 속성 방식 래퍼 ─── */
function openDetailModalFromBtn(btn) {
    openDetailModal(
        parseInt(btn.dataset.pid)       || 0,
        btn.dataset.name                || '',
        btn.dataset.lid                 || '',
        btn.dataset.phone               || '-',
        btn.dataset.area                || '',
        btn.dataset.period              || '',
        btn.dataset.stime               || '-',
        btn.dataset.etime               || '-',
        btn.dataset.drone               || '-',
        parseInt(btn.dataset.altitude)  || 0,
        parseInt(btn.dataset.radius)    || 500,
        btn.dataset.coord               || '',
        btn.dataset.reason              || '',
        parseInt(btn.dataset.photo)     || 0
    );
}

/* ─── 상세 모달 ─── */
function openDetailModal(permitId, name, loginId, phone, area, period,
                         startTime, endTime, drone, altitude, radius, coord, rejectReason, photoRequest) {
    var html = '';

    function row(label, value, accent) {
        return '<div class="detail-item">' +
               '<div class="detail-label">' + label + '</div>' +
               '<div class="detail-value' + (accent ? ' accent' : '') + '">' + (value || '—') + '</div>' +
               '</div>';
    }

    html += row('신청자',   name);
    html += row('아이디',   loginId,  true);
    html += row('연락처',   phone);
    html += row('비행 목적', area);
    html += row('비행 기간', period);
    html += row('비행 시간', startTime + ' ~ ' + endTime);
    html += row('드론 종류', drone);
    html += row('비행 고도', altitude ? altitude + ' m' : '—');
    html += row('비행 반경', radius + ' m');
    html += row('좌표',     coord,    true);
    html += row('촬영 신청', photoRequest ? '✅ 촬영 신청함' : '🚫 촬영 안함');

    html += '<div class="detail-item" style="grid-column:1/-1;">' +
                '<div class="detail-label">거절 사유</div>' +
                '<div class="detail-value" style="color:' +
                    (rejectReason ? 'var(--red)' : 'var(--text-muted)') + ';">' +
                    (rejectReason || '—') +
                '</div>' +
            '</div>';

    html += '<div class="detail-item" style="grid-column:1/-1;">' +
                '<div class="detail-label">첨부파일</div>' +
                '<div class="detail-value" id="detail-files-wrap">' +
                    '<span style="color:var(--text-muted);font-size:0.82rem;">불러오는 중...</span>' +
                '</div>' +
            '</div>';

    document.getElementById('detailContent').innerHTML = html;
    document.getElementById('detailModal').classList.add('open');
    loadAdminPermitFiles(permitId);
}

/* ─── 첨부파일 목록 ─── */
async function loadAdminPermitFiles(permitId) {
    const wrap = document.getElementById('detail-files-wrap');
    if (!wrap) return;
    try {
        const res  = await fetch('/api/my_permits/' + permitId + '/files');
        const data = await res.json();
        if (!data.ok || data.files.length === 0) {
            wrap.innerHTML = '<span style="color:var(--text-muted);font-size:0.82rem;">첨부파일 없음</span>';
            return;
        }
        var rows = '';
        data.files.forEach(function(f) {
            var kb = f.file_size ? ((f.file_size / 1024).toFixed(1) + ' KB') : '';
            rows += '<div style="display:flex;align-items:center;gap:0.5rem;padding:0.28rem 0;' +
                        'border-bottom:1px solid var(--border);font-size:0.82rem;">' +
                        '<span>📄</span>' +
                        '<span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' +
                            f.original_name +
                        '</span>' +
                        '<span style="color:var(--text-muted);font-size:0.72rem;">' + kb + '</span>' +
                        '<a href="' + f.download_url + '" download="' + f.original_name + '"' +
                           ' class="btn btn-ghost btn-sm"' +
                           ' style="font-size:0.72rem;padding:0.15rem 0.5rem;white-space:nowrap;">' +
                            '⬇ 다운로드' +
                        '</a>' +
                    '</div>';
        });
        wrap.innerHTML = rows;
    } catch(e) {
        wrap.innerHTML = '<span style="color:var(--text-muted);font-size:0.82rem;">파일 목록 조회 실패</span>';
    }
}

function closeDetailModal() {
    document.getElementById('detailModal').classList.remove('open');
}

/* ─── 거절 모달 (회원) ─── */
function openRejectModal(userId, userName) {
    document.getElementById('rejectTargetName').textContent = userName;
    document.getElementById('rejectReason').value = '';
    document.getElementById('rejectForm').action = '/admin/members/' + userId + '/reject';
    document.getElementById('rejectModal').classList.add('open');
}
function closeRejectModal() {
    document.getElementById('rejectModal').classList.remove('open');
}

/* ─── 거절 모달 (허가) ─── */
function openPermitRejectModal(permitId, name) {
    document.getElementById('permitRejectTargetName').textContent = name;
    document.getElementById('permitRejectReason').value = '';
    document.getElementById('permitRejectForm').action = '/admin/approval/' + permitId + '/reject';
    document.getElementById('permitRejectModal').classList.add('open');
}
function closePermitRejectModal() {
    document.getElementById('permitRejectModal').classList.remove('open');
}

/* ─── 사유 모달 ─── */
function openReasonModal(userName, reason) {
    document.getElementById('reasonTargetName').textContent = userName;
    document.getElementById('reasonContent').textContent = reason;
    document.getElementById('reasonModal').classList.add('open');
}
function closeReasonModal() {
    document.getElementById('reasonModal').classList.remove('open');
}

/* ─── 일괄 처리 ─── */
function toggleSelectAll(cb) {
    document.querySelectorAll('.row-cb').forEach(function(c) { c.checked = cb.checked; });
    updateBulkBar();
}
function updateBulkBar() {
    const n   = document.querySelectorAll('.row-cb:checked').length;
    const bar = document.getElementById('bulkBar');
    if (!bar) return;
    document.getElementById('bulkCount').textContent = n + '개';
    bar.classList.toggle('show', n > 0);
}
function submitBulk(action) {
    if (!document.querySelectorAll('.row-cb:checked').length) return;
    document.getElementById('bulkAction').value = action;
    document.getElementById('bulkForm').submit();
}
function submitBulkDelete() {
    const n = document.querySelectorAll('.row-cb:checked').length;
    if (!n) return;
    if (!confirm('선택한 ' + n + '건을 삭제하시겠습니까?\n삭제된 데이터는 복구할 수 없습니다.')) return;
    document.getElementById('bulkAction').value = 'delete';
    document.getElementById('bulkForm').submit();
}

/* ─── 공지사항 수정 모달 ─── */
async function openNoticeEditModal(noticeId) {
    try {
        const res  = await fetch('/admin/notice/edit/' + noticeId);
        const data = await res.json();
        document.getElementById('noticeEditTitle').value   = data.title;
        document.getElementById('noticeEditContent').value = data.content;
        document.getElementById('noticeEditForm').action   = '/admin/notice/edit/' + noticeId;
        document.getElementById('noticeEditModal').classList.add('open');
    } catch(e) {
        showToast('공지사항 정보를 불러오지 못했습니다.', 'error');
    }
}
function closeNoticeEditModal() {
    document.getElementById('noticeEditModal').classList.remove('open');
}

/* ─── Fallback ─── */
if (typeof window.togglePins      === 'undefined') window.togglePins      = function() {};
if (typeof window.adminToggleZone === 'undefined') window.adminToggleZone = function() {};

/* ─── Flash → Toast ─── */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.flash-msg').forEach(function(el) {
        const type = el.classList.contains('flash-success') ? 'success'
                   : el.classList.contains('flash-error')   ? 'error' : 'info';
        showToast(el.textContent.trim(), type);
    });
});
