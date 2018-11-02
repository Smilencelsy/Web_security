# Web_security
The homework of Web Security


### 0x00 代码结构说明
---
代码匆忙整理了一下, 没有规范输入输出以及函数命名, 注释也写得不够详细, 请见谅!
- data_analysis 数据分析
	* length_count.py 输入yahoopw.csv/csdnpw.csv 输出passwd_length.csv
	* structure_analysis.py 输入yahoopw.csv/csdnpw.csv 输出structure_analysis.csv & onlyLorD_analysis.csv
	* date_analysis 输入yahoopw.csv/csdnpw.csv 输出onlydate_passwd.csv & enDate.csv
- pwdList_generate 字典生成


### 0x01 总体思路说明
---
0. 预处理：将600w和40w的口令数据分别随机分成两份, 一份用来做测试集, 一份用来做训练集
1. 根据数据分析结果生成弱口令/常用口令字典, 用于筛选口令强度低的用户
2. 将比对过滤后的口令强度高的用户名取出生成新的文件
3. 对于剩下的用户名, 取出其用户名中的特征, 并据此生成n个密码测试(对于可检测度高的用户名 可额外猜测)(*Yahoo和csdn需要分开生成)
4. 最后统计猜测准确率 = 猜中的口令数量/整个词典大小


### 0x02 数据分析思路与结论
---
* 口令长度规律分析(/data_analysis/length_count.py)    
  统计所有口令的长度, 找出占比最高的口令长度, 作为生成字典的主要长度    
  结果如下:   
  
  <img src="source/passwd_length.png" width = 90% height = 90% /> <br>

  ps: 口令的最大长度为40, print了一下长度为40的字符串, 无法正常显示, 应该是中文密码   
  pps: 顺便查了下有没有sql注入的密码, 只找到一个 '1=1' && 'yn'  嘻嘻   
  ppps: 图好像画错了, 两个都是8位最多, 我明天重画一个...   
  </br>
  
* 口令结构分析    
  口令可以由数字、字母、字符组成，分别由D(digit)、L(letter)、S(signel)表示   
  在程序中遍历所有口令,识别其结构,以LxDxSx的格式存储(x为长度), 比如
  > woaini777  ->  L6D3

  ps: 使用了python自带的c.isdigit() isalpha() 判断字母和数字    

  **输出文件1** : 口令结构与对应数量

  | structure | nums |
  | ------ | ------ |
  | L5D2 | 8704 |

  结论:    
  yahoo的口令文件中L6,L7,L8分别占据1、2、3名, 数量为42234,34285,30250, 这三者的占比达到了总数量453490条的23.5%   
  csdn的口令文件中D8,D9,L8分别占据1、2、3名, 数量为1381247,718225,312749, 这三者之和为2412221, 占总数量6428631的37.5%   
  由于csdn是国内的网站, Yahoo属于国际性的网站, 可以从结果中看出国内的网民更偏向于用数字作为密码, 而国外网民可能更偏向于用字母作为密码<sup>[1]</sup>
  </br>
  
  **输出文件2**: 纯数字/字母/字符口令数量以及使用频率top10    
  
  | structure | nums | 1 | 2 ...|   
  | ------ | ------ |------| ------ |   
  | L8 | 8704 | sksssss:100| xxxxxxxx:100|

  yahoo结果:   
  <img src="source/onlyLDS-yahoo.png" width = 90% height = 90% /> </br>
  
  csdn结果:   
  <img src="source/onlyDLS-csdn.png" width = 90% height = 90% /> </br>
  
  还有些奇怪的东西:
  <img src="source/onlyDLS.jpg" width = 90% height = 90% /> </br>
  
  @@@ 还没做的: 统计使用两种字母/数字/字符其中两种结合的, 三种结合的用户数量, 测评密码的安全度 / 判断小写大写字母的数量  
  </br>

* 日期格式口令分析   
  首先对纯数字组成的日期进行分析, 按照习惯, 有可能出现年份(yyyy), 年份-月份(yyyymm) , 年月日(yyyymmdd) 以及
  月日(mmdd)这四种主要形式   
  日期我们限定在正常日期(年份取近现代史1700-2100,月取01-12,日期取01-31)内, 然后对所有口令进行正则判断, 得到以下结果:

  - yahoo:   
  
    | yyyy |  yyyy-mm |  yyyy-mm-dd | mm-dd |   
    |------|------|------|------|   
    | 26995 | 829 | 285 | 21712 |
    
	所有数字长度大于4的口令数量为96742, 而含有(形似)日期数字的口令数量总共有49821条, 占51.5%, 占总口令数量的10.9%
	而对含英文日期的口令进行检测(如Jan\Feb……), 只占756条
	纯日期组成：1565

  - csdn:(国内网民更偏向于用数字作为密码)   
  
    | yyyy |  yyyy-mm |  yyyy-mm-dd | mm-dd |   
    |------|------|------|------|   
    | 1653148 | 669045 | 583023 | 1824891 |
    
	所有数字长度大于4的口令数量为5038597,含有(形似)日期数字的口令数量为4730107, 占93.9%, 占总口令数量的73.6%
	含英文组成的日期比yahoo还要少, 只有611条(可能因为国内网民不习惯用英文日期)
	纯日期组成：519827

   字典生成思路: 穷举某个时间段内的所有日期(不要穷举所有可能组合)

</br>
* 拼音格式口令分析

  两个思路：
  1. 生成一个含有拼音与频率对应的词典, 根据拼音的频率决定匹配方式   
  	 链接: https://blog.csdn.net/beibei8080/article/details/53508996
  2. 通过拼音流划分来提取字符串中的拼音    
  	 链接: https://wenku.baidu.com/view/448e5a21ec3a87c24128c42d.html

  我暂时写了个贪婪的匹配方法, 思路与2类似, 但由于还需要考虑和英文单词的交集, 所以暂时还不太准确

</br>
* 英文单词口令分析

</br>

### 0x03 字典生成思路
---
* Markov


* PCFG


* NLP

</br>
### 0x04 准确率评估
---
   初步评估方法: 成功次数/字典大小

</br>

### 0x05 参考文献
---
[1] Bornmann L, Leydesdorff L. Skewness of citation impact data and covariates of citation distributions: A large-scale empirical analysis based on Web of Science data[J]. Journal of Informetrics, 2016, 11(1):164-175.    
   这篇文章讲了数据分析的一些方法, 并且用PCFG生成了含有拼音的字典
[2] Ur B, Segreti S M, Bauer L, et al. Measuring real-world accuracies and biases in modeling password guessability[C]// Usenix Conference on Security Symposium. USENIX Association, 2015:463-481.
   这篇文章论述了密码安全强度的评价, 以及不同的字典生成方法的攻击成功率
[3] Melicher W, Ur B, Segreti S M, et al. Fast, Lean, and Accurate: Modeling Password Guessability Using Neural Networks[J]. Journal of Networks, 2013, 8(6).
   主要讲了如何用神经网络提升对密码安全评级的准确性(其中包含了对Markov等方法的评价,但可能没讲方法)
[4] Golla M, Dürmuth M. On the Accuracy of Password Strength Meters[C]//Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security. ACM, 2018: 1567-1582.
   该文章比对了各种密码强度评估准则, 并且衡量了这些准则的准确性
