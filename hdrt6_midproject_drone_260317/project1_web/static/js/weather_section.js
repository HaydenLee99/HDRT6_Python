/* ============================================================
weather_section.js - 통합 판단 로직 강화 버전
============================================================ */

const DEFAULT_LAT = 37.49985;
const DEFAULT_LON = 127.03383;

// 1. 시간 업데이트
function updateTime(year, month, day, hour) {
    const now = new Date();
    const yyyy = year != null ? String(year).padStart(4, '0') : String(now.getFullYear());
    const mm = month != null ? String(month).padStart(2, '0') : String(now.getMonth() + 1).padStart(2, '0');
    const dd = day != null ? String(day).padStart(2, '0') : String(now.getDate()).padStart(2, '0');
    const hh = hour != null ? String(hour).padStart(2, '0') : '00';
    const el = document.getElementById('weather-time');
    if (el) el.textContent = `업데이트: ${yyyy}.${mm}.${dd} ${hh}:00 기준`;
}

// 2. 통합 판단 함수 (가장 중요!)
function evaluateFlightStatus(weatherData, zoneType) {
    // Flask에서 전달된 드론 무게 (없으면 null)
    const weight = (typeof USER_DRONE_WEIGHT !== 'undefined' && USER_DRONE_WEIGHT !== null) ? parseFloat(USER_DRONE_WEIGHT) : null;

    // ── [1순위] 구역 기반 규칙 ──────────────────────────────
    if (zoneType === 'forbidden') {
        return { status: '비행 금지', reason: '비행금지구역(RK P)입니다. 기상과 관계없이 승인 없는 비행은 불가합니다.', level: 'ng' };
    }
    if (zoneType === 'restricted') {
        return { status: '비행 승인 필요', reason: '비행제한구역(RK R)입니다. 관할 기관의 승인을 먼저 확인하세요.', level: 'ng' };
    }

    // ── [2순위] 드론 기체 제원(무게) 규칙 ─────────────────────
    if (weight !== null) {
        if (weight > 25) {
            return { status: '비행 승인+자격 필수', reason: `기체 중량 ${weight}kg: 25kg 초과 기체는 비행 승인 및 조종자 증명이 필수입니다.`, level: 'ng' };
        }
        if (weight > 7) {
            return { status: '비행 전 승인 대상', reason: `기체 중량 ${weight}kg: 7kg 초과 기체는 비행 전 신고 및 승인이 필요합니다.`, level: 'warn' };
        }
        if (weight > 2 && zoneType === 'danger') {
            return { status: '비행 위험 주의', reason: `기체 중량 ${weight}kg: 위험구역 내 2kg 초과 기체 비행은 각별히 주의하십시오.`, level: 'warn' };
        }
    }

    // ── [3순위] 날씨 기반 판단 (일반 구역 및 가벼운 기체) ────────
    const ws = weatherData.status; // '비행 가능', '비행 주의', '비행 불가'
    if (ws === '비행 가능') {
        if (zoneType === 'danger') {
            return { status: '비행 주의', reason: '기상은 양호하나 현재 위치는 비행위험구역입니다.', level: 'warn' };
        }
        return { status: '비행 가능', reason: '현재 기상 및 구역 조건에서 안전한 비행이 가능합니다.', level: 'ok' };
    } else {
        const level = (ws === '비행 주의') ? 'warn' : 'ng';
        return { status: ws, reason: weatherData.reason, level: level };
    }
}

// 3. 패널 갱신
function updateWeatherPanel(data, zoneType = 'normal') {
    if (!data.ok) {
        document.getElementById('status-title').textContent = '날씨 조회 실패';
        return;
    }

    const judgment = evaluateFlightStatus(data, zoneType);

    const iconEl = document.getElementById('status-icon');
    const titleEl = document.getElementById('status-title');

    // SVG 아이콘 — 이모지 대신 사용하여 정중앙 정렬 보장
    const iconMap = {
        ok:   `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="22" height="22"><path d="M21 16v-2l-8-5V3.5A1.5 1.5 0 0 0 11.5 2 1.5 1.5 0 0 0 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z" fill="currentColor"/></svg>`,
        warn: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="22" height="22"><path d="M12 2L1 21h22L12 2zm0 3.5L20.5 19h-17L12 5.5zM11 10v4h2v-4h-2zm0 6v2h2v-2h-2z" fill="currentColor"/></svg>`,
        ng:   `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="22" height="22"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`
    };
    const classMap = { ok: 'status-ok', warn: 'status-warn', ng: 'status-ng' };

    iconEl.innerHTML = iconMap[judgment.level];
    iconEl.className = 'status-icon ' + classMap[judgment.level];
    titleEl.textContent = judgment.status;
    titleEl.className = 'status-title ' + judgment.level;
    document.getElementById('status-reason').textContent = judgment.reason;

    // 풍향 숫자(deg) → 한글 방위 변환
    function degToDir(deg) {
        if (deg == null) return '';
        const dirs = ['북','북동','동','남동','남','남서','서','북서'];
        return dirs[Math.round(deg / 45) % 8];
    }
    const windDir  = (data.wind_dir != null) ? degToDir(data.wind_dir) : '';
    const windText = (data.wind != null)
        ? `${data.wind} m/s${windDir ? ' (' + windDir + ')' : ''}`
        : '-';

    // ── 날씨 이모지 결정 ──
    function getWeatherIcon(rain, wind, sunrise, sunset) {
        const rain_val = parseFloat(rain) || 0;
        const wind_val = parseFloat(wind) || 0;

        // 현재 시각이 야간(일몰~일출)인지 판단
        let isNight = false;
        if (sunrise && sunset) {
            const now = new Date();
            const [srH, srM] = sunrise.split(':').map(Number);
            const [ssH, ssM] = sunset.split(':').map(Number);
            const nowMin  = now.getHours() * 60 + now.getMinutes();
            const srMin   = srH * 60 + srM;
            const ssMin   = ssH * 60 + ssM;
            isNight = nowMin < srMin || nowMin > ssMin;
        }

        if (rain_val > 5)               return '⛈';
        if (rain_val > 0)               return '🌧';
        if (wind_val >= 4)              return '🌬️';
        if (isNight)                    return '🌙';
        if (rain_val === 0 && wind_val <= 1) return '☀️';
        return '⛅';
    }

    const weatherIcon = getWeatherIcon(data.rain, data.wind, data.sunrise, data.sunset);
    const iconElWeather = document.getElementById('weather-icon');
    if (iconElWeather) iconElWeather.textContent = weatherIcon;

    // ── 메인 헤더 (풍속 + 강수 요약) ──
    document.getElementById('weather-wind-main').textContent = windText;
    document.getElementById('weather-rain-main').textContent = (data.rain > 0) ? `강수 ${data.rain}mm` : '강수 없음';
    document.getElementById('weather-stn').textContent = '📍 ' + data.stn_name;
    updateTime(data.year, data.month, data.day, data.hour);

    // ── 하단 그리드: 바람 / 강수량 / 일출 / 일몰 ──
    const windEl    = document.getElementById('info-wind');
    const rainEl    = document.getElementById('info-rain');
    const sunriseEl = document.getElementById('info-sunrise');
    const sunsetEl  = document.getElementById('info-sunset');

    if (windEl)    windEl.textContent    = windText;
    if (rainEl)    rainEl.textContent    = (data.rain != null && data.rain > 0) ? `${data.rain}mm` : '없음';
    if (sunriseEl) sunriseEl.textContent = data.sunrise || '-';
    if (sunsetEl)  sunsetEl.textContent  = data.sunset  || '-';
}

// 4. API 호출 (하나만 남기고 중복 삭제!)
async function fetchWeather(lat, lon, zoneType = 'normal') {
    try {
        const res = await fetch(`/api/weather?lat=${lat}&lon=${lon}`);
        const data = await res.json();
        updateWeatherPanel(data, zoneType);
    } catch (e) {
        console.error('날씨 API 오류:', e);
    }
}

// 5. 초기화
document.addEventListener('DOMContentLoaded', () => {
    updateTime();
    fetchWeather(DEFAULT_LAT, DEFAULT_LON); 
    window.onMapClickWeather = fetchWeather; 
});