# import re
#
# companyName = open('/Users/xuyujie/Desktop/companyName.txt', 'w')
# with open('/Users/xuyujie/Desktop/enterprise_list_distinct.txt') as f:
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

import jieba.analyse
import xlwt  # 写入Excel表的库

wbk = xlwt.Workbook(encoding='ascii')
sheet = wbk.add_sheet("wordCount")  # Excel单元格名字
word_lst = []
key_list = []

for line in open('/Users/xuyujie/Desktop/companyName.txt'):  # 是需要分词统计的文档

    item = line.strip('\n\r').split('\t')  # 制表格切分
    # print item
    tags = jieba.analyse.extract_tags(item[0]) # jieba分词
    for t in tags:
        word_lst.append(t)

word_dict = {}
with open("/Users/xuyujie/Desktop/wordCount.txt", 'w') as wf2:  # 打开文件

    for item in word_lst:
        if item not in word_dict:  # 统计数量
            word_dict[item] = 1
        else:
            word_dict[item] += 1

    orderList = list(word_dict.values())
    orderList.sort(reverse=True)
    # print orderList
    for i in range(len(orderList)):
        for key in word_dict:
            if word_dict[key] == orderList[i]:
                wf2.write(key + ' ' + str(word_dict[key]) + '\n')  # 写入txt文档
                key_list.append(key)
                word_dict[key] = 0
        print(i)

for i in range(len(key_list)):
    sheet.write(i, 1, label=orderList[i])
    sheet.write(i, 0, label=key_list[i])
    print(i)
wbk.save('/Users/xuyujie/Desktop/wordCount.xls')  # 保存为 wordCount.xls文件
