from django.shortcuts import render
import pandas as pd
from . import analytics as at
from home import analytics as home_at
from django.http import HttpResponse, JsonResponse
import random
from home import utilities as ut
from datetime import datetime as dt
from datetime import timedelta 
from django.contrib.auth.decorators import login_required

path_windows = "C:/Users/591705/django/plate-charts-NewUI/plate/static/data/"
path_mac="/Users/rags/Documents/ScopeAnalytica/plate-charts-NewUI/plate/static/data/"
# Create your views here.
df_raw = pd.read_csv(path_windows+'combo/ComboAnalysisTable.csv')
mapping_file = path_windows+'itemMappingData.xlsx'
df_cols = home_at.readData()
df_raw['Combinations'] = df_raw.Combinations.str.findall("'([^']*)'")




@login_required
def analysis(request):
	#df_cols = home_at.readData()
	
	minDate = df_cols['S2BillDate'].min()
	maxDate = df_cols['S2BillDate'].max()
	startDate =  ut.subtractDays(maxDate,31)
	endDate = maxDate
	df_days = home_at.filter_df_daterange(df_cols,startDate,endDate) 
	df_days = at.getDaysTrend(df_days)
	random.seed(7)
	item = random.choice(df_cols['S2PName'].unique().tolist())


	if request.is_ajax():
		item = request.POST.get('item')
		category = request.POST.get('category')
		#df = pd.read_csv('D:/django/plate-charts/plate/static/data/combo/ComboAnalysisTable.csv')
		#mapping_file = 'D:/RageshP/ScopeAnalytica/skeleton/data/itemMappingData.xlsx'
		#df_cols = home_at.readData()
		#df['Combinations'] = df.Combinations.str.findall("'([^']*)'")
		df = at.getDfMagicTable(item,df_raw,mapping_file)
		df_pieData = df.head()
		categoryFilter = df['S2PName-Category']==category
		df_categorywise = df[categoryFilter]
		df_categorywise = df_categorywise.head()
		pieData = [{'type' : 'pie',
				 'labels' : df_pieData['Combinations'].tolist(),
				 'values' : df_pieData['Count'].tolist(),
				 'textinfo' : 'label+percent',
				 'insidetextorientation' : 'radial',
				 'hole' : .3
		}]

		pieData_category = [{'type' : 'pie',
			 'labels' : df_categorywise['Combinations'].tolist(),
			 'values' : df_categorywise['Count'].tolist(),
			 'textinfo' : 'label+percent',
			 'insidetextorientation' : 'radial',
			 'hole' : .3
		}]

		return JsonResponse({'pieData':pieData,'pieData_category':pieData_category,'item':item,'category':category})



	#df = pd.read_csv('D:/django/plate-charts/plate/static/data/combo/ComboAnalysisTable.csv')
	#df['Combinations'] = df.Combinations.str.findall("'([^']*)'")
	#mapping_file = 'D:/RageshP/ScopeAnalytica/skeleton/data/itemMappingData.xlsx'
	#df_cols = home_at.readData()
	

	'''Below two line code is for price per item analysis'''
	df_priceTrend = df_cols[df_cols['S2PName']==item]
	df_priceTrend_grp = df_priceTrend.groupby([df_priceTrend['S2Rate']], sort=True)['S2PGTotal'].agg([('totSale','mean')]).reset_index()
	priceTrend_line = {'type':'scatter',
						'x' : df_priceTrend_grp['S2Rate'].tolist(),
						'y' : df_priceTrend_grp['S2Rate'].tolist(),
						'mode' : 'markers+lines',
						'yaxis': 'y2',
						'name' : 'price of Item',
						'line':{
						'color':'rgba(255, 99, 132, 1)',
						'width':3,
						},
						'marker': {
							    'color': 'rgb(255, 99, 132, 0.5)',
							    'size': 12
  						}

	}
	priceTrend_bar = {'type':'bar',
						'x' : df_priceTrend_grp['S2Rate'].tolist(),
						'y' : df_priceTrend_grp['totSale'].tolist(),
						'name' : 'Item sale trend',
						'marker':{'color':'rgba(54, 162, 235, 0.2)',
								'line':{
								'color':'rgba(54, 162, 235, 1)',
								'width': 2
								}
							}
						

	}

	priceTrendData = [priceTrend_line,priceTrend_bar]

	
	
	df = at.getDfMagicTable(item,df_raw,mapping_file)
	category=random.choice(df['S2PName-Category'].unique().tolist())

	
	df_pieData = df.head()
	
	categoryFilter = df['S2PName-Category']==category
	df_categorywise = df[categoryFilter]
	df_categorywise = df_categorywise.head()
	
	

	
	pieData = [{'type' : 'pie',
			 'labels' : df_pieData['Combinations'].tolist(),
			 'values' : df_pieData['Count'].tolist(),
			 'textinfo' : 'label+percent',
			 'insidetextorientation' : 'radial',
			 'hole' : .3
	}]
	pieData_category = [{'type' : 'pie',
			 'labels' : df_categorywise['Combinations'].tolist(),
			 'values' : df_categorywise['Count'].tolist(),
			 'textinfo' : 'label+percent',
			 'insidetextorientation' : 'radial',
			 'hole' : .3
	}]
	daysTrend = [{'type':'scatter',
				   'x' : df_days[df_days['day_name_week']==day]['S2BillDate'].tolist(),
				   'y' : df_days[df_days['day_name_week']==day]['totSale'].tolist(),
					#'text' : itemTrend_df[itemTrend_df['S2PName']==item]['Hover'],
					#'text' : day.tolist(),
					'mode' : 'markers+lines',
					'name' : day,
					'visible' : 'legendonly',
					'hovertemplate': '<b>Date</b>: %{x}' +
                        '<br><b>Sale</b>: %{y}<br>',
                        
		}for day in df_days['day_name_week'].unique().tolist()]
	daysTrend[0]['visible']=''
	

	context = {'pieData' : pieData,
			   'pieData_category':pieData_category,
			   'items':df_cols['S2PName'].unique().tolist(),
			   'categories':df_cols['S2PName-Category'].unique().tolist(),
			   'item':item,
			   'category':category,
			   'startDate':startDate.strftime('%m/%d/%Y'),
			   'endDate':endDate.strftime('%m/%d/%Y'),
			   'daysTrend':daysTrend,
			   'minDate':minDate.strftime('%m/%d/%Y'),
			   'maxDate':maxDate.strftime('%m/%d/%Y'),
			   'priceTrendData':priceTrendData,
			   
			   
			   }

	return render(request,'analytics/analytics.html', context)

@login_required
def daysTrend(request):
	if request.is_ajax():
		
		#df_cols = home_at.readData()
		daterange = request.POST.get('daterange').split('-')
		startDate = dt.strptime(daterange[0].strip(),'%m/%d/%Y')
		endDate = dt.strptime(daterange[1].strip(),'%m/%d/%Y')
		df_days = home_at.filter_df_daterange(df_cols,startDate,endDate) 
		df_days = at.getDaysTrend(df_days)
		daysTrend = [{'type':'scatter',
					   'x' : df_days[df_days['day_name_week']==day]['S2BillDate'].tolist(),
					   'y' : df_days[df_days['day_name_week']==day]['totSale'].tolist(),
						#'text' : itemTrend_df[itemTrend_df['S2PName']==item]['Hover'],
						'mode' : 'markers+lines',
						'name' : day,
						'visible' : 'legendonly',
						'hovertemplate': '<b>Date</b>: %{x}' +
                        '<br><b>Sale</b>: %{y}<br>',
			}for day in df_days['day_name_week'].unique().tolist()]
		daysTrend[0]['visible']=''

		return JsonResponse({'daysTrend':daysTrend})
	else:
		return HttpResponse("Wrong page!")


@login_required
def priceTrend(request):
	if request.is_ajax():

		#df_cols = home_at.readData()
		item = request.POST.get('item')
		
		df_priceTrend = df_cols[df_cols['S2PName']==item]
		df_priceTrend_grp = df_priceTrend.groupby([df_priceTrend['S2Rate']], sort=True)['S2PGTotal'].agg([('totSale','mean')]).reset_index()
		
		priceTrend_line = {'type':'scatter',
							'x' : df_priceTrend_grp['S2Rate'].tolist(),
							'y' : df_priceTrend_grp['S2Rate'].tolist(),
							'mode' : 'markers+lines',
							'yaxis': 'y2',
							'name' : 'price of Item',
							'line':{
							'color':'rgba(255, 99, 132, 1)',
							'width':3,
							},
							'marker': {
								    'color': 'rgb(255, 99, 132, 0.5)',
								    'size': 12
	  						}

		}
		priceTrend_bar = {'type':'bar',
							'x' : df_priceTrend_grp['S2Rate'].tolist(),
							'y' : df_priceTrend_grp['totSale'].tolist(),
							'name' : 'Item sale trend',
							'marker':{'color':'rgba(54, 162, 235, 0.2)',
									'line':{
									'color':'rgba(54, 162, 235, 1)',
									'width': 2
									}
								}
							

		}

		priceTrendData = [priceTrend_line,priceTrend_bar]
		return JsonResponse({'priceTrendData':priceTrendData})
	else:
		return HttpResponse("Wrong page!")


