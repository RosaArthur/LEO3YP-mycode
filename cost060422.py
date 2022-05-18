#!/usr/bin/env python
# coding: utf-8

# cost modelling comprises of investment costs and operating costs

import numpy as np
import matplotlib.pyplot as plt
# In[ ]:

lifetime= 30 #years
d=np.array([10.003, 7.725, 5.021, 7.201]) # d in km

#values 
#properties of track
new_track_length = d[0]+d[1]+d[2]
track_length= d.sum() #track length in km 

#freq= 30 # no of round trips

#in one week
N_single=872 #3 car train one-way trip
N_double=140 #6 car train one-way trip
N_trips= (N_single + N_double)*52

#TKM = track_length* 2* 365* freq #(TKM over a year) number of round trips* total length of round trip line 
TKM= track_length*N_trips

#properties of station
Nplatform= 2
N_new_stations=4
area_station= 25000 #m^2


#properties of train
Ntrains= 8 #number of trains
#Ltrain= 
Ctrain = 5*10**6


# In[ ]:


#investment costs
#infrastructure

# In[ ]:
#area_station*Nstations*
#
Cland= 3*10**6


# In[ ]:
    
#double track million euros/ km
c_d_easytrack=3
c_d_avgtrack= 10 #300 km/h
c_d_avgtunnel= 30


#bridges
c_shortbridge= 15
c_longbridge= 30

#single track
c_s_easytrack= 3 #1-3
c_s_avgtrack= 7
c_s_avgtunnel= 20

l_s_easytrack= 0.75*0.495*new_track_length
l_d_easytrack= 0.25*0.495*new_track_length

l_s_avgtrack= 0.75*0.495*new_track_length #22.7km= new track length #3/4 single
l_d_avgtrack= 0.25*0.495*new_track_length #1/4 double


l_s_avgtunnel= 0.005*new_track_length #150m of single tunnel
#l_d_avgtunnel= 0.005*new_track_length*

l_shortbridge= 0.005*new_track_length #100m of short bridge

#single and double avg, single and double easy
Cbuild= ((l_s_avgtrack*c_s_avgtrack)+(l_d_avgtrack*c_d_avgtrack)+(l_s_easytrack*c_s_easytrack)+(l_d_easytrack*c_d_easytrack)+(l_s_avgtunnel*c_s_avgtunnel) + (l_shortbridge*c_shortbridge))*10**6


# In[ ]:


c_rail= 0.4*10**6 #60kg/m rail mass cost/km
Csingle= c_rail*0.75*new_track_length #single is one
Cdouble= 2*c_rail*0.25*new_track_length #double is two tracks
Ctrack= Csingle+ Cdouble


# In[ ]:


Celec= 0


# In[ ]:

#signalling costs
Csign=0.6*(10**6)*track_length #0.3-1 Million/km for double #signalling likely to be on double track sections


# In[ ]:


#station and other equipment

#dependent on number of platforms (Nplatform) and train length (Ltrain)
#station, locomotive servie and repair facilities, maintenance shops for rolling stock, track
cstation= 10*10**6 #typical is 5-15 million euros
Cstation = cstation*N_new_stations

# In[ ]:
#rolling stock

Ctrains = Ntrains*Ctrain


# In[ ]:


inv = Cland + Cbuild + Ctrack + Celec + Csign + Cstation + Ctrains

#Cstud detailed design as 10% of capital costs
#feasilbilty, prelimary study and project (cost structure - 3% +)

inv_cost = inv/0.9 #including Cstud

Cstudy= inv_cost -inv

inv_cost= 0.83*inv_cost*1.2211 #conversion into pounds



#%%operational cost


# In[ ]:


Ctraction=0 #since we are producing the energy


# In[ ]:


Cdepreciation = Ntrains*(Ctrain/ lifetime)


# In[ ]:
    
#maintenance data


#how regularly will these costs be incurred


Cmaintenance= 0.72*TKM

# In[ ]:

n_ponboard = 2 #driver and ticket officer
n_pstation = 4 #ground services, operating personnel - 2 attendant per station, 2 control staff + administative   
avg_salary = 32000 #per year

C_ponboard = n_ponboard*Ntrains*avg_salary
C_pstation = n_pstation*N_new_stations*avg_salary
Csalaries= C_ponboard + C_pstation


# In[ ]:


Caccess =0.8*TKM #access/ rail maintenance


# In[ ]:


op_cost= Csalaries+ Cmaintenance + Cdepreciation + Caccess +Ctraction
op_cost= 0.83*op_cost*1.2211 #conversion into pounds
total_op_cost = op_cost*lifetime 


# In[ ]:


total_cost = inv_cost + total_op_cost #investment cost + operating cost

inv_cost= inv_cost/(10**6)
op_cost=op_cost/ (10**6)
total_cost= total_cost/ 1000000

#%%
#money costs more than in 2013
# https://www.inflationtool.com/british-pound/2013-to-present-value 
#1.87% inflation
inflation= 1+ (1.87/100)

total_op_cost= (total_op_cost*inflation) #/(10**6)
op_cost= op_cost*inflation
total_cost= total_cost*inflation

#%%
print('investment =' + str(inv_cost))
print('operational in 1 year =' + str(op_cost))
print('operational over 30 years =' + str(total_op_cost/10**6))
print('total over 30 years =' + str(total_cost))

#imcome from advertisement

# percentages
#%% plots

#pie chart
#labels
#labels= 'Buses','Diesel cars', 'Petrol cars', 'Motorcycles' , 'Diesel LGV', 'Petrol LGV'

#change colours
#pct distance
labels = 'Land', 'Build', 'Track', 'Signalling' , 'Station' , 'Trains', 'Study'
pe= [Cland, Cbuild, Ctrack, Csign , Cstation , Ctrains, Cstudy] #variable for pie chart
#cstudy

# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(pe, autopct='%1.1f%%', pctdistance=1.12, startangle=90, textprops={'fontsize':14})
plt.legend(labels,loc=3)
plt.title('Investment Costs')

# show plot
plt.show()

#%%
#operational
labels2 = 'Salaries', 'Maintenance', 'Depreciation', 'Access'
pe2= [Csalaries, Cmaintenance, Cdepreciation, Caccess] #variable for pie chart
#cstudy

# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(pe2, autopct='%1.1f%%',  pctdistance=1.13, startangle=90, textprops={'fontsize':14})
plt.legend(labels2,loc=3)
plt.title('Operational Costs')

# show plot
plt.show()


#%%

#analysis

C_m= 0.83*1.2211*Cmaintenance/10**6 #maintenance cost in pounds million
C_m_e= 2.5*0.83*1.2211*TKM/10**6
print( str(C_m), str(C_m_e))

#%%

C_elec_lb= 0.5*new_track_length*0.5 + 0.5*new_track_length*0.7
C_elec_ub = 0.5*new_track_length*1.2 + 0.5*new_track_length*0.7
C_elec= (C_elec_lb + C_elec_ub) /2
print( str(C_elec), str(C_elec_ub))
