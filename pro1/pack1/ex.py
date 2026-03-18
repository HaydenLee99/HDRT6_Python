# 입력 함수 그대로 사용할 것
# 문1
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas

def processfunc(datas):
    tmp = [0,0,0]
    for i in range(len(datas)):
        datas[i][3] = 2026 - datas[i][3]
        if 0 <= datas[i][3] <= 3:
            tmp[i] = datas[i][2] + 150000
            datas[i].append(150000)
            if 3000000 <= tmp[i]:
                datas[i].append(int(tmp[i]*0.5))
                datas[i].append(tmp[i]-int(tmp[i]*0.5))
            elif 2000000<= tmp[i] < 3000000:
                datas[i].append(int(tmp[i]*0.3))
                datas[i].append(tmp[i]-int(tmp[i]*0.3))
            else:
                datas[i].append(int(tmp[i]*0.15))
                datas[i].append(tmp[i]-int(tmp[i]*0.15))
        elif 4 <= datas[i][3] <= 8:
            tmp[i] = datas[i][2] + 450000
            datas[i].append(450000)
            if 3000000 <= tmp[i]:
                datas[i].append(int(tmp[i]*0.5))
                datas[i].append(tmp[i]-int(tmp[i]*0.5))
            elif 2000000<= tmp[i] < 3000000:
                datas[i].append(int(tmp[i]*0.3))
                datas[i].append(tmp[i]-int(tmp[i]*0.3))
            else:
                datas[i].append(int(tmp[i]*0.15))
                datas[i].append(tmp[i]-int(tmp[i]*0.15))
        else:
            tmp[i] = datas[i][2] + 1000000
            datas[i].append(1000000)
            if 3000000 <= tmp[i]:
                datas[i].append(int(tmp[i]*0.5))
                datas[i].append(tmp[i]-int(tmp[i]*0.5))
            elif 2000000<= tmp[i] < 3000000:
                datas[i].append(int(tmp[i]*0.3))
                datas[i].append(tmp[i]-int(tmp[i]*0.3))
            else:
                datas[i].append(int(tmp[i]*0.15))
                datas[i].append(tmp[i]-int(tmp[i]*0.15))
    return datas[0],datas[1],datas[2]
label=['사번','이름','기본급','근무년수','근속수당','공제액','수령액'] 
print(*label)
print('------------------------------------------------')
for i in range(3):
    print(*processfunc(inputfunc())[i])
print()

#문2 
def inputfunc2():
    datas2 = [
        "새우깡,15",
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas2

def processfunc2(datas2):
    ans = []
    tmp = []
    cnt = [0,0,0]
    for i in range(len(datas2)):
        if datas2[i].split(',')[0] == '새우깡':
            tmp.append(datas2[i].split(',')[0])
            tmp.append(int(datas2[i].split(',')[1]))
            tmp.append(450)
            tmp.append(int(datas2[i].split(',')[1])*450)
            ans.append(tmp)
            cnt[0] = cnt[0] + int(datas2[i].split(',')[1])
            tmp=[]
        elif datas2[i].split(',')[0] == '감자깡':
            tmp.append(datas2[i].split(',')[0])
            tmp.append(int(datas2[i].split(',')[1]))
            tmp.append(300)
            tmp.append(int(datas2[i].split(',')[1])*300)
            ans.append(tmp)
            cnt[1] = cnt[1] + int(datas2[i].split(',')[1])
            tmp=[]
        elif datas2[i].split(',')[0] == '양파깡':
            tmp.append(datas2[i].split(',')[0])
            tmp.append(int(datas2[i].split(',')[1]))
            tmp.append(350)
            tmp.append(int(datas2[i].split(',')[1])*350)
            ans.append(tmp)
            cnt[2] = cnt[2] + int(datas2[i].split(',')[1])
            tmp=[]
    return ans, cnt


label2=['상품명','수량','단가','금액'] 
print(*label2)
print('-----------------------')
for i in range(len(processfunc2(inputfunc2())[0])):
    print(*processfunc2(inputfunc2())[0][i])

print('\n소계')
print(f'새우깡 : {processfunc2(inputfunc2())[1][0]}건\t소계액 : {450*processfunc2(inputfunc2())[1][0]}원')
print(f'감자깡 : {processfunc2(inputfunc2())[1][1]}건\t소계액 : {300*processfunc2(inputfunc2())[1][1]}원')
print(f'양파깡 : {processfunc2(inputfunc2())[1][2]}건\t소계액 : {350*processfunc2(inputfunc2())[1][2]}원')
print('총계')
print(f'총 건수 : {sum(processfunc2(inputfunc2())[1])}')
print(f'총 액 : {450*processfunc2(inputfunc2())[1][0] + 300*processfunc2(inputfunc2())[1][1] \
               + 350*processfunc2(inputfunc2())[1][2]}')

exit(0)