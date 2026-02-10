# (첨도, 왜도, 편차)가 큰 데이터 분포 개선을 위한 로그변환
import math

class LogScaling:
    def __init__(self, offset:float=1.0):
        self.offset = offset
    def transform(self,x_list:list[float]):        # Log 변환
        return [math.log(x+self.offset)for x in x_list]
    def inverse_trans(self,x_list:list[float]):    # Log 역변환
        return [math.exp(x_log)-self.offset for x_log in x_list]


def main():
    data = [10.01, 100.02, 1000.03, 10000.04]               # 편차가 큰 데이터
    log_trans = LogScaling(offset=1.0)

    data_log_scaled = log_trans.transform(data)
    reversed_data = log_trans.inverse_trans(data_log_scaled)
    reversed_data_round = [round(val,2) for val in reversed_data]

    print('원본 자료 : ',data)
    print('로그변환 자료 : ',data_log_scaled)
    print('역변환 자료 : ',reversed_data_round)

if __name__ == '__main__':
    main()
