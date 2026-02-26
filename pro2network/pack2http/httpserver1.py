# http server   :   Web service를 위한 server
# 단순한 http server 구축 - 기본적인 socket 연결 관리

from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7777
handler = SimpleHTTPRequestHandler                      # client의 get 요청에 대해, 문서를 읽어 client로 전송하는 역할
serv = HTTPServer(('127.0.0.1', PORT), handler)         # HTTP server 객체 생성
print('Web service Start...')
serv.serve_forever()                                    # Web service 무한루핑

