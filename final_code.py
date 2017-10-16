import requests
import json
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder

# url：只需替换keyword（1 如果为Null则跳过 2 如果第一个成功则跳过第二个）
def get_url(self, keyword):
    url_pre = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword='
    url_pro = '&templateId=&page=1&pageSize=10'
    # data = str(int(time.time() * 1000))
    url = url_pre + keyword + url_pro
    return url

# 如果提取到网页上特定字段："'results' = []" 则为不成功
def get_webkey(self, url):
    # url = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword=912101127157655762&templateId=&page=1&pageSize=10'
    data = requests.get(url)
    data1 = data.json()
    a = data1.get('data')
    b = a.get('results')
    # print("check = ", check)
    if b != []:
        b = url[61:79]
        return b
    elif b == []:
        return 0

sql_get = """
select * from

"""

sql_create = """

"""

sql_insert = """

"""

if __name__ == '__main__':
    server = SSHTunnelForwarder(
        
    )
    server.start()
    conn = pymysql.connect(
       
    )
    cur = conn.cursor()
    try:
        cur.execute(sql_get)
    except:
        print('Fail to get keyword!')

    cur.execute(sql_create)
    # 提交到数据库执行
    conn.commit()

    # 如果第一个成功则跳过第二个，直接返回第一个；如果第一个不成功则换第二个keyword，第二个成功则返回第二个；如果第二个也不成功则返回Null
    # 保存统一社会信用编码&公司名称&地区编码（第3-8位）
    url = get_url(input())

    # df = pd.read_csv("result3.csv", header=None)
    for i in range(len(df)):
        num1 = df.loc[i][2]
        num2 = df.loc[i][3]
        # request_pre = int(time.time()*1000)
        newtable = [df.loc[i][1], -1]
        if num1 != 'NULL':
            url1 = get_url(num1)
            url2 = get_url(num2)
            if get_webkey(url1) != 0:
                checkcode = num1
                zipCode = num1[2:8]
            elif get_webkey(url1) == 0:
                if get_webkey(url2) != 0:
                    checkcode = num2
                    zipCode = num2[2:8]
                elif get_webkey(url2) == 0:
                    checkcode = 'NULL'
                    zipCode = 'NULL'
        else:
            checkcode = 'NULL'
            zipCode = 'NULL'
        newtable.append(checkcode)
        newtable.append(zipCode)

        try:
            # 执行sql语句
            cur.execute(sql_insert)
            # 提交到数据库执行
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()

        # cur.execute(testsql,data)
        # conn.commit()
        cur.close()
        # 关闭数据库连接
        conn.close()
        # Make sure to call server.stop() when you want to disconnect
        server.stop()
