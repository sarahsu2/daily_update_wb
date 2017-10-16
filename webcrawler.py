import requests
import json
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder

# url：只需替换keyword（1 如果为Null则跳过 2 如果第一个成功则跳过第二个）
def get_url(keyword):
    url_pre = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword='
    url_pro = '&templateId=&page=1&pageSize=10'
    keyword = str(keyword)
    # data = str(int(time.time() * 1000))
    url = url_pre + keyword + url_pro
    return url

# 如果提取到网页上特定字段："'results' = []" 则为不成功
def get_webkey(url):

    data = requests.get(url)
    data1 = data.json()
    a = data1.get('data')
    b = a.get('results')
    if b != []:
        b = url[61:79]
        return b
    elif b == []:
        return 0

sql_get = """
select * from TaxationCode
"""

# 在数据库里新建表（不要主键）：统一社会信用编码，公司名称（汉字），地区编码（第3-8位），该公司数据是否拿到（加一个flag initial －1）
# 建表时 charset utf8mb4
sql_create = """
CREATE TABLE CheckedTaxationCode (
companyName CHAR(50),
creditCode CHAR(18),
zipCode CHAR(6),
gotCompanyInfo CHAR(2))
DEFAULT CHARSET=utf8mb4
"""

sql_insert = """
INSERT INTO CheckedTaxationCode(companyName, creditCode, zipCode, gotCompanyInfo)
       VALUES ('%s', '%s', '%s', '%s' )"""

if __name__ == '__main__':
    server = SSHTunnelForwarder(
        'xxx.xx.xxx.xx',
        ssh_username='xxx',
        ssh_password='xxx',
        remote_bind_address=('127.0.0.1', 3306)
    )
    server.start()
    conn = pymysql.connect(
        host='127.0.0.1',
        port=server.local_bind_port,
        user='root',
        password='xxx',
        db='xxx'
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS CheckedTaxationCode")
    try:
        cur.execute(sql_create)
    except:
        print('Fail to create table CheckedTaxationCode!')
    # 需不需要提交到数据库执行？
    # conn.commit()

    # try:
    cur.execute(sql_get)
    data = cur.fetchall()
    for i in range(len(data)):
        taxPersonCode = data[i][0]
        companyName = data[i][1]
        unifiedCreditCodeZero = data[i][2]
        unifiedCreditCodeNotZero = data[0][3]

        # 如果第一个成功则跳过第二个，直接返回第一个；如果第一个不成功则换第二个keyword，第二个成功则返回第二个；如果第二个也不成功则返回Null
        # 保存统一社会信用编码&公司名称&地区编码（第3-8位）
        # num1 = '\'%s\''%unifiedCreditCodeZero
        num1 = str(unifiedCreditCodeZero)
        num2 = unifiedCreditCodeNotZero
        newtable = ['-1']
        name = companyName
        newtable.append(name)
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
            cur.execute(sql_insert%(newtable[1], newtable[2], newtable[3], newtable[0]))
            # 执行数据库操作每步都要数据库db.commit()以后才能操作
            # 提交到数据库执行
            conn.commit()
            print(i)
        except:
            # Rollback in case there is any error
            conn.rollback()
            print('Fail to insert row ', i)
    # except:
    #     print('Fail to reach the next row!')

    cur.close()
    # 关闭数据库连接
    conn.close()
    # Make sure to call server.stop() when you want to disconnect
    server.stop()
