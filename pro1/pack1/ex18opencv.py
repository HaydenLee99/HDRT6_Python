# OpenCV (Computer Vision)
# 영상처리, 패턴인식, 주파수 변환 등 컴퓨터비전 알고리즘 지원.

import cv2
print(cv2.__version__)
img1=cv2.imread('./nick.jpg')
print(type(img1))

cv2.imshow('image test', img1)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imwrite('nickandjudy.jpg',img1)
cv2.imwrite('nickandjudy.jpg',img1, [cv2.IMWRITE_JPEG_QUALITY, 50])

img2=cv2.resize(img1,(100,300),interpolation=cv2.INTER_AREA)
cv2.imwrite('nickandjudysize.jpg',img2)
