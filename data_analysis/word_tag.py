# 输入：分此后的口令集
# 输出：词性标注后的口令集
import pandas as pd
import nltk
passwd_breaked_path = "passwd_breaked.csv"

passwd = pd.read_csv(passwd_breaked_path)


def get_tag(tag_list):
    con = "-"
    pattern = None
    for c in tag_list:
        if pattern == None:
            pattern = c[1]
        else:
            pattern = con.join([pattern, c[1]])
    return pattern
tags = list()


con = "-"
for item in passwd.head().values:
    print(item[0])
    tagged = nltk.word_tokenize(item[0])
    result = get_tag(nltk.pos_tag(tagged))
    tags.append((con.join(tagged), result))

result = pd.DataFrame(tags, columns= ["pass wd", "tags"])

result.to_csv("pass_nlp_result.csv", sep=",")