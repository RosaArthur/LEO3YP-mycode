#!/usr/bin/env python
# coding: utf-8

# cost modelling comprises of investment costs and operating costs

import numpy as np

# In[ ]:

lifetime= 30 #years
d=np.array([10, 7.72, 5.02, 7.195]) # d in km

#values 
#properties of track
track_length= d.sum() #track length in km 
freq= 30
TKM = track_length* 2* 365* freq #(TKM over a year) number of round trips* total length of line 

#properties of station
Nplatform= 2
Nstations=4

#properties of train
Ntrains= 5 #number of trains
#Ltrain= 
Ctrain = 5*10**6


# In[ ]:


#investment costs
#infrastructure

# In[ ]:

#
Cland= 0


# In[ ]:
    
#double track million euros/ km
c_easytrack=3
c_avgtrack= 10 #300 km/h
c_avgtunnel= 30
c_shortbridge= 15
c_longbridge= 30

l_easytrack= 0.495*track_length
l_avgtrack= 0.495* track_length
l_avgtunnel= 0.005*track_length #150m of tunnel
l_shortbridge= 0.005*track_length #100m of short bridge

Cbuild= ((l_avgtrack*c_avgtrack)+(l_easytrack*c_easytrack)+(l_avgtunnel*c_avgtunnel))*10**6


# In[ ]:


c_rail= 0.4*10**6#60kg/m rail mass cost/km
Ctrack= c_rail*track_length


# In[ ]:


Celec= 0


# In[ ]:

#signalling costs
Csign=0.6*(10**6)*track_length #0.3-1 Million/km for double


# In[ ]:


#station and other equipment

#dependent on number of platforms (Nplatform) and train length (Ltrain)
#station, locomotive servie and repair facilities, maintenance shops for rolling stock, track
cstation= 10*10**6 #typical is 5-15 million euros
Cstation = cstation*Nstations

# In[ ]:
#rolling stock

Ctrains = Ntrains*Ctrain


# In[ ]:


inv = Cland + Cbuild + Ctrack + Celec + Csign + Cstation + Ctrains

#Cstud detailed design as 10% of capital costs
#feasilbilty, prelimary study and project (cost structure - 3% +)

inv_cost = inv/0.9 #including Cstud

inv_cost= 0.83*inv_cost*1.2211 #conversion into pounds



#%%operational cost


# In[ ]:


Ctraction=0 #since we are producing the energy


# In[ ]:


Cdepreciation = Ntrains*(Ctrain/ lifetime)


# In[ ]:
    
#maintenance data


#how regularly will these costs be incurred


Cmaintenance= 2.5*TKM
# https://www.researchgate.net/publication/272913387_Analysis_and_modeling_of_rail_maintenance_costs


# In[ ]:

n_ponboard = 2 #driver and ticket officer
n_pstation = 4 #ground services, operating personnel - 2 attendant per station, 2 control staff + administative   
avg_salary = 32000 #per year

C_ponboard = n_ponboard*Ntrains*avg_salary
C_pstation = n_pstation*Nstations*avg_salary
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

#imcome from advertisement

# percentages

