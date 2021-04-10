import pandas as pd
from datetime import datetime as dt
from datetime import timedelta 

def determineFlag(start_date,end_date):
	val = pd.date_range(start_date, end_date, freq='d').nunique()

	if(val > 7 and val<40):
		flag = 'd'
	elif(val > 40 and val < 370):
	    flag = 'm'
	elif(val<=10):
	    flag ='d'
	else:
	    flag = 'y'

	return flag

def subtractDays(date_,no_of_days):
	return (date_ - timedelta(days=no_of_days))
