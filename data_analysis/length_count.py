import sys
import time
import pandas as pd
from pandas import Series,DataFrame


class Analysis(object):
	def __init__(self,passwdList):
		self.passwdList = passwdList

	#统计不同长度的密码
	def countLength(self):
		maxLength = 0
		ser2 = Series(0,range(0,40))
		for passwd in self.passwdList:
			ser2[len(str(passwd))-1] += 1
		return ser2

if __name__ == '__main__':

	time1 = time.clock()
	#--------------------读文件模块--------------------#
	#读取passwd
	data = pd.read_csv('../source/yahoopw.csv')
	passwdList = pd.Series(data['passwd'].values)

	#读口令结构文件
	time2 = time.clock()
	print 'read file time : ' , (time2 - time1)

	#--------------------分析模块--------------------#
	#输出为csv文件
	Analysis(passwdList).countLength().to_csv('passwd_length.csv')

	time3 = time.clock()
	print 'count length time : ' , (time3 - time2)


