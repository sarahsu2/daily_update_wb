import pymysql
import requests
import time
# from sshtunnel import SSHTunnelForwarder

def url1_maker(data, i):
    a = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword='
    name = data[i][0]
    # print("name ", name)
    b = '&templateId=&page=1&pageSize=10'
    url = a+name+b
    # print("ulr1_maker ", url)
    return url

def url2_maker(url1):
    # url1 = url1.encode('ascii', 'ignore')#.decode('ascii')
    # print("url2_maker_input ", url1)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    data = requests.get(url1, headers=headers)
    try:
        data1 = data.json()
        a = data1.get('data', {})
        b = a.get('results', {})
        if b != []:
            n = len(b)
            url_list = []
            for i in range(n):
                aa = 'http://www.creditchina.gov.cn/api/credit_info_detail?encryStr='
                bb = b[i].get('encryStr', {})
                bbb = bb[:-2] + '%3D%0A'
                url = aa + bbb
                url_list.append(url)
            return url_list
        else:
            return []
    except:
        return []

def credit_code_getter(url2):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    data = requests.get(url2, headers=headers)
    try:
        data1 = data.json()
        a = data1.get('result', {})
        # print("a ",a)
        result = []
        ccode = a.get('creditCode', {})
        result.append(ccode)
        entname = a.get('entName', {})
        result.append(entname)
        # print(url2, result)
        return result
    except:
        return ['','']

def update_db(conn, cur, sql, data):
    try:
        cur.execute(sql, data)
        conn.commit()
    except:
        conn.rollback()
    return 0

def insert_db(conn, cur, sql, data):
    try:
        cur.execute(sql%data)
        conn.commit()
    except:
        conn.rollback()
    return 0

sql_getName = """select * from CheckedTaxationCode where mark = 0 and creditCode = 'NULL'"""
sql_insert = """INSERT INTO CheckedTaxationCode(companyName, creditCode, zipCode, gotCompanyInfo, mark) VALUES ('%s', '%s', '%s', '%s', '%s')"""
sql_update = """UPDATE CheckedTaxationCode SET creditCode = %s , zipCode = %s, mark = %s WHERE companyName = %s"""
sql_check = """select * from CheckedTaxationCode where companyName = %s"""

if __name__ == '__main__':
    conn = pymysql.connect(user='root', password='***', db='EnterpriseInfo', charset='utf8mb4')#, port=server.local_bind_port)
    cur = conn.cursor()
    while True:
        cur.execute(sql_getName)
        data = cur.fetchall()

        if len(data) == 0:
            print("Name2cCode done!")
            break

        else:
            for i in range(len(data)):
                url1 = url1_maker(data, i)
                url2 = url2_maker(url1)
                if len(url2) > 0:
                    for j in range(len(url2)):
                        ccode_entname = credit_code_getter(url2[j])
                        # print("ccode_entname ",ccode_entname)
                        # if entname in table: sql_update, mark = 2
                        # if entname not in table: sql_insert, mark = 3
                        if ccode_entname[1] != {}:
                            name_check = cur.execute(sql_check, (ccode_entname[1]))
                            if name_check != 0:
                                update_data = ((ccode_entname[0]), (ccode_entname[0][2:8]), '2', (ccode_entname[1]))
                                update_db(conn, cur, sql_update, update_data)
                                # print("ccode_entname[0] ",ccode_entname[0])
                                # print('update' , ccode_entname[0],ccode_entname[0][2:8], i)
                                # print('UPDATE CheckedTaxationCode SET ' + 'creditCode =' + repr(ccode_entname[0]))
                            elif name_check == 0:
                                insert_data = ((ccode_entname[1]), (ccode_entname[0]), (ccode_entname[0][2:8]), '-1', '3')
                                insert_db(conn, cur, sql_insert, insert_data)
                                # print('insert', ccode_entname[0], ccode_entname[0][2:8], i)
                        else:
                            pass
                elif url2 == []:
                    pass

                print(i)

        # break

        time.sleep(120)

    cur.close()
    conn.close()
    # server.stop()
