import sys

import ConfigParser
import time
import re

import pandas as pd
from pandas import Series,DataFrame

#统计可能含日期的口令(连续数字位数大于等于4的)
def countProbPasswd(passwdList):
	df = []
	for i in range(len(passwdList)):
		passwd = str(passwdList[i])
		struc = ""
		for ch in passwd:
			if ch.isdigit():
				struc += 'D'
			elif ch.isalpha():
				struc += 'L'
			else:
				struc += 'S'

		char = struc[0]
		c = 1
		stri = struc[1:]
		res = ''
		for j in stri:
			if j == char:
				c += 1
			else:
				res += char
				res += str(c)
				char = j
				c = 1
		res += char
		res += str(c)

		#r'D[4-9]|D\d{2}'
		if re.search(r'D[4-9]|D\d{2}', res):
			df.append(passwd)

	return df

#统计含数字日期的口令
def analysisDate(data):
	datePasswd = []
	c1,c2,c3,c4 = 0,0,0,0
	for i in data:
		#yyyy 1700-2200
		if re.search(r'1[7-9]\d{2}|2[0-1]\d{2}',i):
			c1 += 1
		#yyyy-mm
		if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])',i):
			c2 += 1
		#yyyy-mm-dd
		if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			c3 += 1
		#mm-dd
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			c4 += 1
	print 'yyyy:' , str(c1), ',yyyy-mm:' , str(c2), ',yyyy-mm-dd:' ,str(c3) ,',mm-dd' ,str(c4)
	print 'all-length: ' , str(len(data))

#含英文日期的口令
def analysisEnDate(data):
	dic = ['Jan','January','Feb','February','Mar','March','Apr','April',
			'May','Jun','June','Jul','July','Aug','August','Sep','September',
			'Oct','October','Nov','November','Dec','December']
	lis = []
	for line in data:
		for i in dic:
			if i in str(line):
				lis.append(str(line))

	pd.Series(lis).to_csv('enDate.csv')

#只含日期密码的口令
def analysisDateOnly(data):
	lis = []
	for line in data:
		if re.match(r'\d+$',line):
			if re.match(r'1[7-9]\d{2}|2[0-1]\d{2}$',line):
				lis.append(line)
			elif re.match(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])$',line):
				lis.append(line)
			elif re.match(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$',line):
				lis.append(line)
			elif re.match(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$',line):
				lis.append(line)
	pd.Series(lis).to_csv('onlydate_passwd.csv')


if __name__ == '__main__':

	time1 = time.clock()
	#--------------------读文件模块--------------------#
	#读取passwd
	data = pd.read_csv('../source/yahoopw.csv')
	passwdList = pd.Series(data['passwd'].values)
	#读口令结构文件
	time2 = time.clock()
	print 'read file time : ' , (time2 - time1)

	#--------------------统计模块--------------------#
	lis = countProbPasswd(passwdList)
	analysisDate(lis)
	analysisEnDate(lis)
	analysisDateOnly(lis)
	time3 = time.clock()
	print 'analysis time : ' , (time3 - time2)
