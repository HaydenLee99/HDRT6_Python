def my():
    import os
    import urllib.parse
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    # 주소?이름=값&이름=값&이름=값 정보를 쿼리 스트링으로 가져오기
    query = os.environ.get("QUERY_STRING","")
    # 전달된 문자열을 딕셔너리 형태로 변환
    params = urllib.parse.parse_qs(query)
    # 딕셔너리에서 값 가져오기, 값이 없을 경우 기본 값은 ""
    irum = params.get("name",[""])[0]
    nai = params.get("age",[""])[0]

    # Client browser로 출력
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <html lang="kr">
    <head>
        <meta charset="UTF-8">
        <title>world</title>
    </head>
    <body>
    정보 : {0}의 나이는 {1} 이다.
    </body>
    </html>
    """.format(irum,nai))

if __name__ == '__main__':
    my()