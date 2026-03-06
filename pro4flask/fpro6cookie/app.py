from flask import Flask, render_template_string, request, make_response, redirect, url_for
# render_template : 문자열로 작성한 jinja 템플릿을 렌더링 해 HTML로 반환
# request: 클라이언트 요청 정보 접근
# make+response : 응답 객체 직접 생성
# redirect : 다른 URL로 이동
# url_for: 라우트 함수 이름으로 URL을 안전하게 생성하는 함수
app = Flask(__name__)
# cookie는 브라우저에 저장되는 작은 키-값 데이터이고, 서버가 클라이언트와 계속 연결 상태를 유지하는 것처럼 보이게 해줌
# 서버가 쿠키를 설정 -> 브라우저가 저장 -> 다음 요청 부터는 브라우저가 자동으로 함께 전송
HOME_HTML = """
    <h2>Flask Cookie Test</h2>
    <form action="/set_cookie" method="post">
        쿠키 값 : 
        <input type="text" name="name" placeholder="예: hong">
        <button type="submit">쿠키 저장</button>
    </form>
    <p>
        <a href="/read_cookie">쿠키 읽기</a> |
        <a href="/delete_cookie">쿠키 삭제</a>
    </p>
"""
@app.get("/")
def home():
    return render_template_string(HOME_HTML)

@app.post("/set_cookie")
def set_cookie():
    # 쿠키 저장
    name = request.form.get("name", "unknown")
    # 클라이언트에 쿠키를 심으려면 응답 객체가 필요
    # 먼저 read_cookie page로 이동하라는 객체를 만들고 redirect 객체를 만들고 그 응답에 따라 쿠키를 추가한 뒤 브라우저에 되돌려줌
    resp = make_response(redirect(url_for("read_cookie")))  # url_for해서 함수명 read_cookie를 불러준다. url_for가 없다면 /read_cookie를 불러온다
    resp.set_cookie(         # 브라우저에 쿠키를 저장
        key = "cookiename",  # 쿠키 이름
        value = name,        # 사용자가 입력한 쿠키값
        max_age = 60*5,      # 쿠키 유효 시간 (sec)
        httponly = True,     # JS에서 document.cookie로 접근 불가 (보안)
        samesite = "Lax"     # CSRF 공격 방지용
    )
    return resp              # 쿠키가 포함된 응답을 브라우저로 반환
    # 브라우저는 쿠키를 클라이언트 컴퓨터에 저장하고, redirect 요청에 따라 read_cookie로 요청함

@app.get("/read_cookie")
def read_cookie():
    # 브라우저가 요청에 실어 보낸 모든 쿠키 중에서 내 서버가 만든 쿠키를 꺼냄
    # 없으면 None 반환(첫방문/만료/삭제)
    name=request.cookies.get("cookiename")
    # 읽어온 쿠키 html로 출력하기
    return f"""
        <h3> 쿠키 읽기 </h3>
        <p>쿠키 값 : {name}</p>
        <a href="/">홈으로</a>
    """

@app.get("/delete_cookie")
def delete_cookie():
    # 쿠키 삭제 후 홈(/)으로 이동하기 위한 redirext 응답을 만듦
    resp = make_response(redirect(url_for("home")))
    resp.delete_cookie("cookiename")
    return resp

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)