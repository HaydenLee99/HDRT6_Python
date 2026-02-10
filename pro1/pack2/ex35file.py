# with 구문 사용 - 내부적으로 close()
try:
    with open('ftext3.txt', mode='w', encoding='utf-8') as fobj1:
        fobj1.write('파이썬에서 문서저장\n')
        fobj1.write('with 구문은\n')
        fobj1.write('명시적 close()할 필요가 없다\n')
        fobj1.write('왜냐하면 자동으로 해주니깐\n')
    print('\n[system] 파일 저장 성공.')

    with open('ftext3.txt', mode='r', encoding='utf-8') as fobj2:
        print(fobj2.read())
    print('\n[system] 파일 읽기 성공.')
except Exception as e:
    print(e)

print('\n\n피클링(일반 객체 및 복합 객체 파일 처리)')
import pickle
try:
    dictData = {'tomy':'010-1234-5678', 'Judro':'010-1234-9876'}
    listData = ['마우스', '키보드']
    tupleData = (dictData, listData)
    with open('hello.dat', mode = 'wb') as fobj3:
        pickle.dump(tupleData, fobj3)               # pickle.dump(대상, 파일객체)
        pickle.dump(listData, fobj3)
        
    print('\n[system] 파일 저장 성공.')
    with open('hello.dat', mode = 'rb') as fobj4:
        a, b = pickle.load(fobj4)
        print('a :',a)
        print('b :',b)
        c = pickle.load(fobj4)
        print('c :',c)
    print('\n[system] 파일 읽기 성공.')
except Exception as e:
    print(e)