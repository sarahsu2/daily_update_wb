
os.chdir(os.path.abspath('/Users/xuyujie/Desktop'))
import urllib
from bs4 import BeautifulSoup # parse web
from lxml import etree
import pandas as pd
import pymysql

conn = pymysql.connect()
cur = conn.cursor()
data = cur

# url：只需替换keyword（1 如果为Null则跳过 2 如果第一个成功则跳过第二个）
def get_url(self, inputNum):
    url_pre = 'http://www.creditchina.gov.cn/search_all#keyword='
    url_pro = '&searchtype=0&templateId=&creditType=&areas=&objectType=2&page=1'
    url = url_pre+inputNum+url_pro
    return url

# 如果提取到网页上特定字段："没查到您要的信息" 则为不成功
def get_webkey(self, url):
    # url = 'http://www.creditchina.gov.cn/search_all#keyword=912104020811011528&searchtype=0&templateId=&creditType=&areas=&objectType=2&page=1'
    req = urllib.request.Request(url)
    # print(req)
    data = urllib.request.urlopen(req)
    # print(data)
    bs = data.read().decode('utf-8')
    soup = BeautifulSoup(bs, 'lxml')
    # check = soup.find_all("div", {"class": "no-result hidden"})
    check = soup.find_all("ul", {"class": "credit-info-results public-results-left item-template"})
    print("check = ", check)
    if check == []:
        code = url[49:67]
        return code
    if check != []:
        return 0

if __name__ == '__main__':
    # 如果第一个成功则跳过第二个，直接返回第一个；如果第一个不成功则换第二个keyword，第二个成功则返回第二个；如果第二个也不成功则返回Null
    # 保存统一社会信用编码&公司名称&地区编码（第3-8位）
    df = pd.read_csv("result3.csv", header=None)
    for i in range(len(df)):
        num1 = df.loc[i][2]
        num2 = df.loc[i][3]
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
