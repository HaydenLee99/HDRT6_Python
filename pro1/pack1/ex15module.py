# pack1\ex15module.py - main
print('사용자 정의 모듈 처리하기---')

print('\n경로 지정 방법 1 : import 모듈명')
import pack1.mymod1

print(dir(pack1.mymod1))
print(pack1.mymod1.__file__)
print(pack1.mymod1.__name__)

list1 = [1,2]
list2 = [2,3,4]
pack1.mymod1.listHap(list1, list2)
if __name__ == '__main__':
    print('나는 main module 히히')

print('\n경로 지정 방법 2 : from 모듈명 import 함수명(메소드명) or 전역변수')
from pack1.mymod1 import tot,kbs
from pack1.mymod1 import mbc as 바보
kbs()
바보()
print
print('tot : ', tot)

print('\n경로 지정 방법 3 : import 하위패키지.모듈명')
import pack1.subpack.sbs
pack1.subpack.sbs.sbsHi()

import pack1.subpack.sbs as hi
hi.sbsHi()

print('\n경로 지정 방법 4 : 현재 패키지와 동등한 다른 패키지 모듈 읽기')
# import ../pack1_other.mymod2
from pack1_other import mymod2
print(mymod2.hapFunc(4,3))      # 커맨드에서 python -m pack1.ex15module 로 실행.

import mymod3
result = mymod3.gopFunc(4,3)
print('path가 설정된 곳의 모듈 읽기 - result: ',result)
print(result)