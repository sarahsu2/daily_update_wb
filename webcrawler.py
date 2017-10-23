import requests
import json
import pymysql
from sshtunnel import SSHTunnelForwarder
import time

# url：只需替换keyword（1 如果为Null则跳过 2 如果第一个成功则跳过第二个）
def get_url(keyword):
    url_pre = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword='
    url_pro = '&templateId=&page=1&pageSize=10'
    # print(keyword)
    # data = str(int(time.time() * 1000))
    url = url_pre + keyword + url_pro
    return url

# 如果提取到网页上特定字段："'results' = []" 则为不成功
def get_webkey(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    data = requests.get(url, headers=headers)
    data1 = data.json()
    # print (data1)
    a = data1.get('data')
    b = a.get('results')
    if b != []:
        c = url[61:79]
        return c
    elif b == []:
        return 0

sql_get = """
SELECT * FROM TaxationCode
"""

# 在数据库里新建表（不要主键）：统一社会信用编码，公司名称（汉字），地区编码（第3-8位），该公司数据是否拿到（加一个flag initial －1）
# 建表时 charset utf8mb4
sql_create = """
CREATE TABLE CheckedTaxationCode (
companyName CHAR(50),
creditCode CHAR(18),
zipCode CHAR(6),
gotCompanyInfo CHAR(2),
code1 CHAR(18),
code2 CHAR(18),
code3 CHAR(18),
mark CHAR(1))
DEFAULT CHARSET=utf8mb4
"""

sql_insert = """
INSERT INTO CheckedTaxationCode(companyName, creditCode, zipCode, gotCompanyInfo, code1, code2, code3, mark)
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

sql_getMark = """
SELECT * FROM CheckedTaxationCode WHERE 'mark' = 1
"""

def process_data_after_interruption(data):
    # for i in range(3, len(data)):
    for i in range(56640, len(data)):
        # print(i)
        # print(data[i])
        taxPersonCode = data[i][0]
        companyName = data[i][1]
        unifiedCreditCodeZero = data[i][2]
        unifiedCreditCodeNotZero = data[i][3]
        unifiedCreditCodeAllZero = data[i][4]
        # print((data[i][0]))
        try:
            # 如果第一个成功则跳过第二个，直接返回第一个；如果第一个不成功则换第二个keyword，第二个成功则返回第二个；如果第二个也不成功则返回Null
            # 保存统一社会信用编码&公司名称&地区编码（第3-8位）
            # num1 = '\'%s\''%unifiedCreditCodeZero
            num1 = unifiedCreditCodeZero
            num2 = unifiedCreditCodeNotZero
            num3 = unifiedCreditCodeAllZero
            newtable = ['-1']
            name = companyName
            newtable.append(name)

            # 跑50条休息5秒
            # if i % 50 == 0:
            #     time.sleep(5)

            if num1 != 'NULL':
                # print("True")
                url1 = get_url(num1)
                # print(url1)
                url2 = get_url(num2)
                url3 = get_url(num3)
                # print(get_webkey(url1))
                if get_webkey(url1) != 0:
                    checkcode = num1
                    zipCode = num1[2:8]
                    # print("url1 != 0")
                elif get_webkey(url1) == 0:
                    if get_webkey(url2) != 0:
                        checkcode = num2
                        zipCode = num2[2:8]
                        # print("url2 != 0")
                    elif get_webkey(url2) == 0:
                        if get_webkey(url3) != 0:
                            checkcode = num3
                            zipCode = num3[2:8]
                        elif get_webkey(url3) == 0:
                            checkcode = 'NULL'
                            zipCode = 'NULL'
                            # print("url3 == 0")
            elif num1 == 'NULL':
                checkcode = 'NULL'
                zipCode = 'NULL'
                # print("url1 == NULL")

            newtable.append(checkcode)
            newtable.append(zipCode)
            newtable.append(num1)
            newtable.append(num2)
            newtable.append(num3)
            newtable.append('0')
            # print(newtable)

            try:
                # 执行sql语句
                cur.execute(sql_insert%(newtable[1], newtable[2], newtable[3], newtable[0], newtable[4], newtable[5], newtable[6], newtable[7]))
                # 执行数据库操作每步都要数据库db.commit()以后才能操作
                # 提交到数据库执行
                conn.commit()
                print(i)
            except:
                # Rollback in case there is any error
                conn.rollback()
                print('Fail to insert row ', i)
        except:
            # print('Fail to reach row', i)
            cur.execute(sql_insert%(companyName, 'NULL', 'NULL','-1', unifiedCreditCodeZero, unifiedCreditCodeNotZero, unifiedCreditCodeAllZero, '1'))
            conn.commit()
            pass

def process_data(data):
    for i in range(len(data)):
        # print(i)
        # taxPersonCode = data[i][0]
        companyName = data[i][1]
        unifiedCreditCodeZero = data[i][4]
        unifiedCreditCodeNotZero = data[i][5]
        unifiedCreditCodeAllZero = data[i][6]
        # print((data[i][0]))
        try:
            # 如果第一个成功则跳过第二个，直接返回第一个；如果第一个不成功则换第二个keyword，第二个成功则返回第二个；如果第二个也不成功则返回Null
            # 保存统一社会信用编码&公司名称&地区编码（第3-8位）
            # num1 = '\'%s\''%unifiedCreditCodeZero
            num1 = unifiedCreditCodeZero
            num2 = unifiedCreditCodeNotZero
            num3 = unifiedCreditCodeAllZero
            newtable = ['-1']
            name = companyName
            newtable.append(name)

            # 跑50条休息5秒
            # if i % 50 == 0:
            #     time.sleep(5)

            if num1 != 'NULL':
                # print("True")
                url1 = get_url(num1)
                url2 = get_url(num2)
                url3 = get_url(num3)
                # get_webkey(url1)
                if get_webkey(url1) != 0:
                    checkcode = num1
                    zipCode = num1[2:8]
                    # print("url1 != 0")
                elif get_webkey(url1) == 0:
                    if get_webkey(url2) != 0:
                        checkcode = num2
                        zipCode = num2[2:8]
                        # print("url2 != 0")
                    elif get_webkey(url2) == 0:
                        if get_webkey(url3) != 0:
                            checkcode = num3
                            zipCode = num3[2:8]
                        elif get_webkey(url3) == 0:
                            checkcode = 'NULL'
                            zipCode = 'NULL'
                        # print("url2 == 0")
            elif num1 == 'NULL':
                checkcode = 'NULL'
                zipCode = 'NULL'
                # print("url1 == NULL")

            newtable.append(checkcode)
            newtable.append(zipCode)
            newtable.append('0')
            # print(newtable)

            try:
                # 执行sql语句
                cur.execute(sql_insert%(newtable[1], newtable[2], newtable[3], newtable[0], newtable[7]))
                # 执行数据库操作每步都要数据库db.commit()以后才能操作
                # 提交到数据库执行
                conn.commit()
                print(i)
            except:
                # Rollback in case there is any error
                conn.rollback()
                print('Fail to insert row ', i)
        except:
            # print('Fail to reach row', i)
            cur.execute(sql_insert%(companyName, 'NULL', 'NULL', '-1', '1'))
            conn.commit()
            pass

if __name__ == '__main__':
    server = SSHTunnelForwarder(
        'xxx.xx.xxx.xx',
        ssh_username='xx',
        ssh_password='xx',
        remote_bind_address=('127.0.0.1', 3306)
    )
    server.start()
    conn = pymysql.connect(
        host='127.0.0.1',
        port=server.local_bind_port,
        user='xx',
        password='xx',
        db='xx',
        charset = 'utf8mb4'
    )
    cur = conn.cursor()

    # cur.execute("DROP TABLE IF EXISTS CheckedTaxationCode")
    # try:
    #     cur.execute(sql_create)
    # except:
    #     print('Fail to create table CheckedTaxationCode!')
    # # 需不需要提交到数据库执行？
    # # conn.commit()

    cur.execute(sql_get)
    data = cur.fetchall()
    # print(len(data))
    # for i in range(20):
    process_data_after_interruption(data)
    print("Finished first round!")


    # 循环检查CheckedTaxationCode里mark为1的，重新跑
    # read CheckedTaxationCode, find all mark == 1, re-run
    while True:
        cur.execute(sql_getMark)
        data = cur.fetchall()
        process_data(data)
        print("Finished a new round")
        if len(data) == 0:
            print("Finished second part")
            break

    cur.close()
    # 关闭数据库连接
    conn.close()
    # Make sure to call server.stop() when you want to disconnect
    server.stop() 
