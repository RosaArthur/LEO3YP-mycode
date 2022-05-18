# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 08:00:39 2022

@author: Poca
"""

#analysis of co2 emission data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
df = pd.read_excel("2005-19_UK_local_and_regional_CO2_emissions.xlsx", "Full dataset", header=1 )

#figure 1 (of different industry totals)
#ro= ['Oxfordshire Total', 'National Total']
co= ['Second Tier Authority', 'Year','Industry Total', 'Commercial Total', 'Public Sector Total', 'Domestic Total', 'Transport Total','LULUCF Net Emissions', 'Grand Total', 'Population (thousands, mid-year estimate)']
df1 = pd.DataFrame(data=df, columns= co)
df2 = df1.loc[df1['Second Tier Authority'] == 'Oxfordshire Total']
df2.columns = ['Second Tier Authority', 'Year','Industry_Total', 'Commercial_Total', 'Public_Sector_Total', 'Domestic_Total', 'Transport_Total','LULUCF_Net_Emissions', 'Grand_Total', 'Population']

#national
df3 = df1.loc[df1['Second Tier Authority'] == 'Oxfordshire Total']

#%%

#percentage drop
total_decrease= abs(df2.iloc[0]['Grand_Total']-df2.iloc[-1]['Grand_Total'])/df2.iloc[0]['Grand_Total']
transport_decrease= abs(df2.iloc[0]['Transport_Total']-df2.iloc[-1]['Transport_Total'])
transport_decrease_percent= transport_decrease/df2.iloc[0]['Transport_Total']

# #plot total
# #plt.plot(df2.Year, df2.Grand_Total, label = 'Grand Total')
# plt.plot(df2.Year, df2.Population, label = 'Population')

# #%%
# figure_1= plt.figure(1)
# plt.plot(df2.Year, df2.Industry_Total, label = 'Industry')
# plt.plot(df2.Year, df2.Commercial_Total, label = 'Commercial')
# plt.plot(df2.Year, df2.Public_Sector_Total, label = 'Public Sector')
# plt.plot(df2.Year, df2.Domestic_Total, label = 'Domestic Sector')
# plt.plot(df2.Year, df2.Transport_Total, label = 'Transport Sector')
# plt.plot(df2.Year, df2.LULUCF_Net_Emissions, label ='LULUCF')
# plt.xlabel('Time (years)') 
# plt.ylabel('CO2 emissions estimates (kt CO2)') 
# plt.legend(plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=2))
# #plt.plot(df2.Year, df2.Grand_Total)

# #'Public_Sector_Total', 'Domestic_Total', 'Transport_Total','LULUCF_Net_Emissions', 'Grand_Total'
# plt.show()


#data=None, index=None, columns=None

#df2= pd.DataFrame(df, index = ro) 
                  #columns = 'Local Authority territorial CO2 emissions estimates 2005-2019 (kt CO2) -  Full dataset'

#%%2019

#for i in ['2018', ]
transportdf = pd.read_excel("Road_Transport_fuel_consumption_tables_2005-2019 (1).xlsx", sheet_name ='2019', header=4 )
transportco= ['Local Authority', 'Buses total','Diesel cars total', 'Petrol cars total', 'Motorcycles total' , 'Diesel LGV total', 'Petrol LGV total']
transportdf1 = pd.DataFrame(data=transportdf, columns= transportco)
transportdfox = transportdf1.loc[transportdf1['Local Authority'] == 'Oxford']
transportdfox.columns = [0,1,2,3,4,5,6]
#make location the key 
transportdfox= transportdfox.set_index(0)

#%%
a= np.zeros(6)
#turn into array

i=0
while i < len(a):
    a[i]= transportdfox.iat[0,i]
    i+=1

#%%
figure_2= plt.figure(2)
#pie chart
#labels
labels= 'Buses','Diesel cars', 'Petrol cars', 'Motorcycles' , 'Diesel LGV', 'Petrol LGV'

#change colours
#pct distance

# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(a, autopct='%1.1f%%', pctdistance=1.13, startangle=180, textprops={'fontsize':14})
#plt.legend(labels,loc=3)
plt.title('Oxford')
# show plot
plt.show()

# #labels = cars

# #values='', names='country',
# #%%
# transportdf1 = pd.DataFrame(data=transportdf, columns= transportco)
# transportdfox = transportdf1.loc[transportdf1['Local Authority'] == 'Oxford'] 
# transportdfwestox =transportdf1.loc[transportdf1['Local Authority'] == 'West Oxfordshire']

