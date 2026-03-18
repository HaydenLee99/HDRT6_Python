# 일회용 서버
from socket import *

serversock = socket(AF_INET,SOCK_STREAM)        # socket 객체 생성
serversock.bind(('127.0.0.1', 8888))            # socket을 특정 컴과 binding
serversock.listen(5)                            # Clinet와 연결 정보 수. Listener 설정
print('서버 서비스 중...')

conn, addr = serversock.accept()                # 수동적 연결 대기
print('Client addr : ', addr)
print('from Clent msg : ', conn.recv(1024).decode())
conn.close()
serversock.close()