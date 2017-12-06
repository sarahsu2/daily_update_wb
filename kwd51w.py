# -*- coding: UTF-8 -*-
# # get 517257 company names
# from sshtunnel import SSHTunnelForwarder
# import pymysql
#
# server = SSHTunnelForwarder(
#     '143.89.126.78',
#     ssh_username='hzhangbc',
#     ssh_password='elearning',
#     remote_bind_address=('127.0.0.1', 3306)
# )
#
# server.start()
#
# conn = pymysql.connect(
#     host='127.0.0.1',
#     port=server.local_bind_port,
#     user='root',
#     password='2016leichen',
#     charset='utf8mb4',
#     db='EnterpriseInfo'
# )
#
# cur = conn.cursor()
# cur.execute("select companyName from TaxationCode")
# data = cur.fetchall()
# f = open('compName.txt', 'w')
# f.write(str(data))
# cur.close()
# conn.close()
# server.stop()

# preprocessing
# companyName = open('/Users/xuyujie/Desktop/compName.txt', 'r')
# df = companyName.readline()
# data = df.split("',), ('")
# ttt = open('sepa.txt', 'w')
# for i in data:
#     ttt.write(i)
#     ttt.write("\n")
# 手动去第一行和最后一行的括号

# import re
#
# companyName = open('/Users/xuyujie/Desktop/name.txt', 'w')
# with open('/Users/xuyujie/Desktop/sepa.txt') as f:
#     data = f.readlines()
#     for i in range(len(data)):
#         # get everything between ""
#         lists = re.findall(r'"(.*?)"', data[i])
#         # remove all non-chinese characters
#         name = re.findall(u'[\u4e00-\u9fff]+', lists[0])
#         namelist = ''.join(name)
#         companyName.write(namelist+ '\n')
#         print(i)
# companyName.close()

# word frequency counting
# import jieba.analyse
# import xlwt  # 写入Excel表的库
#
# wbk = xlwt.Workbook(encoding='ascii')
# word_lst = []
# key_list = []
#
# for line in open('/Users/xuyujie/Desktop/sepa.txt'):  # 是需要分词统计的文档
#
#     item = line.strip('\n\r').split('\t')  # 制表格切分
#     # print item
#     tags = jieba.analyse.extract_tags(item[0]) # jieba分词
#     for t in tags:
#         word_lst.append(t)
#
# word_dict = {}
# with open("/Users/xuyujie/Desktop/nameCount.txt", 'w') as wf2:  # 打开文件
#
#     for item in word_lst:
#         if item not in word_dict:  # 统计数量
#             word_dict[item] = 1
#         else:
#             word_dict[item] += 1
#
#     orderList = list(word_dict.values())
#     orderList.sort(reverse=True)
#     # print orderList
#     for i in range(len(orderList)):
#         for key in word_dict:
#             if word_dict[key] == orderList[i]:
#                 wf2.write(key + ' ' + str(word_dict[key]) + '\n')  # 写入txt文档
#                 key_list.append(key)
#                 word_dict[key] = 0
#         print(i)
