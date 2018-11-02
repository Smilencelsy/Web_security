#analyze the keyboard password
#version 1 
#1.current work:
#define 6 type of keyboard password strings
#if password is one of the substrings of we define, we think it is keyboard password, and record it
#
#2.next stage:
#get rid fo some single or distinguished short substring, for example, single letter or number,
#give some more accurate definition of keyboard password, and modify the code
from pandas import Series
import pandas as pd
import operator

##############################################
#0.prepare data
##############################################
yahoopath = 'yahoopw.csv'
csdnpath = 'csdnpw.csv'
yahoo_pass_data = pd.read_csv(yahoopath)
csdn_pass_data = pd.read_csv(csdnpath)

#turn DataFrame to Series
yahoo_pass_data = yahoo_pass_data['passwd']
csdn_pass_data = csdn_pass_data['passwd']

#All KeyboardPass String
keyboard_pass1 = '1234567890qwertyuiopasdfghjkl;zxcvbnm,./'#left to right, top to down
keyboard_pass2 = '1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,9ol.0p;/'#top to down, left to right
keyboard_pass3 = '0987654321poiuytrewq;lkjhgfdsa/.,mnbvcxz'#right to left, top to down
keyboard_pass4 = 'zaq1xsw2cde3vfr4bgt5nhy6mju7,ki8.lo9/;p0'#down to top, left to right
#only letter
keyboard_pass5 = 'qazwsxedcrfvtgbyhnujmik,ol.p;/'#top to down, left to right
keyboard_pass6 = 'zaqxswcdevfrbgtnhymju,ki.lo/;p'#down to top, left to right
keyboard_pass_all = keyboard_pass1 + keyboard_pass2 + keyboard_pass3 + keyboard_pass4 + keyboard_pass5 + keyboard_pass6

#Counter of the keyboard password
yahoo_count = 0
csdn_count = 0

#save the keyboard password and it's number
yahoo_output = dict()
csdn_output = dict()

##############################################
#1.check every password in YAHOO password file
##############################################
for single_data in yahoo_pass_data.values:
	#turn some float and int to str
	single_data = str(single_data)
	
	if single_data in keyboard_pass_all:
		#this password is keyboard password
		#add counter
		yahoo_count = yahoo_count + 1
		
		if yahoo_output.has_key(single_data):
			#this password has been in dic, just add the value
			yahoo_output[single_data] = yahoo_output[single_data] + 1
		else:
			#has not been in dic, add key-value
			yahoo_output[single_data] = 1

##############################################
#2.check every password in CSDN password file
##############################################
for single_data in csdn_pass_data.values:
	#turn some float and int to str
	single_data = str(single_data)
	
	if single_data in keyboard_pass_all:
		#this password is keyboard password
		#add counter
		csdn_count = csdn_count + 1
		
		if csdn_output.has_key(single_data):
			#this password has been in dic, just add the value
			csdn_output[single_data] = csdn_output[single_data] + 1
		else:
			#has not been in dic, add key-value
			csdn_output[single_data] = 1

##############################################
#3.1 manage YAHOO data
##############################################
#turn output dict to Series
yahoo_output = pd.Series(yahoo_output)

#save statistics into dict
yahoo_output['all password'] = len(yahoo_pass_data)
yahoo_output['keyboard password'] = yahoo_count

#sort the series by descending
yahoo_output = yahoo_output.sort_values(ascending = False)

#print to console
#print(yahoo_output)

#print to file
yahoo_output.to_csv('result_yahoo.csv')

##############################################
#3.2 manage CSDN data
##############################################
#turn output dict to Series
csdn_output = pd.Series(csdn_output)

#save statistics into dict
csdn_output['all password'] = len(csdn_pass_data)
csdn_output['keyboard password'] = csdn_count

#sort the series by descending
csdn_output = csdn_output.sort_values(ascending = False)

#print to console
#print(csdn_output)

#print to file
csdn_output.to_csv('result_csdn.csv')
