# Socket : 프로그램끼리 네트워크로 데이터를 주고받는 통로
#          TCP/IP를 사용하는 프로그래머 인터페이스(Programmer Interface)

# 연결 지향(Socket Type: TCP)
# - TCP/IP 기반
# - 데이터 전송 전 연결 수립
# - 순서 보장, 신뢰성 있음
# - 예시: 웹 브라우징, 이메일, 파일 전송
# - 사용 함수 예시: socket(), bind(), listen(), accept(), connect(), send(), recv()

# 비연결 지향(Socket Type: UDP)
# - UDP 기반
# - 연결 없이 데이터 전송
# - 순서/신뢰성 보장 없음, 속도 빠름
# - 예시: 실시간 스트리밍, 온라인 게임, 라디오/TV 방송
# - 사용 함수 예시: socket(), sendto(), recvfrom()

# socket 통신 확인
import socket

print(socket.getservbyname('http','tcp'))       # HTTP (웹 서비스)      TCP 포트 번호 80 출력
print(socket.getservbyname('ssh','tcp'))        # SSH (원격 접속)       TCP 포트 번호 22 출력
print(socket.getservbyname('ftp','tcp'))        # FTP (파일 전송)       TCP 포트 번호 21 출력
print(socket.getservbyname('smtp','tcp'))       # SMTP (메일 송수신)    TCP 포트 번호 25 출력
print(socket.getservbyname('pop3','tcp'))       # POP3 (e-mail)        TCP 포트 번호 110 출력

# 특정 web server의 IP addr 확인
print(socket.getaddrinfo('www.naver.com', 80, proto=socket.SOL_TCP))