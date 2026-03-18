# 우편 정보 파일 dataRoad.txt 읽기
def roadProcess():
    dongname = input('동 이름 입력:')
    # dongname = '도곡'
    try:
        with open(r'dataRoad.txt', mode = 'r', encoding = 'euc-kr') as f:
            line = f.readline()
            # lines = line.split(sep = '\t')
            # print(lines)
            while line:
                lines = line.split('\t')
                if lines[3].startswith(dongname):
                    print('우편번호:'+lines[0]+', '+lines[1]+' '+lines[2]+' '+lines[3])
                line = f.readline()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    roadProcess()