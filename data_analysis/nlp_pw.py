import pandas as pd
import numpy as np
import nltk

# 用于对单个口令进行基于自然语言处理的攻击
# 使用方法：
# 1. 生成一个nlp_pw类的实例，eg：test = nlp_pw()
# 2. 如果是初次运行，先生成语料库，eg：test.build_corpora()
# 3. 读取语料库，eg：test.read_corpora()
# 4. 对口令进行分词，获取所有有可能的分词方式，eg：test.word_break("abc")，
#     并将所有可能的分词方式按数组形式返回，eg：[['a', 'b', 'c'], ['a', 'bc'], ['ab', 'c']]
# 5. 得到口令最有可能的分词方式，eg；test.word_slice(candidates)，
#     其中candidates为word_break的返回值，该方法以此调用了segment（）方法，best_n_tram_score（）方法，
#     来计算每种候选项的得分，返回得分最高者及其word_segment，即最终的分词方式(如“iloveyou”返回['I', 'love', 'you'])
#     和其word_segment(后面可能用来分析)，返回值形式： [best_candidate, best_candidate_word_segment]
# 6. 对得到的分词进行词性标注，eg：test.words_tag(best_candidate)，返回标注了的单词分词结果
#     返回值格式：[('I', ['PRP']), ('love', ['name', 'VBP']), ('you', ['PRP'])]

class nlp_pw:
    source_corpora = None
    reference_source = None
    names = None
    countrys = None
    months = None
    COCA_1_gram = None
    COCA_2_gram = None
    COCA_3_gram = None

    COCA_1_gram_sum = None
    COCA_2_gram_sum = None
    COCA_3_gram_sum = None
#  生成语料库
    def biuld_corpora(self):
        # 读取制备语料库的文件
        namespath = "./names.csv"
        countrypath = "./main_countrys.csv"

        namesinfo = pd.read_csv(namespath)  # 按照使用频率
        names = namesinfo.sort_values("counts", ascending=False)["name"].str.lower()

        months = pd.DataFrame(
            {"month": ("Jan", "January", "Feb", "February", "Mar", "March", "Apr", "April", "May", "May", "Jun", "June",
                       "Jul", "July", "Aug", "August", "Sept", "September", "Oct", "October", "Nov", "November", "Dec",
                       "December")})

        countrys = pd.read_csv(countrypath)

        months["month"] = months["month"].str.lower()
        countrys["country"] = countrys["country"].str.lower()

        COCA_1_grams = pd.read_table('words_frequency.txt', header=None,
                                     names=['Word', 'Tag', 'Frequency', 'Dispersion'], sep='\t', index_col=0)
        COCA_2_grams = pd.read_table('w2c.txt', header=None, names=['Frequency', 'Word1', 'Word2', 'Tag1', 'Tag2'],
                                     sep='\t', index_col=0)
        COCA_3_grams = pd.read_table('w3c.txt', header=None,
                                     names=['Frequency', 'Word1', 'Word2', 'Word3', 'Tag1', 'Tag2', 'Tag3'], sep='\t',
                                     index_col=0)

        COCA_2_grams_sorted = COCA_2_grams.sort_index(ascending=False)
        COCA_3_grams_sorted = COCA_3_grams.sort_index(ascending=False)

        # 制备 source_corpora
        source_corpora = pd.concat([months["month"], names])
        source_corpora = pd.concat([source_corpora, countrys["country"]])
        source_corpora = pd.concat([source_corpora, pd.Series(["I", "a"])])

        words_2 = list()  # 单词长度为2
        words_3 = list()  # 单词长度为3

        for word in COCA_1_grams["Word"]:
            if len(word) == 2:
                if len(words_2) < 37:
                    words_2.append(word)
            elif len(word) == 3:
                words_3.append(word)

        words = pd.Series(list(set(words_2).union(set(words_3))))
        source_corpora = pd.concat([source_corpora, words])

        # 生成 source_corpora文件
        source_corpora.to_csv("./source_corpora.csv", sep=",", index=0)

        # 生成 reference_corpora
        reference_source = [COCA_1_grams, COCA_2_grams_sorted, COCA_3_grams_sorted,
                            pd.DataFrame(list(names), columns=["names"]), months, countrys]
        i = 0
        for corpora in reference_source:
            corpora.to_csv("reference_source_" + str(i) + "_.csv", sep=",", index=True)
            i += 1

#   读取语料库
#   得到source_corpora, reference_corpora
#   其中source_corpora用来确定一个单词是常用词还是一个无用的间隙词（如IalovebChina中，a为间隙词）
#   reference_corpora用来确定单词词性，使用频率等特点进行进一步分析，[COCA的1-grams，2-grams，3-grams,name, month, country]
#   输入：空
#   输出：[source_corpora, reference_corpora]
    def read_corpora(self):
        source_corpora = pd.read_csv("./source_corpora.csv", header=None)

        reference_corpora = list()
        for i in np.arange(6):
            x = pd.read_csv("reference_source_" + str(i) + "_.csv", sep=",", index_col=0)
            reference_corpora.append(x)

        self.source_corpora = source_corpora
        self.reference_source = reference_corpora
        self.COCA_1_gram = reference_corpora[0]
        self.COCA_2_gram = reference_corpora[1]
        self.COCA_3_gram = reference_corpora[2]
        self.names = reference_corpora[3]
        self.months = reference_corpora[4]
        self.countrys = reference_corpora[5]
        self.score_init()
        return [source_corpora, reference_corpora]


#   分词
#   获得一个口令所有有可能的分词方式
    def word_break(self, words):
        word_slices = self.in_word_break(words)
        return self.unique(word_slices)

#   list无法做hash，转成tuple便于去重
    def unique(self, words):
        temp = map(self.list2tuple, words)
        temp_uni = list(set(temp))
        return list(map(self.tuple2list, temp_uni))

    def list2tuple(self, lists):
        return tuple(lists)

    def tuple2list(self, tuples):
        return list(tuples)


#   递归求解所有有可能的分词方式
    def in_word_break(self, words):
        if len(words) > 1:
            result = list()
            for i in np.arange(1, len(words)):
                item = [words[:i], words[i:len(words)]]
                result.append(item)

                pre_combs = self.in_word_break(words[:i])
                if pre_combs:
                    for pre_item in pre_combs:
                        pos_word_copy = words[i:len(words)]
                        pre_item.append(pos_word_copy)
                        result.append(pre_item)

                pos_combs = self.in_word_break(words[i:len(words)])
                if pos_combs:
                    for pos_item in pos_combs:
                        pre_word_copy = [words[:i]]
                        pre_word_copy.extend(pos_item)
                        result.append(pre_word_copy)
            return result

        return None

#   确定word_segment 和 gap_segment
#   在后面得分计算中，需要计算word_segment的得分和，所以要找到每个候选项中的word_segment
#   判断方法为，是否在source_corpora中
    def segment(self, candidate):
        word_segment = list()
        gap_segment = list()

        for i in np.arange(len(candidate)):
            if candidate[i].lower() in self.source_corpora[0].values:
                word_segment.append([candidate[i], i])
            else:
                gap_segment.append([candidate[i], i])

        return [word_segment, gap_segment]


# 0. 调用word_break得到了一个口令所有可能的断词方式，每种断词我们称作一个候选项
# 1. 确定每个候选项中哪些部分为words segment 哪些为gaps segment
# 2. [自己添加的]如果候选项中words segment为空，则将该候选项去掉，如果一个口令最终没有候选项，则该口令不适合nlp分析
# 3. 根据单词在语料库中出现的频率，计算候选项中words segment的得分，得分最高的分组为口令最终的断词结果
# 论文提到的算法2
    def score_init(self):
        self.COCA_1_gram_sum = np.sum(self.COCA_1_gram["Frequency"])
        self.COCA_2_gram_sum = np.sum(self.COCA_2_gram.index.to_series())
        self.COCA_3_gram_sum = np.sum(self.COCA_3_gram.index.to_series())

    def uni_gram_prob(self, candidates):
        score = 0
        preq = sum(self.COCA_1_gram[self.COCA_1_gram.Word == candidates[0].lower()]["Frequency"])
        if not preq == 0:
            score = (preq / self.COCA_1_gram_sum)
        return score

    def bi_gram_prob(self, candidates):
        score = 0
        preq = sum(self.COCA_2_gram[
                       (self.COCA_2_gram.Word1 == candidates[0]) &
                       (self.COCA_2_gram.Word2 == candidates[1])].index)
        if not preq == 0:
            score = (preq / self.COCA_2_gram_sum)
        return score

    def tri_gram_prob(self, candidates):
        score = 0
        preq = sum(self.COCA_3_gram[
                    (self.COCA_3_gram.Word1 == candidates[0]) &
                    (self.COCA_3_gram.Word2 == candidates[1]) &
                    (self.COCA_3_gram.Word3 == candidates[2])].index)
        if not preq == 0:
            score = (preq/self.COCA_3_gram_sum)
        return score

    def best_n_tram_score(self, candidate):
        score = 0
        length = len(candidate)

        if length == 1:
            score = self.uni_gram_prob(candidate)
        elif length == 2:
            score = self.bi_gram_prob(candidate)
        elif length == 3:
            score = self.tri_gram_prob(candidate)

        if (score == 0):
            for i in np.arange(1, (4 if length > 3 else length)):
                a = self.best_n_tram_score(candidate[:i])
                b = self.best_n_tram_score(candidate[i:])
                temp_score = a * b

                if temp_score > score:
                    score = temp_score
        return score

#   1. 调用segment将每一个候选项分为word_segment和gap_segment
#   2. 去掉那些word_segment为空的候选项
#   3. 计算所有候选项得分，得分最高的为该口令的分段方式(只考虑word_segment)
#   4. NOTE
    # 按照原算法计算，则存在['Ilo', 'v', 'e', 'you']中只计算you，
    # 而该候选项得分完全依赖于得分较高的you，对于['I', 'love', 'you']不公平
    # 所以修改得分为得分*（2**（-len(gap_segment）)
    # 除此之外，由于source_corpora并未完全在reference_corpora中，有些包含不常用人名的会被舍弃
    # 因此我们对于所有得分为零的候选项，在未得到最佳候选项之前按照在source_corpora中的数量进行排列
    # 取最大
#   输入：候选项集合
#   输出：最佳候选项或None，当返回None时表示该口令不适合nlp分析
    def word_slice(self, candidates):
        best_candidate = None
        best_candidate_word_segment = None
        best_score = 0
        t_word_segment = None
        t_gap_segment = None
        for candidate in candidates:
            [word_segment, gap_segment] = self.segment(candidate)
            if not len(word_segment) == 0:
                score = (self.best_n_tram_score(np.array(word_segment)[:, 0]))*(8**(-len(gap_segment)))
                if score > best_score:
                    best_candidate = candidate
                    best_candidate_word_segment = word_segment
                    best_score = score
                elif best_score == 0:
                    if (t_word_segment == None) or ((len(t_word_segment) < len(word_segment)) & (len(t_gap_segment) < len(gap_segment))):
                        t_word_segment = word_segment
                        t_gap_segment = gap_segment
                        best_candidate = candidate

        if best_score == 0:
            best_candidate_word_segment = t_word_segment

        return [best_candidate, best_candidate_word_segment]



#   判断单词的词性，包括是否为姓名，月份，城市等，输出标记后的单词序列，如果一个单词包括多个词性，则我们尽量多的标注
#   输入：单词数组，eg：["I", "love", "china"]
#   输出：标记后的单词词组，eg：[('I', ['PRP']), ('love', ['name', 'VBP']), ('china', ['name', 'country', 'NN'])]
    def words_tag(self, words):
        words_tagged = list()
        word_pre = None
        for word in words:
            word_tags = list()
            if (True in self.names['names'].isin([word]).values):
                word_tags.append('name')
            if (True in self.months['month'].isin([word]).values):
                word_tags.append('month')
            if (True in self.countrys['country'].isin([word]).values):
                word_tags.append('country')

            if (word_pre == None):
                tag = nltk.pos_tag([word])
                word_tags.append(tag[0][1])
            else:
                word_tags.append(nltk.pos_tag([word_pre, word])[1][1])

            word_pre = word
            words_tagged.append((word, word_tags))

        return words_tagged


# ## 使用举例
x = nlp_pw()
# x.biuld_corpora()
[a, b] = x.read_corpora()
# print(x.word_break("Ilovechina"))
# print(x.word_slice([['Ilo', 'v', 'e', 'you'], ['I', 'love', 'you'], ['I', 'lo', 've', 'you']]))
#
# print(x.best_n_tram_score(["the"]))
# print(x.best_n_tram_score(["of", "the"]))
# print(x.best_n_tram_score(["one", "of", "the"]))
# print(x.best_n_tram_score(["I", "love", "you"]))
# print(x.best_n_tram_score(["any", "one"]))
# print(x.best_n_tram_score(["anyone"]))
# print(x.best_n_tram_score(["I", "love", "you", "very", "much"]))
#
# print(x.word_slice([['Ilo', 'v', 'e', 'you'], ['I', 'love', 'you']]))
# print(x.words_tag(["I", "love", "you"]))
a = x.word_break("steveol")
print(a)
b = x.word_slice(a)
print(b)
