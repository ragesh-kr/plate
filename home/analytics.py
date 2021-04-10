import pandas as pd
import numpy as np
from datetime import datetime as dt
from . import utilities as ut
from django.templatetags.static import static
from babel.numbers import format_currency

locale='en_IN'
currency = 'INR'

path_windows = "C:/Users/591705/django/plate-charts-NewUI/plate/static/data/"
path_mac="/Users/rags/Documents/ScopeAnalytica/plate-charts-NewUI/plate/static/data/"

'''
The below mentiond cleanData() function needs to be moved as a 
module to onboarding or data upload application.This is a temp function just to read.
While on boarding properties needs to be set, while uploading those props needs to be used and final sheet needs to 
be produced. Refer jupyter notebook "charts" 
'''
def readData():	
	df = pd.read_csv(path_windows+'input/data_f.csv' , parse_dates=["S2BillDate"])
	
	return df

def returnBasicDf(df):
	

	basic_df = df.groupby(['S2PName','S2PName-Category'], sort=False)['S2PGTotal'].agg([('totSale','sum'), ('count','size')]).reset_index()

	return basic_df
	
def filter_df_daterange(df,start_date,end_date):
	
	filter_by_date = df['S2BillDate'].between(start_date,end_date)
	df = df[filter_by_date]
	return df


def filter_df_franchise(df,franchise):
	filter_by_franchise = df['Franchise']==franchise
	df = df[filter_by_franchise]
	return df


'''function name says category trend, but it basically groups by category 
and date, hence can be reused for overall sales performance but grouping category needs to be dealth with,
or else can create problems'''
def categoryTrend(df,flag):
	
	df = df.groupby(['S2PName-Category','background_color','border_color',df['S2BillDate'].dt.to_period(flag)], sort=False)['S2PGTotal'].agg([('totSale','sum'),('count','size')]).reset_index()
	df = df.sort_values('S2BillDate').reset_index(drop=True)
	df['S2BillDate'] = df['S2BillDate'].astype('str')
	
	return df

def franchiseTrend(df,flag):
	df = df.groupby([df['S2BillDate'].dt.to_period(flag)], sort=False)['S2PGTotal'].agg([('totSale','sum')]).reset_index()
	df = df.sort_values('S2BillDate').reset_index(drop=True)
	df['S2BillDate'] = df['S2BillDate'].astype('str')
	
	return df


def categoryChart(date_range):

	df = categoryTrend(df,start_date,end_date,flag)


	return df

def itemPerf(df,category,count):
	df = df.groupby(['S2PName','S2PName-Category','background_color','border_color'], sort=False)['S2PGTotal'].agg([('totSale','sum'), ('count','size')]).reset_index()
	filter_category = df['S2PName-Category'] == category
	bstPerf_df = df[filter_category].sort_values('totSale',ascending=False)
	not_bstPerf_df = df[filter_category].sort_values('totSale')
	return bstPerf_df.head(count),not_bstPerf_df.head(count)

def getDataForItemsTrend(df,start_date,end_date,flag):
	

	
	df = df.groupby(['S2PName',df['S2BillDate'].dt.to_period(flag)], sort=False)['S2PGTotal'].agg([('totSale','sum'),('count','size'),('Avg','mean')]).reset_index()
	#print(df.head(20))
	#df.sort_values('S2BillDate',inplace=True) - commented
	df = df.sort_values("S2BillDate").reset_index(drop=True)
	
	df['S2BillDate'] = df['S2BillDate'].astype('str')
	if(flag=='w'):
		df["S2BillDate"] = df["S2BillDate"].str.split("/").str[1].astype("datetime64[ns]")
	
	#print(df.head())
	return df



def getRollingPercentage(df,cardStartDate,endDate):

	df_d = df.groupby([df['S2BillDate'].dt.to_period('d')], sort=False)['S2PGTotal'].agg([('totSale','sum')]).reset_index()
	df_d['DoD'] = (df_d['totSale'].pct_change()*100).round(1)
	df_m = df.groupby([df['S2BillDate'].dt.to_period('m')], sort=False)['S2PGTotal'].agg([('totSale','sum')]).reset_index()
	df_m['MoM'] = (df_m['totSale'].pct_change()*100).round(1)
	
	
	cardStartMonth = ut.subtractDays(endDate,31)
	#daySales_1 means it referes to startdate oda overall sales
	if df_d[df_d['S2BillDate']==cardStartDate.to_period('d')].empty:
		daySales_1 = 'nan'
	else:
		daySales_1 = format_currency(df_d[df_d['S2BillDate']==cardStartDate.to_period('d')]['totSale'].iloc[0].round(1),currency,locale=locale)
		
	

	if df_d[df_d['S2BillDate']==endDate.to_period('d')].empty:
		daySales_2 = 'nan'
	else:
		daySales_2 = format_currency(df_d[df_d['S2BillDate']==endDate.to_period('d')]['totSale'].iloc[0].round(1),currency,locale=locale)
		daySales_percentage = df_d[df_d['S2BillDate']==endDate.to_period('d')]['DoD'].iloc[0]

	
	#print(df_m)
	if df_m[df_m['S2BillDate']==cardStartMonth.to_period('m')].empty:
		monthSales_1 = 'nan'
	else:
		monthSales_1 = format_currency(df_m[df_m['S2BillDate']==cardStartMonth.to_period('m')]['totSale'].iloc[0].round(1),currency, locale=locale)

	if df_m[df_m['S2BillDate']==endDate.to_period('m')].empty:
		monthSales_2='nan'
	else:
		monthSales_2 = format_currency(df_m[df_m['S2BillDate']==endDate.to_period('m')]['totSale'].iloc[0].round(1),currency,locale=locale)
		monthSales_percentage = df_m[df_m['S2BillDate']==endDate.to_period('m')]['MoM'].iloc[0]

	cardsData = {'daySales_1':daySales_1,
				 'daySales_2' : daySales_2,
				 'daySales_percentage':daySales_percentage,
				 'monthSales_1':monthSales_1,
				 'monthSales_2':monthSales_2,
				 'monthSales_percentage':monthSales_percentage

	}

	return cardsData
	
	

