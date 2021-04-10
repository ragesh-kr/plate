import pandas as pd


def mapCategories(df,mapping_file):
    df_map = pd.read_excel(mapping_file)
    
    df['S2PName-Category'] = df['Combinations'].map(df_map.set_index('S2PName')['S2PName-Category'])

    return df

def getDfMagicTable(keyword, df_magicTable,mapping_file):
    
    s = df_magicTable.explode('Combinations')
    df = s.loc[s.Combinations.eq(keyword).groupby(level=0).transform('any') & s.Combinations.ne(keyword)]
    df = mapCategories(df,mapping_file)
    
    
    return df


def getDaysTrend(df_days):

	df_days['day_of_week'] = df_days['S2BillDate'].dt.dayofweek
	days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
	df_days['day_name_week'] = df_days['day_of_week'].apply(lambda x: days[x])
	#new_df = df.groupby(['S2BillDate', 'day_name_week','border_color']).agg({'S2PGTotal': ['sum']})
	df_days = df_days.groupby([df_days['S2BillDate'].dt.to_period('d'),'day_name_week'], sort=False)['S2PGTotal'].agg([('totSale','sum')]).reset_index()
	df_days = df_days.sort_values("S2BillDate").reset_index(drop=True)
	df_days['S2BillDate'] = df_days['S2BillDate'].astype('str')

	return df_days



