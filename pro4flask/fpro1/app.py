from flask import Flask     # 웹서버 생성에 필요
# Python Application Server : py Program code를 실행해서 요청을 처리하는 서버

# Flask 기본 서버는 개발용 학습용으로 light-weight server
# 실무용 서버(WSGI) : gunicorn(리눅스), waitress(윈도우), nginx ... 등등

# waitress 서버를 사용한다면..
from waitress import serve

app = Flask(__name__)       # Flask 객체 생성. __name__ : 현재 모듈의 이름

@app.route("/")             # URL mapping(routing). Client 요청이 '/' 일 때, 아래 함수 수행
def abc():                  # 클라이언트 요청을 처리하는 함수
    return "<h1>안녕하세요</h1> 반갑수다"

@app.route("/about")
def about():
    return "플라스크를 소개하자면..."

@app.route("/user/<name>")  # URL에 변수를 담아 요청
def user(name):
    return f"내 친구 {name}"




if __name__ == "__main__":
    # Flask server
    # app.run()
    # app.run(debug=True, host='0.0.0.0', port=5000)       # debug True 하면 watchdog 켜짐. 이제 저장할 때마다 라이브로 서버에 반영.
    
    # waitress server
    print("web server 서비스 시작")
    serve(app=app, host='0.0.0.0', port=8000)

