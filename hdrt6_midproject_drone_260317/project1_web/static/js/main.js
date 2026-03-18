/* ============================================================
   main.js
   역할: main.html 전용 — 탭 전환, 공지사항 로드/모달
   원본: main.html 내 <script> 블록 추출
   의존: Flask 세션 변수 (IS_LOGGED_IN, IS_ADMIN) → main.html에서 전달
============================================================ */

/* ─── 탭 전환 ─── */
function showTab(tab, btn) {
    // 비행 허가 탭: 로그인 필수 (비로그인 시 서버 렌더링으로 주입된 값 활용)
    if (tab === 'permit' && !IS_LOGGED_IN && !IS_ADMIN) {
        alert('비행 허가 신청은 로그인 후 이용 가능합니다.');
        location.href = '/login';
        return;
    }

    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');

    const panelMap     = document.getElementById('panel-map');
    const panelWeather = document.getElementById('panel-weather');
    const panelPermit  = document.getElementById('panel-permit');
    const panelNotice  = document.getElementById('panel-notice');

    // 전부 숨기기
    panelMap.style.display     = 'none';
    panelWeather.style.display = 'none';
    panelPermit.style.display  = 'none';
    panelNotice.classList.remove('active');

    if (tab === 'map') {
        panelMap.style.display     = 'flex';
        panelWeather.style.display = 'flex';
        // OpenLayers는 숨겨진 상태에서 크기를 측정 못하므로
        // 패널이 보인 뒤 강제로 크기 재계산
        setTimeout(() => {
            if (typeof vMap !== 'undefined' && vMap) vMap.updateSize();
        }, 50);
    } else if (tab === 'permit') {
        panelPermit.style.display = 'block';
        pmInitMap();
    } else if (tab === 'notice') {
        panelNotice.classList.add('active');
        loadNotices();
    }
}

/* ─── 공지사항 동적 로딩 ─── */
let noticesLoaded = false;

async function loadNotices() {
    if (noticesLoaded) return;
    try {
        const res  = await fetch('/api/notices');
        const data = await res.json();
        const list = document.getElementById('notice-list');

        if (!data.ok || data.notices.length === 0) {
            list.innerHTML = '<div class="notice-item" style="justify-content:center; color:var(--text-muted); font-size:0.83rem;">등록된 공지사항이 없습니다.</div>';
            return;
        }

        list.innerHTML = data.notices.map((n, i) => `
            <div class="notice-item" onclick="openNoticeModal('${escapeHtml(n.title)}', '${escapeHtml(n.content)}', '${n.created_at}')">
                ${i === 0 ? '<span class="notice-badge badge-new">NEW</span>' : ''}
                <span class="notice-title">${n.title}</span>
                <span class="notice-date">${n.created_at}</span>
            </div>
        `).join('');

        noticesLoaded = true;
    } catch (e) {
        document.getElementById('notice-list').innerHTML =
            '<div class="notice-item" style="justify-content:center; color:var(--text-muted); font-size:0.83rem;">공지사항을 불러오지 못했습니다.</div>';
    }
}

/* ─── HTML 이스케이프 ─── */
function escapeHtml(str) {
    return str.replace(/'/g, "\\'").replace(/\n/g, '\\n');
}

/* ─── 공지 모달 열기 / 닫기 ─── */
function openNoticeModal(title, content, date) {
    document.getElementById('modal-title').textContent   = title;
    document.getElementById('modal-content').textContent = content.replace(/\\n/g, '\n');
    document.getElementById('modal-date').textContent    = '📅 ' + date;
    const overlay = document.getElementById('notice-modal');
    overlay.style.display = 'flex';
}

function closeNoticeModal() {
    document.getElementById('notice-modal').style.display = 'none';
}

/* ─── ESC 키로 모달 닫기 ─── */
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeNoticeModal();
});
