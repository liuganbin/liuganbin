# 导入所需包
import jieba
import jieba.analyse
import re


# Jaccard相似度
class JaccardSim(object):
    # 构造函数
    def __init__(self, a, b):
        self.c1 = a
        self.c2 = b

    # 提取关键词
    @staticmethod
    def getKeywords(content):
        # 过滤特殊字符
        filter = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
        content = filter.sub(' ', content)
        # 利用jieba分词切开句子，并提取关键词
        string = [i for i in jieba.cut(content, cut_all=True) if i != '']
        result = jieba.analyse.extract_tags("|".join(string), topK=200, withWeight=False)
        return result

    def main(self):
        # 提取关键词
        keyA = self.getKeywords(self.c1)
        keyB = self.getKeywords(self.c2)

        # 计算
        intersection = len(list(set(keyA).intersection(set(keyB))))
        union = len(list(set(keyA).union(set(keyB))))

        # 除零处理
        sim = float(intersection) / union if union != 0 else 0
        return sim


# 测试
if __name__ == '__main__':
    p1 = input("论文原文的文件的绝对路径：")
    p2 = input("抄袭版论文的文件的绝对路径：")
    if not jieba.os.path.exists(p1):
        print("论文原文的文件的绝对路径错误")
        exit()
    if not jieba.os.path.exists(p2):
        print("抄袭版论文的文件的绝对路径错误")
        exit()
    with open(p1, 'r', encoding='UTF-8') as x, \
            open(p2, 'r', encoding='UTF-8') as y:
        a = x.read()
        b = y.read()
        similarity = JaccardSim(a, b)
        similarity = similarity.main()
        print('重复率: %.2f%%' % (similarity * 100))
