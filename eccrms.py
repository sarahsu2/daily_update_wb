# =====0 path of documents=====
# path = '/Users/xuyujie/PycharmProjects/webParse/step7_NLP/EntityRec/'
# psg0 = path+'news_0.txt'
# psg4 = path+'news_4.txt'

# =====1 stanford parser=====
# 命令行用stanford parser
# java -Xmx5g -cp stanford-corenlp-3.8.0.jar:stanford-corenlp-models-3.7.0.jar:* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,mention,coref -coref.algorithm neural -file /Users/xuyujie/PycharmProjects/webParse/step7_NLP/EntityRec/news_0.txt

# =====2 jieba=====
# import jieba
# # 分词
# seg_list = jieba.cut(u"这是一段测试文本",cut_all = False)
# print("Full mode: \n"+ "\n".join(seg_list))  #默认精确模式
#
# # 词性标注
# import jieba.posseg as pseg
# words = pseg.cut("我爱北京天安门")
# for word,flag in words:
#     print('%s, %s' %(word,flag))
#
# #关键词提取
# import jieba.analyse
# content = u'会议邀请到美国密歇根大学(University of Michigan, Ann Arbor）环境健康科学系副教授奚传武博士作题为“Multibarrier approach for safe drinking waterin the US : Why it failed in Flint”的学术讲座，介绍美国密歇根Flint市饮用水污染事故的发生发展和处置等方面内容。讲座后各相关单位同志与奚传武教授就生活饮用水在线监测系统、美国水污染事件的处置方式、生活饮用水老旧管网改造、如何有效减少消毒副产物以及美国涉水产品和二次供水单位的监管模式等问题进行了探讨和交流。本次交流会是我市生活饮用水卫生管理工作洽商机制运行以来的又一次新尝试，也为我市卫生计生综合监督部门探索生活饮用水卫生安全管理模式及突发水污染事件的应对措施开拓了眼界和思路。'
# #基于TF-IDF
# keywords = jieba.analyse.extract_tags(content,topK = 5,withWeight = True,allowPOS = ('n','nr','ns'))
# for item in keywords:
#     print(item[0],item[1])
# #基于TextRank
# keywords = jieba.analyse.textrank(content,topK = 5,withWeight = True,allowPOS = ('n','nr','ns'))
# for item in keywords:
#     print(item[0],item[1])

# =====3 hanlp entity recognition=====
# # use HanLP get entity candidates
# from jpype import *
# startJVM(getDefaultJVMPath(), "-Djava.class.path=/Users/xuyujie/Downloads/hanlp-portable-1.5.3.jar:/Users/xuyujie/Downloads", "-Xms1g", "-Xmx1g") # 启动JVM，Linux需替换分号;为冒号:
# # startJVM(getDefaultJVMPath(), "-Djava.class.path=/Users/xuyujie/Downloads/hanlp-1.5.3-release/hanlp-1.5.3.jar:/Users/xuyujie/Downloads/hanlp-1.5.3-release", "-Xms1g", "-Xmx1g") # 启动JVM，Linux需替换分号;为冒号:
# HanLP = JClass('com.hankcs.hanlp.HanLP')

# # 中文分词
# java.lang.System.out.println(HanLP.segment("你好，欢迎使用HanLP汉语处理包！"))
# # 命名实体识别与词性标注
# NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
# print(NLPTokenizer.segment('中国科学院计算技术研究所的宗成庆教授正在教授自然语言处理课程'))
# # 关键词提取
# document = "水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
#            "根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
#            "有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
#            "严格地进行水资源论证和取水许可的批准。"
# print(HanLP.extractKeyword(document, 2))
# # 自动摘要
# print(HanLP.extractSummary(document, 3))
# # 依存句法分析
# print(HanLP.parseDependency("徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"))

# document0 = open(psg0).read()
# candidateEntity = []
# for i in range(30):
#     candidateEntity.append(HanLP.extractKeyword(document0, 30)[i])
# f1 = open('/Users/xuyujie/Desktop/webank/week 31/candidate_entity/output1.txt','w')
# for j in candidateEntity:
#     f1.write(j+'\n')
#
# shutdownJVM()

# =====4 mention coreference=====
# # clustering mention candidates
# 识别entity--提取entity（包括位置）
import re
input = open('/Users/xuyujie/Desktop/result.txt').read()
ce = input.split('}, {')
w, h = 3, len(ce)
detailMatrix = [[0 for x in range(w)] for y in range(h)]
count = []
posList = []
for i in range(len(ce)):
    detail = re.split('\': \'|\', \'|\': |, \'', ce[i])
    # print(len(detail))
    detailMatrix[i][0] = detail[1]
    detailMatrix[i][1] = int(detail[3])
    detailMatrix[i][2] = int(detail[5])
    posList.append(detail[7])
    count.append(input.count(detail[1]))

# 看论文－第一步怎么设置各个distance
w2, h2 = len(ce), len(ce)
distance1 = [[0 for x2 in range(w2)] for y2 in range(h2)]
distance2 = count
pos = [[0 for x3 in range(w2)] for y3 in range(h2)]

for i2 in range(len(ce)):
    for j in range(len(ce)):
        distance1[i2][j] = abs(detailMatrix[j][1] - detailMatrix[i2][1])

for i3 in range(len(ce)):
    for j2 in range(len(ce)):
        if posList[i3] == posList[j2]:
            pos[i3][j2] = 0
        else:
            pos[i3][j2] = 1

import numpy as np
mention1 = np.concatenate((distance1,pos))
mention2 = np.vstack((mention1,distance2))
# print(mention2)
mentions = mention2.transpose()
# print(mentions)

# 做聚类
# from sklearn.cluster import DBSCAN
# dbscan = DBSCAN(eps=0.5, metric='euclidean', min_samples=5)
# dbscan.fit(mentions)
# print(dbscan.labels_)

from sklearn import cluster
k_means = cluster.KMeans(n_clusters=200)
k_means.fit(mentions)
print(k_means.labels_)

# r = [178  53 143 113 113  25  25 146 108 165  10  10  10 170 170 170 122 198
#   58  58 154  94 193  24 188 188 124  81  67 119 159   2  98 173 173 173
#   43  43  43 128  73 111  31 153 106  16  16  16  46  74  32 102 172   9
#    9   9  35 100 100 196  66 135 197  22  22 129  38  93  61  84   5   5
#  136  39  44  44 130 183 115  14  14  96  47  28  28 118 118  50  50   6
#    6 120 101  21  65  99 174  33  82 145 145 132 132  11  11 181  95 199
#  179 142  69  30  30 171 109 182  62 155 131  63  63 156 156   0  71  51
#   70 139  37  37  86  86 194   7 191  57 112 141 141  23  23 148  41 169
#  163  76 157 127  13 104 180  52  52 149  40 137  72 147 103   3 158  90
#  189  49  49 126 126  68  68 176 176  26 117 121 187  45 160  88  88 177
#  164  17  17  83  83  42 167  75 110 152   8   8 133  92  54  19 144 144
#  125  59  48  48  85  85  85 161  77  77  77  77 190  12  12  12  91  91
#   91 123  36  36  36  87  87 162 107 166 166  18  18  18  18 138 138  89
#   80 184 184 184   1   1   1 186  78  78  78 140  64 192  29 151  15  15
#  105 168  34  97  56 195  20  79  60 150 150 150 150   4   4   4 185 185
#  114 114 175 175  55  55  55 134  27 116 116]
# s = r.split()
# s = ['79', '79', '27', '107', '107', '107', '107', '66', '106', '106', '9', '9', '9', '9', '9', '9', '9', '60', '60', '60', '60', '114', '80', '80', '17', '17', '17', '102', '78', '78', '32', '32', '120', '37', '37', '37', '37', '37', '37', '112', '2', '63', '95', '95', '22', '76', '76', '76', '71', '18', '58', '90', '41', '134', '134', '134', '92', '68', '68', '68', '8', '28', '28', '28', '28', '139', '36', '96', '62', '83', '15', '15', '38', '137', '42', '42', '132', '119', '119', '0', '0', '91', '47', '39', '39', '115', '115', '34', '34', '20', '20', '117', '10', '97', '87', '29', '29', '104', '13', '13', '13', '103', '103', '103', '103', '81', '81', '81', '45', '45', '45', '126', '126', '69', '69', '30', '30', '67', '125', '125', '125', '5', '5', '5', '84', '48', '54', '57', '57', '57', '16', '16', '16', '77', '77', '116', '73', '7', '7', '7', '7', '82', '82', '82', '52', '127', '127', '124', '26', '133', '49', '49', '49', '49', '64', '64', '11', '108', '108', '65', '65', '99', '99', '21', '21', '101', '101', '101', '72', '72', '72', '46', '122', '86', '86', '3', '3', '118', '118', '118', '50', '50', '50', '56', '56', '113', '31', '31', '74', '89', '130', '130', '121', '14', '75', '24', '24', '24', '131', '55', '98', '98', '1', '1', '1', '1', '85', '85', '85', '85', '44', '44', '44', '44', '100', '100', '100', '123', '70', '70', '70', '135', '135', '19', '88', '88', '88', '138', '138', '138', '138', '40', '40', '105', '109', '53', '53', '53', '53', '53', '53', '12', '12', '12', '12', '61', '61', '111', '111', '35', '4', '4', '128', '33', '33', '23', '94', '59', '59', '43', '93', '6', '6', '6', '6', '6', '6', '6', '110', '110', '110', '110', '51', '51', '51', '51', '51', '136', '129', '25', '25']
# for i in range(len(s)):
#     s[i] = int(s[i])
s = [79, 79, 27, 107, 107, 107, 107, 66, 106, 106, 9, 9, 9, 9, 9, 9, 9, 60, 60, 60, 60, 114, 80, 80, 17, 17, 17, 102, 78, 78, 32, 32, 120, 37, 37, 37, 37, 37, 37, 112, 2, 63, 95, 95, 22, 76, 76, 76, 71, 18, 58, 90, 41, 134, 134, 134, 92, 68, 68, 68, 8, 28, 28, 28, 28, 139, 36, 96, 62, 83, 15, 15, 38, 137, 42, 42, 132, 119, 119, 0, 0, 91, 47, 39, 39, 115, 115, 34, 34, 20, 20, 117, 10, 97, 87, 29, 29, 104, 13, 13, 13, 103, 103, 103, 103, 81, 81, 81, 45, 45, 45, 126, 126, 69, 69, 30, 30, 67, 125, 125, 125, 5, 5, 5, 84, 48, 54, 57, 57, 57, 16, 16, 16, 77, 77, 116, 73, 7, 7, 7, 7, 82, 82, 82, 52, 127, 127, 124, 26, 133, 49, 49, 49, 49, 64, 64, 11, 108, 108, 65, 65, 99, 99, 21, 21, 101, 101, 101, 72, 72, 72, 46, 122, 86, 86, 3, 3, 118, 118, 118, 50, 50, 50, 56, 56, 113, 31, 31, 74, 89, 130, 130, 121, 14, 75, 24, 24, 24, 131, 55, 98, 98, 1, 1, 1, 1, 85, 85, 85, 85, 44, 44, 44, 44, 100, 100, 100, 123, 70, 70, 70, 135, 135, 19, 88, 88, 88, 138, 138, 138, 138, 40, 40, 105, 109, 53, 53, 53, 53, 53, 53, 12, 12, 12, 12, 61, 61, 111, 111, 35, 4, 4, 128, 33, 33, 23, 94, 59, 59, 43, 93, 6, 6, 6, 6, 6, 6, 6, 110, 110, 110, 110, 51, 51, 51, 51, 51, 136, 129, 25, 25]
first_iter0 = np.vstack((mention2,s))
first_iter = first_iter0.transpose()

#按label打印cluster 肉眼看正确率
testlist = [[0 for x4 in range(200)] for y4 in range(10)]
for i4 in range(200):
    testlist[i4][i4] = s
    # input[1]
    # detailMatrix[i][0]

# cluster之间再匹配
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

def DAgger(first_iter, variable):
    mentionPairs = []
    for i4 in range(len(first_iter)):
        first_iter[i4] = 0

# 命名体标注
# for i in range(len(candidateEntity)):
#     candidateEntity[i] = 0

def LR(input_matrix, variable):
    input = input_matrix
    # calculate AUC and pick the best