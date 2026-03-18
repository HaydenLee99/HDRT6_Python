def helloWorld():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ss = '파이썬 자료 출력'
    ss2 = 487 + 13
    # Client browser로 출력
    print("Content-Type: text/html; charset=utf-8\n")
    print("<html><body>")
    print("<b>안녕, 파이썬 모듈로 작성한 문서야</b><br/>")
    print("파이썬 변수 값1 : %s <br/>"%(ss,))
    print("파이썬 변수 값2 : %d"%(ss2,))
    print("</body></html>")

if __name__ == '__main__':
    helloWorld()