# -*- coding: utf-8 -*-
from NearEntities.linked_list import LinkedList, LinkedListNode
from patternRecognition.utility import get_abs_path, load_list_from_file
from MMsegWithHMM.Merge import cut
from collections import defaultdict, Counter
import tensorflow as tf

class MyLinkedList(LinkedList):
    def __init__(self):
        super(MyLinkedList, self).__init__()
        self.entity_dict = dict()
        self.entity_list = list()

    @staticmethod
    def tuples2nodes(_seg_result):
        index = 0
        node_list = list()
        for seg_tuple in _seg_result:
            word_start = index
            word_end = index + len(seg_tuple[0])
            node = LinkedListNode(seg_tuple[0], word_start, word_end - 1)
            node_list.append(node)
            index = word_end
        return node_list

    def tuples2linkedlist(self, tuple_list):
        self.make_list(self.tuples2nodes(tuple_list))

    def combine_entity(self, _entity_list):
        for entity in _entity_list:
                self.combine_node_by_position(entity['start'], entity['end'] - 1)
        self.entity_list = _entity_list

    def mark_surrounding(self, window_size=5):
        for _entity in self.entity_list:
            entity_name = _entity['word']
            starting_node = self.node_ref[_entity['start']]
            for movement in ['prev', 'next']:
                current_node = getattr(starting_node, '%s_node' % movement)()
                _counter = 0
                while current_node:
                    current_node.add_label(entity_name)
                    _counter += 1
                    if _counter >= window_size:
                        break
                    current_node = getattr(current_node, '%s_node' % movement)()

    def get_marking_result(self):
        current_node = self.head
        marking_result = defaultdict(Counter)
        while current_node:
            if current_node.labels:
                marking_result[current_node.value] += current_node.labels
            current_node = current_node.next_node()
        out = open('/Users/xuyujie/Desktop/36kr_result.txt','a')
        for k, v in marking_result.items():
            out.write(k)
            out.write(str(v))
            out.write('\n')
            print(k, v)

        sorted_result = sorted(marking_result, key=lambda x: marking_result[x]['total'])
        # for item in sorted_result:
        #     print(item)


if __name__ == '__main__':
    # named_entity_list = load_list_from_file(get_abs_path('./entity_list.txt'))
    # for _input in test_text[:1]:
    #     get_named_entity_str(_input, ner_list)

    # read documents
    f = open('/Users/xuyujie/Desktop/sql_separated.txt')
    data = f.readlines()
    for i in range(58,len(data)):
        document = data[i]
        # document = "腾讯、阿里两家科技巨擎的产业大战，在电商、出行、餐饮、影视娱乐、云计算领域的碰撞都掀起风暴。当前，马云与马化腾的对决又聚焦到“新零售”。高鑫零售12月8日公告，阿里巴巴29亿元要约收购高鑫零售全部已发行股份。12月11日，永辉超市公告，腾讯将通过协议转让方式受让其5%股份，同时腾讯拟取得永辉超市控股公司永辉云创15%的股权。两大互联网巨头纷纷拿出真金白银在零售商超行业攻城略地，火药味十足，也让资本看清了下一个风口，以至于近日新零售概念股大涨。争战“新零售”被植入互联网基因后，中国零售行业正迎来变革。永辉云创成立于2015年6月，业务主要包括永辉会员店、“超级物种”以及永辉生活APP等。超级物种一直被外界视为与阿里旗下盒马鲜生对标的业态，此次交易也意味着腾讯将在新零售领域与阿里进行正面开战。两家中国科技公司正用实体商店重新定义购物，这种“新零售”的概念试图模糊掉实体店购物和线上购物界限的方式。比如，盒马鲜生通过各种技术和服务连接了线上、线下。消费者可以通过自助扫描收银机付款，也可以扫描货架上的商品，在收银处通过移动支付方式为“虚拟购物车”中的所有商品付款，无需把商品放入购物车，随后将由配送员送到家中。门店附近3公里范围内，30分钟送货上门。这一模式似乎是行得通的。2017年7月，盒马鲜生CEO侯毅在接受媒体采访时表示，盒马营业时间超过半年的门店已经基本实现盈利。华泰证券2016年12月的研报显示，盒马上海金桥店2016年全年营业额约2.5亿元，坪效(每坪面积可以产出的营业额)约5.6万元，远高于同业平均水平(1.5万元)。阿里在零售方面的布局可谓激进和大胆许多。2016年马云提出“新零售”概念后，今年下半年，盒马鲜生正式在全国各地大规模铺开。除了新零售品牌独立运营外，阿里系持续不断在资本市场大举收购零售类上市公司股权。据不完全统计，近4年来，阿里巴巴至少已经投入了750亿元人民币，用以对战略入股或收购传统零售商业公司。在A股市场，阿里已牵手苏宁云商、三江购物、新华都三家上市公司。此外还有银泰商业、联华超市以及高鑫零售。腾讯有流量竞争优势，依靠社交的连接把衣食住行等应用聚合成巨大的生态系统。但腾讯在零售市场主要合作伙伴是京东，尽管微信支付已几乎无处不在，但与线下商超之间缺少实质性关联。不过，腾讯显然也是线下百货争相合作的对象。腾讯与永辉超市互补永辉超市旗下“超级物种”与阿里巴巴旗下“盒马鲜生”有相似之处，均被视为“新零售”的创新业态。超级物种业务包括了未来超市和餐饮的概念，同时力推线上、线下融合，聚集了永辉超市孵化的8个项目。截至目前，“超级物种”有18家门店，分布在福州、厦门、深圳、北京。上海、成都和南京。据称，2018年超级物种门店数量将达到100家。对比盒马鲜生，超级物种具备生鲜供应链优势，永辉超市近年大力度投入供应链和线下门店。引入牛奶国际补充境外供应链、与贝恩联手收购全球最大的零售商服务企业达曼公司，投资更上游农业养殖公司“星源农牧”，永辉在供应链投入不断。末端门店也在持续扩张，截至2017年9月30日，永辉已开门店526家，不含超级物种9家、生活店102家。但是，超级物种线上能力较弱，作为一家O2O模式的零售品牌，超级物种与永辉超市伴生但缺失互联网资源。这一问题在2015年永辉引入京东之后也并未带来直观的改善。腾讯有望给“超级物种”插上互联网的翅膀，近两年来，腾讯在电商、零售领域亦是广泛布局，除了投资京东和美团点评，还包括移动电商平台拼多多、生鲜电商每日优鲜。零售也是腾讯不会放弃的阵地。腾讯CEO马化腾在2017年的公开信亦曾多次提到“智慧零售解决方案”。通过微信公众号、微信小程序等，腾讯为线下商家提供支付、营销、会员管理等解决方案。在巨大流量的吸引下，不少企业和商家通过微信上线。腾讯与永辉超市的合作可谓双赢，永辉能够通过腾讯补足支付短板，可借力微信的流量做营销；腾讯则可拓展线下支付场景，与支付宝抗衡，在线下消费行为大数据方面或有所作为。生鲜是电商增量市场11月的光棍节促销中，阿里巴巴和京东两家平台实现了440亿美元的商品交易总额，显示出了线上销售的庞大规模，数据显示，目前中国线上销售额已占到社会零售总额的约五分之一，但是中国电商也面临是否已经达到了顶点的疑问。中国线上零售在过去5年平均每年增长43%，但去年增速放缓至26%。引发了一场有关线上零售是否饱和的辩论。有分析师认为，线上销售额占社会零售总额比例正趋于稳定。拉动电商增长的消费电子产品等品类或许已无多少提升线上销售占比的空间，但是生鲜食品和快速消费品等其他品类的电商渗透率仍很低。据研究机构IDG预测，2017年的生鲜杂货销售额将达到1.3万亿美元，其中在线销售额只占2%到3%。总体上，电商占中国零售销售额的18%。但是如何打开生鲜市场？以往简单的B2C生鲜电商模式可以说已经被判定是失败的。今年6月，美国最大的电商平台亚马逊公司宣布以每股42美元的现金交易收购全美最大的天然和有机食品连锁零售商全食食品超市，交易价值为137亿美元。亚马逊收购全食超市旨在透过其遍布全美的线下门店，以及生鲜快消品上的优势，向线下寻找来客增量，从而弥补自身短板。阿里巴巴与永辉超市在线下布局的生鲜超市与亚马逊收购全食食品逻辑有一致性，但是阿里巴巴与腾讯对O2O似乎有更深刻的见解，超级物种或将成为腾讯新零售的首个试验田。"
        tf.reset_default_graph()
        try:
            result = cut(document, HMM=True, CRF=False, NER=True, pureResult=False)
            # print(result)
            entities = result['entities']
            seg_result = result['seg_result']
            linked_words = MyLinkedList()
            linked_words.tuples2linkedlist(seg_result)
            linked_words.print_node_ref(upper_bound=20)

            linked_words.combine_entity(entities)
            linked_words.print_node_ref(upper_bound=20)

            linked_words.mark_surrounding(window_size=10)
            linked_words.get_marking_result()
        except:
            pass
