# 서버
from socket import *
import sys

HOST = '127.0.0.1'
PORT = 7788

serversock = socket(AF_INET,SOCK_STREAM)     # socket 객체 생성

def socket1():
    try:
        serversock.bind((HOST, PORT))            # socket을 특정 컴과 binding
        serversock.listen(5)                     # Clinet와 연결 정보 수. Listener 설정
        print('서버 서비스 중...')

        while True:
            conn, addr = serversock.accept()     # 수동적 연결 대기
            print('clent info : ', addr[0], ' ', addr[1])
            print(conn.recv(1024).decode())
            conn.send(('from server : ' + str(addr[1]) + '너도 잘 지내').encode('utf_8'))

    except Exception as e:
        print('err : ', e)
        sys.exit()
    finally:
        if conn:
            conn.close()
        if serversock:
            serversock.close()

if __name__ == '__main__':
    socket1()