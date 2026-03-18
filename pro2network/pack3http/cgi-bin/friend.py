def friend():
    # -*- coding: utf-8 -*-   
    # 한글 깨짐 현상 해결 - 위 명령 안 먹으면 아래 방법 사용
    import sys
    sys.stdout.reconfigure(encoding='utf-8')   

    import os
    import urllib.parse

    # REQUEST_METHOD 내의 GET / POST 요청 확인 
    method = os.environ.get("REQUEST_METHOD", "GET")    # GET  → 주소창으로 보냄, POST → 폼으로 숨겨서 보냄
    # 요청 별 
    if method == "POST":
        length = int(os.environ.get("CONTENT_LENGTH", 0))       # 데이터 글자 수
        body = sys.stdin.read(length)                           # 글자 수 만큼 읽기
    else:       # GET 일 때
        body = os.environ.get("QUERY_STRING", "")

    # 전달된 문자열을 딕셔너리 형태로 변환
    params = urllib.parse.parse_qs(body)
    # 딕셔너리에서 값 가져오기, 값이 없을 경우 기본 값은 ""
    irum = params.get("name", [""])[0]
    junhwa = params.get("phone", [""])[0]
    gen = params.get("gen", [""])[0]

    print("Content-Type: text/html; charset=utf-8")
    print()
    print("""
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>world</title>
    </head> 
    <body>
        입력한 값은 : 이름은 {0} 전화는 {1} 성별은 {2} 
    </body>
    </html>
    """.format(irum, junhwa, gen))

if __name__ == '__main__':
    friend()