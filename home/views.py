from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import analytics as ana
from datetime import datetime as dt
from datetime import timedelta 
from . import utilities as ut
from . import analytics as at
import math,random
import ast
import pandas as pd
import numpy as np
from babel.numbers import format_currency
from django.contrib.auth.decorators import login_required

locale='en_IN'
currency = 'INR'


# Create your views here.
@login_required
def home(request):

	return render(request,'home/home1.html')

@login_required
def itemsAjax(request):

	if request.is_ajax():
		
		itemsList = request.POST.get('items')
		
		#itemsList = ast.literal_eval(itemsList)
		#itemsList = [n.strip() for n in itemsList]
		itemsList=itemsList.split(',')

		daterange = request.POST.get('daterange').split('-')
		
		#franchise = request.POST.get('franchise')
		startDate = dt.strptime(daterange[0].strip(),'%m/%d/%Y')
		endDate = dt.strptime(daterange[1].strip(),'%m/%d/%Y')
		df = at.readData()
		flag = ut.determineFlag(startDate,endDate)
		df = at.filter_df_daterange(df,startDate,endDate)
		itemTrend_df = at.getDataForItemsTrend(df,startDate,endDate,flag)
		
		
		
		itemTrend_plt = [{'type':'scatter',
							'x' : itemTrend_df[itemTrend_df['S2PName']==item]['S2BillDate'].tolist(),
							'y' : itemTrend_df[itemTrend_df['S2PName']==item]['totSale'].tolist(),
							#'text' : itemTrend_df[itemTrend_df['S2PName']==item]['Hover'],
							'mode' : 'markers+lines',
							'name' : item,
							'hovertemplate': '<b>Date</b>: %{x}' +
                        '<br><b>Tot Sales</b>: %{y}<br>',
		}for item in itemsList]

		return JsonResponse({'itemTrend_plt':itemTrend_plt})

	else:
		return HttpResponse(' Not authorised!')


@login_required
def test(request):
	if request.is_ajax():
		
		category = request.POST.get('category')
		daterange = request.POST.get('daterange').split('-')
		#franchise = request.POST.get('franchise')
		count = int(request.POST.get('count'))
		


		startDate = dt.strptime(daterange[0].strip(),'%m/%d/%Y')
		endDate = dt.strptime(daterange[1].strip(),'%m/%d/%Y')
		df = at.readData()
		
		df = at.filter_df_daterange(df,startDate,endDate)


		bstPerfDf,not_bstPerfDf = at.itemPerf(df,category,count)
		data_bstPerf_plt = [{'type':'bar',
					'x':bstPerfDf['S2PName'].unique().tolist(),
					'y':bstPerfDf['totSale'].tolist(),
					'marker':{'color':'rgba(75, 192, 192, 0.5)',
								'line':{
								'color':'rgba(75, 192, 192, 1)',
								'width': 2
								}
							}
					}]

		data_not_bstPerf_plt = [{'type':'bar',
					'x':not_bstPerfDf['S2PName'].unique().tolist(),
					'y':not_bstPerfDf['totSale'].tolist(),
					'marker':{'color':'rgba(255, 80, 80, 0.5)',
								'line':{
								'color':'rgba(255, 80, 80, 1)',
								'width': 2
								}
							}
					}]

		
		return JsonResponse({'data_bstPerf_plt':data_bstPerf_plt,'data_not_bstPerf_plt':data_not_bstPerf_plt})
	else:
		return HttpResponse('None of ur business !!!!!!')
	


@login_required
def dashboard(request):
	df_raw= at.readData()
	#franchiseList = np.sort(df_raw_['Franchise'].unique()).tolist()
	#franchise = franchiseList[1]
	#df_raw = at.filter_df_franchise(df_raw_,franchise)
	count = 5
	minDate = df_raw['S2BillDate'].min()
	maxDate = df_raw['S2BillDate'].max()
	
	#print(minDate)
	#print(maxDate)
	if request.method == 'POST':
		daterange = request.POST['daterange'].split('-')
		#franchise = request.POST['franchise']
		#df_raw = at.filter_df_franchise(df_raw_,franchise)
		startDate = dt.strptime(daterange[0].strip(),'%m/%d/%Y')
		endDate = dt.strptime(daterange[1].strip(),'%m/%d/%Y')
		cardStartDate = ut.subtractDays(endDate,1)
		cardStartDate = pd.Timestamp(cardStartDate.year,cardStartDate.month,cardStartDate.day)
		cardEndDate = pd.Timestamp(endDate.year,endDate.month,endDate.day)
		# minDate = df_raw['S2BillDate'].min()
		# maxDate = df_raw['S2BillDate'].max()
			


	else:		
		startDate = ut.subtractDays(maxDate,14)
		cardStartDate = ut.subtractDays(maxDate,1)
		endDate = maxDate
		cardEndDate = endDate
		

	flag = ut.determineFlag(startDate,endDate)
	df = at.filter_df_daterange(df_raw,startDate,endDate)
	df['S2BillTime'] = pd.to_datetime(df["S2BillTime"])
	df.index = df['S2BillTime']

	df_breakfast = df.between_time('05:00', '11:30')
	df_lunch = df.between_time('11:30', '06:30')
	df_dinner = df.between_time('06:30', '10:30')
	breakfastSales = format_currency(df_breakfast['S2Rate'].sum(),currency,locale=locale)
	lunchSales = format_currency(df_lunch['S2Rate'].sum(),currency,locale=locale)
	dinnerSales = format_currency(df_dinner['S2Rate'].sum(),currency,locale=locale)

	df_breakfast_grp = df_breakfast.groupby(['S2PName'], sort=True)['S2PGTotal'].agg([('totSale','sum')]).reset_index()
	df_breakfast_grp = df_breakfast_grp.sort_values('totSale', ascending=False).head(10)

	breakfastTopBar = [{'type':'bar',
					'x':df_breakfast_grp['S2PName'].unique().tolist(),
					'y':df_breakfast_grp['totSale'].tolist(),
					'marker':{'color':'rgba(75, 192, 192, 0.5)',
								'line':{
								'color':'rgba(75, 192, 192, 1)',
								'width': 2
								}
							}
					}]


	#Pie chart for Breakfast,Lunch Dinner
	pieData = [{'type' : 'pie',
				 'values' : [df_breakfast['S2Rate'].sum(),df_lunch['S2Rate'].sum(),df_dinner['S2Rate'].sum()],
				 'labels' : ['Breakfast','Lunch','Dinner'],
				 'textinfo' : 'label+percent',
				 'insidetextorientation' : 'radial',
				 'hole' : .3
		}]
	

	#print(df.head())
	#df = at.filter_df_franchise(df_raw,franchise)
	movingPercentage = at.getRollingPercentage(df_raw,cardStartDate,cardEndDate)
	
	df_franchisePerf = at.franchiseTrend(df_raw,ut.determineFlag(minDate,maxDate))
	
	df_categoryTrend = at.categoryTrend(df,flag)
	
	xaxis_categoryTrend = df_categoryTrend['S2BillDate'].unique().tolist()
	category_list = df_categoryTrend['S2PName-Category'].unique().tolist()
	
	#Below line ss for plotly graph
	data_plt = [{'type' : 'scatter' , 
					'x' : df_categoryTrend[df_categoryTrend['S2PName-Category']==cat]['S2BillDate'].tolist(),
					'y' : df_categoryTrend[df_categoryTrend['S2PName-Category']==cat]['totSale'].tolist(),
					'mode' : 'markers+lines',
					'name' : cat,
					'line' : {'color': df_categoryTrend[df_categoryTrend['S2PName-Category']==cat]['border_color'].tolist()[0]}
				} for cat in category_list]

	overall_franchise_Sales =[{'type':'scatter',
								'x' : df_franchisePerf['S2BillDate'].tolist(),
								'y' : df_franchisePerf['totSale'].tolist(),
								'mode' : 'markers+lines',
								

	}]

	
	
	bstPerfDf, not_bstPerfDf = at.itemPerf(df,'Food',count)
	#Best performance Bar graph in chart js
	#xaxis_bstPerfBar = bstPerfDf['S2PName'].unique().tolist()
	#dataset_bstPerf = [{'data':bstPerfDf['totSale'].tolist(),'borderWidth':2,'borderColor':bstPerfDf[bstPerfDf['S2PName-Category']=='Food']['border_color'].tolist()[0],'backgroundColor':bstPerfDf[bstPerfDf['S2PName-Category']=='Food']['background_color'].tolist()[0]}]

	data_bstPerf_plt = [{'type':'bar',
					'x':bstPerfDf['S2PName'].unique().tolist(),
					'y':bstPerfDf['totSale'].tolist(),
					'marker':{'color':'rgba(75, 192, 192, 0.5)',
								'line':{
								'color':'rgba(75, 192, 192, 1)',
								'width': 2
								}
							}
					}]
	data_not_bstPerf_plt = [{'type':'bar',
					'x':not_bstPerfDf['S2PName'].unique().tolist(),
					'y':not_bstPerfDf['totSale'].tolist(),
					'marker':{'color':'rgba(255, 80, 80, 0.5)',
								'line':{
								'color':'rgba(255, 80, 80, 1)',
								'width': 2
								}
							}
					}]

	itemTrend_df = at.getDataForItemsTrend(df,startDate,endDate,flag)
	#Below is for magic drop down
	itemsListDD = itemTrend_df['S2PName'].unique().tolist()
	
	itemTrend_plt = [{'type':'scatter',
						'x' : itemTrend_df[itemTrend_df['S2PName']==item]['S2BillDate'].tolist(),
						'y' : itemTrend_df[itemTrend_df['S2PName']==item]['totSale'].tolist(),
						'text' : itemTrend_df[itemTrend_df['S2PName']==item]['count'].tolist(),						
						'mode' : 'markers+lines',
						'name' : item,
						'hovertemplate': '<b>Date</b>: %{x}' +
                        '<br><b>Tot Sales</b>: %{y}<br>' +
						'<br><b>Quantity Sold</b>: %{text}<br>',
	}for item in itemsListDD[0:2]]

	itemsListGraph = ','.join(itemsListDD[0:2])
	#print(minDate.strftime('%m/%d/%Y'))
	#print(maxDate.strftime('%m/%d/%Y'))
	# print(itemsListGraph)
	#Need to remove dicts belonging to chart.js
	context = {'startDate':startDate.strftime('%m/%d/%Y'),'endDate':endDate.strftime('%m/%d/%Y'),
	'xaxis_categoryTrend':xaxis_categoryTrend,
	#'data_categoryTrend':data_categoryTrend,
	'data_categoryTrend_pl' : data_plt,
	'category_list': category_list,
	#'dataset_bstPerf':dataset_bstPerf,
	'data_not_bstPerf_plt':data_not_bstPerf_plt,
	#'xaxis_bstPerfBar':xaxis_bstPerfBar,
	'data_bstPerf_plt':data_bstPerf_plt,
	'name':'Ragesh',
	'itemsList':itemsListDD,
	'itemsListGraph':itemsListGraph,
	'itemTrend_plt':itemTrend_plt,
	'cardStartDate':cardStartDate.strftime('%d-%b-%Y'),
	'cardEndDate':endDate.strftime('%d-%b-%Y'),
	'cardStartDate_sales':movingPercentage['daySales_1'],
	'cardEndDate_sales':movingPercentage['daySales_2'],
	'cardStartMonth_sales':movingPercentage['monthSales_1'],
	'cardEndMonth_sales':movingPercentage['monthSales_2'],
	'cardEndMonth':cardStartDate.strftime('%b-%Y'),
	'cardStartMonth':ut.subtractDays(endDate,31).strftime('%b-%Y'),
	'overall_franchise_Sales':overall_franchise_Sales,
	'minDate':minDate.strftime('%m/%d/%Y'),
	'maxDate':maxDate.strftime('%m/%d/%Y'),
	'breakfastSales':breakfastSales,
	'lunchSales':lunchSales,
	'dinnerSales':dinnerSales,
	'pieData':pieData,
	'breakfastTopBar':breakfastTopBar,
	'daySales_percentage':movingPercentage['daySales_percentage'],
	'monthSales_percentage':movingPercentage['monthSales_percentage'],

	}

	return render(request,'home/home1.html',context)
	
	



	
	


