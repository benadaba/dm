import pandas as pd
import numpy as np
import datetime as dt
import time
from datetime import datetime

#Now, load the input data file and parse the Order Date column.
#data = pd.read_csv('data.txt', sep='|', names=['Date','OrderNumber','CustomerId', 'ProductId','Value'])
data = pd.read_csv('data.txt')
data['ParsedDate'] = data['Date'].apply(lambda x: dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))

#NOW = dt.datetime(2016,8,18)
NOW = dt.datetime.now()

timestamp = int(time.mktime(datetime.now().timetuple()))
#now1 = datetime.fromtimestamp(timestamp)
'''
To calculate the actual RFM table, use the Split-Apply-Combine pattern:
Split the data into groups based on some criteria (Customer Id in our case).
Apply a function to each group independently.
Combine the result into a new data structure.
We will group the data by Customer Id and apply three different functions to each column. We provide them as anonymous lambda functions inside a dictionary with keys indicating columns to which they are to be applied.
'''

rfmTable = data.groupby('CustomerId').agg({ 'ParsedDate': lambda x: (NOW - x.max()).days, # R
                                            'OrderNumber': lambda x: len(x), # F
                                            'Value': lambda x: x.sum()}) # M
                                            
#rfmTable = data.groupby('CustomerId').agg({ 'ParsedDate': lambda x: int(time.mktime(datetime(NOW - x.max()).days.timetuple())), # R
#                                            'OrderNumber': lambda x: len(x), # F
#                                            'Value': lambda x: x.sum()}) # M
                                            
                                            
                                            
#rfmTable['ParsedDate'] = rfmTable['ParsedDate'].astype(int)
rfmTable['ParsedDate'] = rfmTable['ParsedDate']                                       
#rfmTable['ParsedDate'] = rfmTable['ParsedDate'].datetime.utcnow().strftime("%s") 
rfmTable['ParsedDate'] = int(time.mktime(rfmTable.ix[:,['ParsedDate']].timetuple()))
#import datetime
#
#def to_integer(dt_time):
#    return 10000*dt_time.year + 100*dt_time.month + dt_time.day
#
#to_integer(datetime.date(rfmTable['ParsedDate']))

#.astype(int)
rfmTable.rename(columns={'ParsedDate': 'R', 'OrderNumber': 'F', 'Value': 'M'}, inplace=True)
rfmTable.sort(columns='R', ascending=False)
rfmTable
