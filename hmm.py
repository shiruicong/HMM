import math
import numpy as np

global start_prob
global trans_prob
global emit_prob
global total_words_count

'''
    数据预处理
    参数：无
    返回:
        1. word_freq            词频字典，例如{'我':1553,'爱':898,'人民币':353}  代表在语料库中，'我'这个字出现1553次，其它的类比
        2. total_words_count    词典词汇总数，包含重复的词
        3. start_prob           代表某个语料库中出现某个词性标注的概率(经过ln函数处理)
        4. trans_prob           代表训练语料库中词性之间的连接概率(经过ln函数处理)，这里只考虑前一个词性连接后一个词性，例如  '我'/'r','爱'/'v' 这两个词，表示为trans_prob['r']['v']
        5. emit_prob            代表词性对应词汇的概率(经过ln函数处理)，例如 '我'/r，表示为emit_prob['r']['我']
    注：此处的word_freq在代码中并未使用到，后续改进可能使用到，所以在此处保留
'''
def preprocess():

    i = -1
    word_list = []
    word_freq = {}
    total_words_count = 0
    start_prob = {}
    trans_prob = {}
    emit_prob  = {}

    list_char = []
    list_en = []
    with open("./data/raw_data.txt", 'r', encoding='UTF-8') as fi:
        for line in fi.readlines():
            line = line.strip().split()
            try:
                for word in line:
                    if word == "//w":
                        char = "/"
                        en = "/w"
                    else:
                        char, en = word.split("/")
                        list_char.append(char)
                        list_en.append(en)
            except:None

    for word in list_char:
        total_words_count = total_words_count + 1
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] = word_freq[word] + 1
        for en, count in word_freq:
         start_prob[word] = math.log(count/total_words_count)
    # 词典大小
    size_vocal = len(word_freq)
    #word2ids
    word2id = {}
    id2word = {}
    i = 0
    for word in word_freq:
        word2id[word] = i
        id2word[i] = word
        i = i + 1

    # 词性标注:标签的种类，以及转为ID
    en_freq={}
    for en in list_en:
        if en not in en_freq:
            en_freq[en] = 1
        else:
            en_freq[en] = en_freq[en] + 1
    size_en = len(en_freq)
    en2id = {}
    i = 0
    for en in en_freq:
        en2id[en] = i
        i = i + 1
    a = np.zeros(shape=(size_vocal, size_vocal))
    b = np.zeros(shape=(size_vocal, size_en))

    for i in range(total_words_count-1):
        word1 = list_char[i]
        word2 = list_char[i+1]
        id1 = word2id[word1]
        id2 = word2id[word2]
        a[id1][id2] += 1

    for i in range(total_words_count - 1):
        word1 = list_char[i]
        en = list_en[i]
        id1 = word2id[word1]
        id2 = en2id[en]
        a[id1][id2] += 1





            # #start_prob 此处计算的start_prob不是最终的start_prob
    # for line in lines:
    #     if line=='\n':
    #         continue
    #     else:
    #         list = line.split('\t')
    #         if list[3]=='_':            #由于有些单词没有标注词性，所以跳过
    #             continue
    #         if list[3] not in start_prob:
    #             start_prob[list[3]] = 1
    #         else:
    #             start_prob[list[3]] += 1
    #
    # #trans_prob 此处计算的trans_prob不是最终的trans_prob
    # for line in lines:
    #     if line=='\n':
    #         word_list = []  #由于计算词性连接概率是以句子为单位的，例如 ['我','爱','你'] ['他','爱','她']  第1句 我->爱 ，词性是'r'->'v'，而第1句的结尾'你' 和 第2句的开头'他'，是不做计算的，所以每次碰到句子的结尾，就必须重置临时变量
    #         i = -1
    #         continue
    #     else:
    #         list = line.split('\t')
    #         if list[3]=='_':            #由于有些单词没有标注词性，所以跳过
    #             continue
    #         word_list.append(list[3])
    #         i += 1
    #         if len(word_list)!=1: #句子的第1个单词，没有前一个单词，所以要跳过，后续会做特殊处理
    #             if word_list[i-1] not in trans_prob:
    #                 trans_prob[word_list[i-1]] = {}
    #                 trans_prob[word_list[i-1]][word_list[i]] = 1
    #             else:
    #                 if word_list[i] not in trans_prob[word_list[i-1]]:
    #                     trans_prob[word_list[i-1]][word_list[i]] = 1
    #                 else:
    #                     trans_prob[word_list[i-1]][word_list[i]] += 1
    #
    # #emit_prob 此处计算的emit_prob不是最终的emit_prob
    # for line in lines:
    #     if line=='\n':
    #         continue
    #     else:
    #         list = line.split('\t')
    #         if list[3]=='_':            #由于有些单词没有标注词性，所以跳过
    #             continue
    #         if list[3] not in emit_prob:
    #             emit_prob[list[3]] = {}
    #             emit_prob[list[3]][list[1]] = 1
    #         else:
    #             if list[1] not in emit_prob[list[3]]:
    #                 emit_prob[list[3]][list[1]] = 1
    #             else:
    #                 emit_prob[list[3]][list[1]] += 1


    '''
    #上面的 word_freq，total_words_count，start_prob，trans_prob，emit_prob 共5个数据，可以整合成一块进行计算，上面分开计算是为了读者方便阅览代码，理清楚逻辑
    for line in lines:
        #print(line=='\n')
        if line=='\n':
            word_list = []
            i = -1
            continue
        else:
            list = line.split('\t')
            if list[3]=='_':
                continue
            else:
                #计算word_freq
                if list[1] not in word_freq:
                    word_freq[list[1]] = 1
                else:
                    word_freq[list[1]] = word_freq[list[1]] + 1


                #计算total_words_count
                total_words_count += 1


                #计算start_prob
                if list[3] not in start_prob:
                    start_prob[list[3]] = 1
                else:
                    start_prob[list[3]] += 1


                #计算trans_prob
                word_list.append(list[3])
                i += 1
                if len(word_list)!=1:
                    if word_list[i-1] not in trans_prob:
                        trans_prob[word_list[i-1]] = {}
                        trans_prob[word_list[i-1]][word_list[i]] = 1
                    else:
                        if word_list[i] not in trans_prob[word_list[i-1]]:
                            trans_prob[word_list[i-1]][word_list[i]] = 1
                        else:
                            trans_prob[word_list[i-1]][word_list[i]] += 1


                #计算emit_prob
                if list[3] not in emit_prob:
                    emit_prob[list[3]] = {}
                    emit_prob[list[3]][list[1]] = 1
                else:
                    if list[1] not in emit_prob[list[3]]:
                        emit_prob[list[3]][list[1]] = 1
                    else:
                        emit_prob[list[3]][list[1]] += 1

    '''

    #对start_prob进行ln处理，由于log函数的特性，log(a*b*c) = log(a) + log(b) + log(c)，后续要用这些概率进行乘法，容易造成数值下溢出，所以先进行ln函数处理
    for key in start_prob:
        start_prob[key] = math.log(start_prob[key]/total_words_count)

    #对trans_prob进行ln处理
    for key1 in trans_prob:
        for key2 in trans_prob[key1]:
            trans_prob[key1][key2] = math.log(trans_prob[key1][key2]/total_words_count)

    #对emit_prob进行ln处理
    for key1 in emit_prob:
        for key2 in emit_prob[key1]:
            emit_prob[key1][key2] = math.log(emit_prob[key1][key2]/total_words_count)

    return word_freq,total_words_count,start_prob,trans_prob,emit_prob

'''
    加载测试集：返回举例
    [
        [('坚决', 'a'), ('惩治', 'v'), ('贪污', 'v'), ('贿赂', 'n'), ('等', 'u'), ('经济', 'n'), ('犯罪', 'v')],
        [('反对', 'v'), ('腐败', 'a'), ('是', 'v'), ('贯彻', 'v'), ('执行', 'v'), ('党的基本路线', 'n'), ('的', 'u'), ('必然', 'b'), ('要求', 'n')]
    ]
    说明：外面这个list是所有句子的集合，里面每一个list代表一个句子，里面list的元素是一个元组，元组的第一个元素是词，第二个元素是词性标注
'''
def load_test_data(filename):
    sentences = [[]]
    index = 0
    with open(filename,'r',encoding='UTF-8') as f:
        for line in f.readlines():
            if line=='\n':
                index += 1
                sentences.append([])
            else:
                list = line.split('\t')
                if list[3]=='_':
                    continue
                else:
                    sentences[index].append((list[1],list[3]))
    return sentences

'''
    词性标注方法,
    参数：一个句子的 单词list，例如 ['我','爱','中华','人民','共和国']
    返回：该句子的词性标注list，例如 ['r','v','n','n','n']

    注：本方法除了使用 入参list和 返回tag_list之外，还有一下几个相关的变量:
        1. prev_tag 代表前一个单词的词性，由于句首，没有前一个单词，所以词性默认为'S'
        2. start_prob 代表某个单词在训练语料库中出现的概率：ln(频次/总词数)，总次数包含重复的单词
        3. trans_prob 代表训练语料库中词性之间的连接概率(经过ln函数处理)，这里只考虑前一个词性连接后一个词性，例如  '我'/'r','爱'/'v' 这两个词，表示为trans_prob['r']['v']
        4. emit_prob  代表词性对应词汇的概率(经过ln函数处理)，例如 '我'/r，表示为emit_prob['r']['我']
        5. total_words_count 总词数(包含重复的词)
        6. all_tags 训练语料库中所有出现的词性标注
'''
def tag(list):
    tag_list = []
    prev_tag = 'S'
    #计算all_tags
    all_tags = set(start_prob.keys())
    #由于句首没有前一个词，所以前一个词的词性定义为'S'，并且为其赋值为句首单词的词性出现概率 即trans_prob['S']['n'] = start_prob['n']
    trans_prob[prev_tag] = {}
    for tag in all_tags:
        trans_prob[prev_tag][tag] = start_prob[tag]

    for word in list:
        #如果出现训练预料库中未出现的词汇，则默认其为出现1次，例如出现 '阿尔卑斯山脉' 则 emit_prob[所有词性]['阿尔卑斯山脉'] = math.log(1/total_words_count)
        for tag in all_tags:
            if word not in emit_prob[tag]:
                emit_prob[tag][word] = math.log(1/total_words_count)
        #如果词性之间的连接不存在，则默认为1，例如 训练语料库中不存在 前一个词性为'n',后一个词性为'v'的情况，则trans_prob['n']['v'] = math.log(1/total_words_count)
        for tag in all_tags:
            if tag not in trans_prob[prev_tag]:
                trans_prob[prev_tag][tag] = math.log(1/total_words_count)
        #这里的概率计算公式为，以['我','爱','你']为例，假设当前word为'爱'，则计算出'爱'对应每一种标注的概率，然后取最大的，假设标注为'v'，前一个字'我'，计算出来的标注为'r',则'爱'标注为'v'的概率= 语料库中出现'v'的概率 * (前一个词为'r'，后一个词为'v'的概率) * 'v'对应'爱'的概率
        (prob,tag) = max([(start_prob[tag]+trans_prob[prev_tag][tag]+emit_prob[tag][word],tag) for tag in all_tags])
        prev_tag = tag
        tag_list.append(tag)
    return tag_list

'''
    计算测试集的标注正确率
    参数：测试集，该参数正式上面 load_test_data的返回，参照load_test_data方法
    返回：一个double类型的值，代表对该测试集进行标注的正确率
'''
def calc_percentage(test_data):
    #正确标注的数量
    right_tag_count = 0
    for sentence in test_data:
        list = [word for (word,tag) in sentence]
        right_tag_list = [tag for (word,tag) in sentence]
        tag_list = tag(list)
        for i in range(len(list)):
            if right_tag_list[i] == tag_list[i]:
                right_tag_count += 1
    return right_tag_count/total_words_count

if __name__ == '__main__':
    word_freq,total_words_count,start_prob,trans_prob,emit_prob = preprocess()
    test_data = load_test_data('train.conll')
    percentage = calc_percentage(test_data)
    print('正确率是%s' % percentage)
