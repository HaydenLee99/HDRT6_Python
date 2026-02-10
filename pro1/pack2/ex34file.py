# 파일 입출력 처리
import os

try:
    # print(os.getcwd())  # 현재 path
    f1 = open('ftext.txt', mode = 'r', encoding='utf-8')        # mode : "r" "w" "a" "b"
    print(f1.read())
    f1.close()
    print('\n[system] 파일 읽기 성공.')

    f2 = open('ftext2.txt', mode='w', encoding = 'utf-8')
    f2.write('내 사랑아\n')
    f2.write('호랑이, 터보, 국종이')
    f2.close()
    print('\n[system] 파일 저장 성공.')

    f3 = open('ftext2.txt', mode = 'a', encoding='utf-8')
    f3.write('\n국종이\n꾹형사\n한남자')
    f3.close()
    print('\n[system] 파일 추가 성공.')

    f4 = open('ftext2.txt', mode = 'r', encoding='utf-8')
    print(f4.read())
    f4.close()
    print('\n[system] 파일 읽기 성공.')
except Exception as e:
    print('파일 처리 오류 : ', e)


