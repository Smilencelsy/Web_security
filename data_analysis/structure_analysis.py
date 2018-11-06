import sys

import ConfigParser
import time
import re
import csv

import pandas as pd
from pandas import Series,DataFrame

class Analysis(object):
	def __init__(self,passwdList):
		self.passwdList = passwdList

	#统计纯数字和字母的口令数量
	def countDorL(self):
		#统计总条数
		dic = {'L4':{},'L7':{},'L6':{},'L8':{},'L5':{},'L10':{},'L9':{},'L3':{},'L11':{},
		'L12':{},'D14':{},'D8':{},'D6':{},'D5':{},'D7':{},'D9':{},'D4':{},'D12':{},'L13':{},
		'L15':{},'L19':{},'L14':{},'L16':{},'D10':{},'L17':{},'D3':{},'L18':{},'D1':{},'D20':{},
		'L20':{},'D11':{},'L1':{},'L2':{},'D18':{},'D15':{},'D13':{},'D16':{},'S5':{},'S6':{},
		'D2':{},'S7':{},'S4':{},'S20':{},'S1':{},'S10':{},'S9':{},'D21':{},'D19':{}}

		df = DataFrame(columns=('structure','nums','1','2','3','4','5','6','7','8','9','10'))
		patternLetter = re.compile(r'[A-Za-z]+$')
		patternDigit = re.compile(r'\d+$')
		patternSig = re.compile(r'\W+$')
		for line in self.passwdList:
			line = str(line)
			l = ''
			if patternLetter.match(line):
				l = 'L' + str(len(line))
			elif patternDigit.match(line):
				l = 'D' + str(len(line))
			elif patternSig.match(line):
				l = 'S' + str(len(line))
			if l:
				if line in dic[l]:
					dic[l][line] += 1
				else:
					dic[l][line] = 1
		
		for tp in dic:
			every_dic = dic[tp]
			sums = sum(every_dic.get(x) for x in every_dic)
			rows = [tp,sums]
			every_dic = sorted(every_dic.items(),key = lambda x:x[1],reverse = True)
			if len(every_dic) > 10:
				for r in range(10):
					rows.append(str(every_dic[r]))
			else:
				for r in range(len(every_dic)):
					rows.append(str(every_dic[r][0]) + ' : ' + str(every_dic[r][1]))
				for r in range(10 - len(every_dic)):
					rows.append(0)
			df.loc[tp] = rows
		df = df.sort_values(by = 'nums')
		return df


	#统计字符串出现频率
	def countStr(self):
		pattern_letter = re.compile(r'[a-z]+' , re.I)
		pattern_digit = re.compile(r'\d+')
		pattern_sig = re.compile(r'[^A-Za-z0-9]+')
		str_dic = {}
		str_file = open('csdn_strfile.csv','w')
		csv_write = csv.writer(str_file)  #由于dataframe只支持对齐的table 这里采用了csv库的方法写文件
		for line in self.passwdList:
			letter_list = re.findall(pattern_letter,str(line))
			digit_list = re.findall(pattern_digit,str(line))
			sig_list = re.findall(pattern_sig,str(line))
			for L_str in letter_list:
				tmp_key = 'L' + str(len(L_str))
				if tmp_key in str_dic:
					if str(L_str) in str_dic[tmp_key]:
						str_dic[tmp_key][str(L_str)] += 1
					else:
						str_dic[tmp_key][str(L_str)] = 1
				else:
					str_dic[tmp_key] = {str(L_str):1}
			for L_str in digit_list:
				tmp_key = 'D' + str(len(str(L_str)))
				if tmp_key in str_dic:
					if str(L_str) in str_dic[tmp_key]:
						str_dic[tmp_key][str(L_str)] += 1
					else:
						str_dic[tmp_key][str(L_str)] = 1
				else:
					str_dic[tmp_key] = {str(L_str):1}
			for L_str in sig_list:
				tmp_key = 'S' + str(len(str(L_str)))
				if tmp_key in str_dic:
					if str(L_str) in str_dic[tmp_key]:
						str_dic[tmp_key][str(L_str)] += 1
					else:
						str_dic[tmp_key][str(L_str)] = 1
				else:
					str_dic[tmp_key] = {L_str:1}
		for tmp_dic in str_dic.keys():
			tpList = sorted(str_dic[tmp_dic].items(),key=lambda item:item[1],reverse=True)
			write_res = [tmp_dic]
			for tu in tpList:
				l = str(tu[0]) + '-' + str(tu[1])
				write_res.append(l)
			csv_write.writerow(write_res)

	#统计口令结构
	def countStruc(self):
		strucList = []
		for passwd in self.passwdList:
			struc = ''
			passwd = str(passwd)
			for ch in passwd:
				if ch.isdigit():
					struc += 'D'
				elif ch.isalpha():
					struc += 'L'
				else:
					struc += 'S'
			strucList.append(struc)

		#统计每种结构的口令数量
		nums = {}
		for stru in strucList:
			if stru in nums.keys():
				nums[stru] += 1
			else:
				nums[stru] = 1

		#计算出现频率 存入dataframe
		df = DataFrame(columns = ('structure','nums','freq'))
		for x in nums.keys():
			char = x[0] 
			stru = x[1:]
			c = 1 
			res = ''
			for i in stru:
				if i == char:
					c += 1
				else:
					res += char
					res += str(c)
					char = i
					c = 1
			res += char
			res += str(c)
			ge = '{:.18f}'.format(int(nums[x]) * 1.0 / len(strucList))
			df.loc[x] = [x, nums[x] , ge] 
			
		#转换为LxDxSx的形式
		for stri in df['structure']:
			char = stri[0] 
			stru = stri[1:]
			c = 1 
			res = ''
			for i in stru:
				if i == char:
					c += 1
				else:
					res += char
					res += str(c)
					char = i
					c = 1
			res += char
			res += str(c)
			df.loc[stri]['structure'] = res

		df = df.sort_values(by = 'nums')
		return df



if __name__ == '__main__':

	time1 = time.clock()

	#--------------------读文件模块--------------------#
	#读取文件
	data = pd.read_csv('../source/csdnpw.csv')
	passwdList = pd.Series(data['passwd'].values)

	#记录读文件的时间
	time2 = time.clock()
	print 'read file time : ' , (time2 - time1)

	#--------------------分析模块--------------------#
	ana = Analysis(passwdList)

	#分析生成口令结构/对应数量/出现概率的字符串
	ana.countStruc().to_csv('str_analysis_csdn.csv',index = False)
	#分析生成仅由字母/数字组成的口令数量, 以及每种结构频率TOP10的口令
	ana.countDorL().to_csv('onlyLorD_analysis.csv' , index = False)
	#统计字符子串的出现频率 如L3中'lsy'的出现频率等
	ana.countStr()

	#记录分析生成的时间
	time3 = time.clock()
	print 'Analysis time : ' , (time3 - time2)


