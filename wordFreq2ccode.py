import requests
import pymysql

def crwaler1(word):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    head = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword='
    middle1 = '&templateId=&page='
    end = '&pageSize=10'
    # 'http://www.creditchina.gov.cn/api/credit_info_search?keyword=%E5%BC%80%E5%8F%91&templateId=&page=1&pageSize=10'
    resultlist = []
    for i in range(102130):
        url = head + word + middle1 + repr(i) + end
        data = requests.get(url, headers=headers)
        try:
            data1 = data.json()
            data2 = data1.get('data', {})
            a = data2.get('results', {})
            if a == []:
                break
            else:
                for j in range(len(a)):
                    b = list(a[j].values())
                    # name = a[j].get('name', {})
                    # encry = a[j].get('encryStr', {})
                    # code = a[j].get('idCardOrOrgCode', {})
                    name = b[0]
                    code = b[1]
                    encry = b[8][:-2]
                    resultlist.append(name)
                    resultlist.append(code)
                    resultlist.append(encry)
                    # return resultlist
        except:
            pass
    return resultlist

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

sql_insert = """INSERT INTO CheckedTaxationCode(companyName, creditCode, encryStr, gotCompanyInfo, mark) VALUES ('%s', '%s', '%s', '%s', '%s')"""
sql_update = """UPDATE CheckedTaxationCode SET creditCode = %s , encryStr = %s, mark = %s WHERE companyName = %s"""
sql_check = """select * from CheckedTaxationCode where companyName = %s"""

if __name__ == '__main__':
    conn = pymysql.connect(user='root', password='**', db='**', charset='utf8mb4')  # , port=server.local_bind_port)
    cur = conn.cursor()

    with open("/path/wordFreq_20up.txt") as f:
        data = f.readlines()
        for i in range(len(data)):
            data1 = data[i].split()
            data2 = data1[0]
            # can be written as parallel program
            datalist = crwaler1(data2)
            for j in range(int(len(datalist)/3)):
                companyName = datalist[j*3]
                creditCode = datalist[j*3+1]
                encryStr = datalist[j*3+2]
                name_check = cur.execute(sql_check, companyName)
                if name_check != 0:
                    update_data = (creditCode, encryStr, '6', companyName)
                    update_db(conn, cur, sql_update, update_data)
                elif name_check == 0:
                    insert_data = (companyName, creditCode, encryStr, '-1', '6')
                    insert_db(conn, cur, sql_insert, insert_data)
                print(j)
            print(i)

    cur.close()
    conn.close()
