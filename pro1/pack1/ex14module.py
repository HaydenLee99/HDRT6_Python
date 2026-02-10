# Module : 소스 코드의 재사용을 가능하게 하며, 소스 코드를 하나의 이름 공간으로 구분하고 관리
# 하나의 파일 = 하나의 모듈
# 표준 모듈, 사용자 작성 모듈, 제 3자 모듈(third party)로 구분 가능

import sys
print(sys.path)

import calendar
calendar.setfirstweekday(6)
calendar.prmonth(2026,3)
del calendar

import random
print(random.random())
print(random.randrange(1,10,3))
from random import *
print(random())
print(randrange(1,10,3))



print('\nend'); sys.exit(0)