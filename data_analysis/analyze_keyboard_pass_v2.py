#analyze the keyboard password
#version 2
#1.current work:
#(1)define 6 more type of keyboard password strings, now there are 12 in total
#the result has no big change, in CSDN data result there are about 8000 more, in YAHOO data result about 1000 more, and the frequency of more than 20 has no change at all.
#(2)get rid of single letters or numbers
#(3)just pick reletively high-frequency passwords
#(4)generate the password list and show the frequency
from pandas import Series
import pandas as pd
import numpy as np
import operator
np.set_printoptions(suppress=True)#use suppress option to print float

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

#define all KeyboardPass String
keyboard_pass1 = '1234567890qwertyuiopasdfghjkl;zxcvbnm,./'#left to right, top to down(1)
keyboard_pass2 = '1234567890poiuytrewqasdfghjkl;/.,mnbvcxz'#left to right, top to down(2)

keyboard_pass3 = '1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,9ol.0p;/'#top to down, left to right(1)
keyboard_pass4 = '1qazxsw23edcvfr45tgbnhy67ujm,ki89ol./;p0'#top to down, left to right(2)

keyboard_pass5 = 'zaq1xsw2cde3vfr4bgt5nhy6mju7,ki8.lo9/;p0'#down to top, left to right(1)
keyboard_pass6 = 'zaq12wsxcde34rfvbgt56yhnmju78ik,.lo90p;/'#down to top, left to right(2)

keyboard_pass7 = '0987654321poiuytrewq;lkjhgfdsa/.,mnbvcxz'#right to left, top to down(1)
keyboard_pass8 = '0987654321qwertyuioplkjhgfdsazxcvbnm,./'#right to left, top to down(2)

#only letter
keyboard_pass9 = 'qazwsxedcrfvtgbyhnujmik,ol.p;/'#top to down, left to right(1)
keyboard_pass10 = 'qazxswedcvfrtgbnhyujm,kiol./;p'#top to down, left to right(2)

keyboard_pass11 = 'zaqxswcdevfrbgtnhymju,ki.lo/;p'#down to top, left to right(1)
keyboard_pass12 = 'zaqwsxcderfvbgtyhnmjuik,.lop;/'#down to top, left to right(2)

keyboard_pass_all = keyboard_pass1 + keyboard_pass2 + keyboard_pass3 + keyboard_pass4 + keyboard_pass5 + keyboard_pass6 + keyboard_pass7 + keyboard_pass8 + keyboard_pass9 + keyboard_pass10 + keyboard_pass11

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
	
	if single_data in keyboard_pass_all and len(single_data) > 1:
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
	
	if single_data in keyboard_pass_all and len(single_data) > 1:
		#this password is keyboard password
		#add counter
		csdn_count = csdn_count + 1
		
		if csdn_output.has_key(single_data):
			#this password has been in dic, just add the value
			csdn_output[single_data] = csdn_output[single_data] + 1
		else:
			#has not been in dic, add key-value
			csdn_output[single_data] = 1

###############################################################
#3.1 get rid of some low frequency passwords
#3.2 calculate the frequency
#3.2 generate the passwordlist
###############################################################

###########################yahoo data##########################
#get rid of low frequency passwords which occur less than 10
tmp_dict = dict()
for single_data in yahoo_output:
	if yahoo_output[single_data] >= 10:
		tmp_dict[single_data] = yahoo_output[single_data]
yahoo_output = tmp_dict

#turn output dict to Series
yahoo_output = pd.Series(yahoo_output)

#sort the series by descending
yahoo_output = yahoo_output.sort_values(ascending = False)

#turn Series to Dataframe
df_yahoo = pd.DataFrame({'password' : yahoo_output.index , 'numbers' : yahoo_output.values , 'probability' : None})

#calculate the probability
index_yahoo = df_yahoo.index
for index in index_yahoo:
	df_yahoo.loc[index , 'probability'] =  str(float(df_yahoo.loc[index , 'numbers']) / yahoo_count).format(':.8f')

#save into csv files
df_yahoo.to_csv('result_yahoo_v2.csv' , columns = ['password' , 'numbers' , 'probability'])


###########################csdn data#############
#get rid of low frequency passwords which occur less than 20
tmp_dict.clear()
for single_data in csdn_output:
	if csdn_output[single_data] >= 20:
		tmp_dict[single_data] = csdn_output[single_data]
csdn_output = tmp_dict

#turn output dict to Series
csdn_output = pd.Series(csdn_output)

#sort the series by descending
csdn_output = csdn_output.sort_values(ascending = False)

#turn Series to Dataframe
df_csdn = pd.DataFrame({'password' : csdn_output.index , 'numbers' : csdn_output.values , 'probability' : None})

#calculate the probability
index_csdn = df_csdn.index
for index in index_csdn:
	df_csdn.loc[index , 'probability'] =  str(float(df_csdn.loc[index , 'numbers']) / csdn_count).format(':.8f')

#save into csv files
df_csdn.to_csv('result_csdn_v2.csv' , columns = ['password' , 'numbers' , 'probability'])