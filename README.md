# Web_security
The homework of Web Security


### 0x00 代码结构说明
---
- data_analysis 数据分析
- pwdList_generate 字典生成


### 0x01 总体思路说明
---
0. 预处理：将600w和40w的口令数据分别随机分成两份, 一份用来做测试集, 一份用来做训练集
1. 根据数据分析结果生成弱口令/常用口令字典, 用于筛选口令强度低的用户
2. 将比对过滤后的口令强度高的用户名取出生成新的文件
3. 对于剩下的用户名, 取出其用户名中的特征, 并据此生成n个密码测试(对于可检测度高的用户名 可额外猜测)
4. 最后统计猜测准确率 = 猜中的口令数量/整个词典大小


### 0x02 数据分析思路与结论
---
* 口令长度规律分析(/data_analysis/length_count.py)
  统计所有口令的长度, 找出占比最高的口令长度, 作为生成字典的主要长度
  结果如下:


* 口令结构分析
  口令可以由数字、字母、字符组成，分别由D(digit)、L(letter)、S(signel)代替
  在程序中遍历所有口令,识别其结构,以LxDxSx的格式存储(x为长度), 比如
  > woaini777  ->  L6D3

  ps: 使用了python自带的c.isdigit() isalpha() 判断字母和数字

(2) 数据文件：
	yahooStruc.csv  CSDNStruc.csv
	格式 口令结构串：出现频率

(3) 纯字母、纯数字的口令占比
	yahooOnlyLorD.csv
	CSDNOnlyLorD.csv


### 0x03 字典生成思路
---
* Markov


* PCFG


* NLP



