import sys
sys.stdout.reconfigure(encoding='utf-8')

import MySQLdb
import pickle

def dataLoad():
    with open(r"cgi-bin/mydb.dat", mode="rb") as obj:
        config = pickle.load(obj)
    return config

def sangpum(config):
    try:
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("<html><body><b><h1>** 상품 정보 **</h1></b>")
        print("<table border='1'>")
        print("<tr><td>코드</td><td>상품명</td><td>수량</td><td>단가</td></tr>")

        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        cursor.execute("select * from sangdata order by code desc")
        datas = cursor.fetchall()
        for code, sang, su, dan in datas:
            print("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(code, sang, su, dan))
        print("</table>")
        print("</body></html>")

    except Exception as e:
        print('err : ', e)

    finally:
        try: cursor.close()
        except: pass
        try: conn.close()
        except: pass


if __name__ == "__main__":
    data = dataLoad()
    sangpum(data)