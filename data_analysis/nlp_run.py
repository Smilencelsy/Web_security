import nlp_pw as nlp
import pandas as pd
import numpy as np
from nltk.corpus import wordnet
import threading

# 真正用来运行分析的代码，
# 调用nlp_pw类实现对单个单词的分析
# 该类本来想通过多线程运行，但是wordnet好像不支持多线程
# 直接调用pw_analysis方法即可。

class nlp_pw_analysis(threading.Thread):
    result = list()

    def __init__(self, begin, end):
        threading.Thread.__init__(self)
        self.begin = begin
        self.end = end

    def run(self):
        print ("开始线程：" , self.name , " | ", self.begin , " -> " , self.end)
        self.pw_analysis(self.begin, self.end)
        print(self.result)
        # if final_result == None:
            #final_result = self.result
        # else:
            # final_result + self.result
        print("退出线程：", self.name)


    # 多线程分析，截取不同断分别分析
    def pw_analysis(self, begin, end):
        attacker = nlp.nlp_pw()
        attacker.read_corpora();

        yahoo_pw = pd.read_csv("yahoopw.csv", encoding = 'GBK')
        if end == -1:
            passwds = yahoo_pw["passwd"]
        else:
            passwds = yahoo_pw["passwd"].loc[begin:end]

        for item in passwds.values:
            print(item)

            if not wordnet.synsets(item):
                temp = attacker.word_slice(attacker.word_break(item))
                if temp == None or temp[0] == None:
                    result = attacker.words_tag([item])
                    print(result)
                    self.result.append(result)
                else:
                    result = attacker.words_tag(temp[0])
                    print(result)
                    self.result.append(result)
            else:
                result = attacker.words_tag([item])
                print(result)
                self.result.append(result)

    def persistent_result(self):
        # n1 = np.array(final_result_1)
        # print(self.result)
        final_result = pd.DataFrame(self.result, columns=["pattern", "word", "number"])
        final_result.to_csv("word_nlp_analysis.csv", sep=",")
        print(final_result)


#   开始分析！！！
a = nlp_pw_analysis(0, -1)
# b = nlp_pw_analysis(6, 10)
# c = nlp_pw_analysis(11, 15)

a.start()
# b.start()
# c.start()
a.join()
# b.join()
# c.join()
a.persistent_result()

print("退出主线程。。。")