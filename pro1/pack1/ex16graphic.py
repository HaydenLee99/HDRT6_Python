# turtle 모듈(라이브러리)
from turtle import *
p = Pen()
p.color('red','yellow')
p.begin_fill()
while 1:
    p.forward(200)
    p.left(170)
    if abs(p.position()) < 1:
        break

p.end_fill()
input()