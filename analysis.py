import numpy as np
import pandas as pd
import json
pd.set_option('display.max_rows',None)

def remove_comma(string):
    return string.replace(',','')

def find_month(string):
    month_dict = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    month = int(string.split('/')[1])
    return month_dict[month]

data = pd.read_csv('spending.csv')
data['description'] = data['description'].fillna('misc')

data['amount'] = data['amount'].map(remove_comma).copy()
data['amount'] = data['amount'].astype(int)

#finding the spending by month 
data['month'] = data['date'].apply(find_month)
data_by_month = data.groupby('month',sort=False)['amount'].sum() * -1

#finding the spending by category
data_by_category = data.groupby(['category'])['amount'].sum() * -1
data_by_category = data_by_category[data_by_category>0]

#data for monthly category 
data_monthly_category = data.set_index(['month','category']).copy()
data_monthly_category = data_monthly_category.groupby(level=[0,1],sort=False)['amount'].sum() * -1
data_monthly_category = data_monthly_category[data_monthly_category>0]

#converting json object of data_monthly_category
series = pd.Series(data_monthly_category)

df = series.reset_index()
df.columns = ['Month', 'Category', 'Value']

# Convert the DataFrame to the desired JSON format
result = {}
for index, row in df.iterrows():
    month_data = result.setdefault(row['Month'], {})
    month_data[row['Category'].lower()] = row['Value']

result = pd.DataFrame(result)

result.to_json('data/json_data_monthly_category.json')
data_by_month.to_json('data/json_data_by_month.json')
data_by_category.to_json('data/json_data_by_category.json')
