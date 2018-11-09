import pandas as pd
import numpy as np
import nltk

passwd = pd.read_csv("passwd_nlp_result.csv",index_col=0)

最常用百大名词
noun = passwd[((passwd["tags"] == "NN") | (passwd["tags"] == "NNS"))]
noun_passwd = noun["pass wd"].value_counts()
noun_passwd = noun_passwd[:100].index.tolist()

最常用百大形容词
adj = passwd[(passwd["tags"] == "JJ")]
adj_passwd = adj["pass wd"].value_counts()
adj_passwd = adj_passwd[:100].index.tolist()

最常用百大动词
verbing = passwd[(passwd["tags"] == "VBP")]
verbing_passwd = verbing["pass wd"].value_counts()
verbing_passwd = verbing_passwd[:100].index.tolist()

dictionary = list()
cont = ""
for adjw in adj_passwd:
    for nounw in noun_passwd:
        dictionary.append(cont.join([adjw, nounw]))
for nounw in noun_passwd :
    for verb in verbing_passwd:
        dictionary.append(cont.join([nounw, verb]))
        
pw_Ser = pd.Series(dictionary)
pw_Ser.to_csv("nlp_dictionary.csv", sep=",", index=None)