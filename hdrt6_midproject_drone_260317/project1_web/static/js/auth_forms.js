/* ============================================================
   auth_forms.js
   역할: 로그인 / 회원가입 / 마이페이지 공통 폼 유틸리티
   적용: login.html, register.html, mypage.html
   원본: register.html, mypage.html 내 <script> 블록 통합·추출
============================================================ */

/* ─── 달력 버튼 클릭 → 숨김 date picker 오픈 ─── */
function openBirthPicker() {
    const picker = document.getElementById('birth-picker');
    if (!picker) return;
    try { picker.showPicker(); } catch(e) {}
}

/* ─── 달력에서 날짜 선택 → 텍스트 인풋에 반영 ─── */
document.addEventListener('DOMContentLoaded', function () {
    const picker = document.getElementById('birth-picker');
    if (picker) {
        picker.addEventListener('change', function () {
            const input = document.getElementById('birth-input');
            if (input) input.value = this.value;
        });
    }
});

/* ─── 생년월일 자동 하이픈 (19991231 → 1999-12-31) ─── */
function formatBirth(input) {
    let val = input.value.replace(/[^0-9]/g, '');
    if (val.length <= 4) {
        input.value = val;
    } else if (val.length <= 6) {
        input.value = val.slice(0, 4) + '-' + val.slice(4);
    } else {
        input.value = val.slice(0, 4) + '-' + val.slice(4, 6) + '-' + val.slice(6, 8);
    }
}

/* ─── cm 자동 추가 ─── */
function formatCm(input) {
    let val = input.value.replace(/[^0-9.]/g, '');
    input.value = val ? val + 'cm' : '';
    const pos = val.length;
    input.setSelectionRange(pos, pos);
}

/* ─── 전화번호 자동 하이픈 ─── */
function pmFormatPhone(input) {
    let val = input.value.replace(/[^0-9]/g, '');
    if (val.length <= 3) {
        input.value = val;
    } else if (val.length <= 7) {
        input.value = val.slice(0, 3) + '-' + val.slice(3);
    } else {
        input.value = val.slice(0, 3) + '-' + val.slice(3, 7) + '-' + val.slice(7, 11);
    }
}

/* ─── 토스트 알림 (register 전용) ─── */
function showRegToast(msg) {
    const prev = document.getElementById('reg-toast');
    if (prev) prev.remove();

    const toast = document.createElement('div');
    toast.id = 'reg-toast';
    toast.textContent = msg;
    Object.assign(toast.style, {
        position:    'fixed',
        top:         '28px',
        left:        '50%',
        transform:   'translateX(-50%)',
        background:  'var(--red, #dc2626)',
        color:       '#fff',
        fontFamily:  "'Noto Sans KR', sans-serif",
        fontSize:    '0.82rem',
        fontWeight:  '600',
        padding:     '10px 20px',
        borderRadius: '8px',
        boxShadow:   '0 4px 20px rgba(220,38,38,0.35)',
        zIndex:      '9999',
        whiteSpace:  'nowrap',
        animation:   'toastIn 0.25s ease',
    });
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s';
        toast.style.opacity    = '0';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

/* ─── 입력 필드 에러 표시 / 해제 ─── */
function setFieldError(name, hasError) {
    const input = document.querySelector(`[name="${name}"]`);
    if (!input) return;
    input.style.borderColor = hasError ? '#dc2626' : '';
    input.style.boxShadow   = hasError ? '0 0 0 3px rgba(220,38,38,0.1)' : '';
}

/* ─── 회원가입 폼 유효성 검사 ─── */
document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('register-form');
    if (!registerForm) return;

    const requiredFields = [
        { name: 'name',     label: '이름' },
        { name: 'birth',    label: '생년월일' },
        { name: 'phone',    label: '전화번호' },
        { name: 'login_id', label: '아이디' },
        { name: 'password', label: '비밀번호' },
    ];

    // 입력 시 빨간 테두리 해제
    requiredFields.forEach(f => {
        const input = document.querySelector(`[name="${f.name}"]`);
        if (input) input.addEventListener('input', () => setFieldError(f.name, false));
    });

    registerForm.addEventListener('submit', function (e) {
        let firstEmpty = null;

        requiredFields.forEach(f => setFieldError(f.name, false));

        for (const field of requiredFields) {
            const input = document.querySelector(`[name="${field.name}"]`);
            if (!input || !input.value.trim()) {
                setFieldError(field.name, true);
                if (!firstEmpty) firstEmpty = { input, label: field.label };
            }
        }

        if (firstEmpty) {
            e.preventDefault();
            showRegToast(`⚠️ ${firstEmpty.label}을(를) 입력해 주세요.`);
            firstEmpty.input.focus();
        }
    });
});
