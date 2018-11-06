import time

#一元马尔可夫。。。
passwords=[]  #存储带前缀和后缀的口令,前缀可以使的概率计算统一化，后缀用来确定生成的口令是否为一整条口令
dicts1={}     #存储一元语法及其出现的次数
dicts={}      #存储二元语法及其出现的次数
q={}          #字典，存储生成的字符串以及其对应的概率值

def readfiles(file_name):        #将口令读取到passwords中,file_name是一个字符串
    f=open(file_name,'r')
    lines=f.readlines();
    f.close()
    for p in lines:
        passwords.append(p[0:-1])    #这里取p[0:-1]是因为从文件中读取出的字符串结尾带有换行符'\n'

#对口令进行预处理，对passwords中的口令加上前缀(#)和后缀($)
def pre_passwords():
    for i in range(len(passwords)):
            passwords[i]="#"+passwords[i]+"$"

#存储训练集中二元语法出现的次数，写到字典dicts中
def eryuan_dict():
    for i in passwords:
        for j in range(len(i)-2):
            if dicts.has_key(i[j:j+2]):
                dicts[i[j:j+2]]+=1
            else:
                dicts[i[j:j+2]]=1
        if dicts.has_key(i[-2:]):
            dicts[i[-2:]]+=1
        else:
            dicts[i[-2:]]=1

#存储一元语法出现的次数,写到字典dicts1中
def yiyuan_dict():
    for i in passwords:
        for j in range(len(i)):
            if dicts1.has_key(i[j]):
                dicts1[i[j]]+=1
            else:
                dicts1[i[j]]=1

#计算一个字符串的概率，这之前进行了添加前缀后缀的操作，所以字符串s第一个字符一定是#
#这个函数其实后来没有用到，因为对于一个口令单独计算概率的复杂度太高，在后面的算法中直接记录每个字符串的出现的概率，然后当在字符串后面拼接字符的时候，
#可以直接利用记录的字符串的概率计算拼接后的字符串的概率，这样比较快。比如已知字符串w1 w2 w3的概率，要计算字符串w1 w2 w3 w4的概率就可以直接利用字符串
#w1 w2 w3的概率计算，即p(w1 w2 w3 w4)=p(w1 w2 w3)*p(w4|w3)。
def str_prob(s):
    total=1    
    if len(s)==1:
        total=1      
    else:
        for i in range(len(s)-1):
            str1=s[i]+s[i+1]
            if str1 in dicts.keys():
                total*=(float(dicts[str1]+1))/(float(dicts1[s[i]]+len(dicts)))
            else:
                total*=float(1)/float(dicts1[s[i]]+len(dicts))
    return total

#返回字典中最大的value所对应的key
def getMax(dic):
    aa=dic.items()
    bb=aa[0][1]
    cc=aa[0][0]
    for i in range(len(aa)):
        if aa[i][1]>bb:
            bb=aa[i][1]
            cc=aa[i][0]
    return cc

start=time.clock()
readfiles('yahoo-words.txt')     #yahoo-words.txt中存储了口令中的英文字符串，读出文件内容并将文件内容存储在passwords中
pre_passwords()                  #对passwords中的字符串加前后缀
yiyuan_dict()                    #填写字典dicts1，存储键值对（单个字符：出现的次数）
eryuan_dict()                    #填写字典dicts，存储键值对（passwords中英文字符串出现的两个字符的组合：出现的次数）

#zifu=['!', '$', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', 'B', 'G', 'L', 'M', 'N', 'S', 'T', 'V', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#zifu存储要拼接的所有字符
zifu=['$','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lenzufu存储列表zifu的长度
lenzufu=len(zifu)

q['#']=float(1)
result=[]      #记录所有输出的整个的字符串，在算法计算完毕后再写入到文件中去，比生成一个就往文件中写一个所用的时间短一点
while(len(result)<100000):
    if len(q)==0:
        break
    else:
        temp1=getMax(q)   #取字典中最大值所对应的字符串
        v=q.pop(temp1)    #把上一条取出的字符串从字典中删除
        temp_dict={}      #记录各个字符串和其出现的概率
        if temp1[-1]=='$':     #如果队列中取出的是整个字符，就把它输出到结果中去
            if len(temp1)>3:     #规定生成的字符串至少大于3（包括前后缀）
                result.append(temp1)
            else:
                pass
        else:
            for ii in zifu:
                pinjie=temp1+ii
                if pinjie=='#$':
                    pass
                else:
                    q[pinjie]=float(v)*(float(dicts[temp1[-1]+ii]+1)/float(dicts1[temp1[-1]]+lenzufu))   #其中的+1和+lenzifu是为了对概率进行平滑，防止口令概率为零的情况出现，从而导致过拟合
    end=time.clock()
    if int(end-start)>259200:        #设定终止时间为72小时后终止，开始时间为11月5日00:00
        break
end=time.clock()
print result

f2=open('resulea.txt','w+')         #最后将结果统一写入文件
for kkk in result:
    f2.write(kkk+'\n')
f2.close()

print 'time=',str(end-start)       #输出总的运行时间
