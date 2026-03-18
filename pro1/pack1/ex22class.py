# 클래스는 새로운 타입을 만들어 자원을 공유 가능

# class Singer:
#     title_song = '빛나라 샤이니'

#     def sing(self):
#         msg = '노래는 '
#         print(msg, self.title_song)

from ex22singer import Singer
bts = Singer()      # 생성자 호출해 객체 생성 후 주소 bts에 치환
bts.sing()
print(type(bts))
bts.title_song = "Permission to Dance"
bts.sing()
bts.co = '빅히트 ENT'
print('소속사 : ',bts.co)

ive = Singer()
ive.sing()
print(type(ive))
ive.co = '??? ENT'
print('소속사 : ',ive.co)
Singer.title_song = '아 샤인 선샤인'
bts.sing()
ive.sing()

niceGroup = ive
niceGroup.sing()

