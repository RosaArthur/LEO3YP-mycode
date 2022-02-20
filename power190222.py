# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 16:08:50 2022

@author: Poca
"""

import numpy as np
import math
import matplotlib.pyplot as plt


#inputs
a=0.8
s_avg= 120 #(km/hr) - input, assumption
s_avg= s_avg*1000*(1/60**2) #m/s
tstep=1

#track data(google earth)
d=np.array([10, 7.72, 5.02, 7.195]) #distance(km)
d=d*1000 #in m
#slope data

#train data
# define and have as inputs for time model

#inputs for time
#Beta = [p_carterton, p_witney, p_eynsham] #proportion of passengers embarking or disembarking
Beta = np.array([[0.35,0], [0.35,0.05], [0.3,0.05], [0,0.9]])
#[embarking, disembarking] each row is a station (carterton, witney, eynsham, oxford)
tau= 0.35 #train occupancy rate

from time190222 import tmodel
t_station= int(tmodel(d, a, s_avg, Beta, tau))

from velocity190222 import v_profile
##do for each distance vsplit and then compile into one big v, for use in force

[v_0, t_0, d_0]= v_profile(a,t_station, s_avg, tstep, d[0])

total_d_0= d_0.sum() #total distance travelled
from numpy import cumsum, ones
cd_0= cumsum(d_0) #cumulative distance
#plt.plot(cd_0, v_0)

[v_1, t_1, d_1]= v_profile(a,t_station, s_avg, tstep, d[1])
[v_2, t_2, d_2] = v_profile(a,t_station, s_avg, tstep, d[2])
[v_3, t_3, d_3] = v_profile(a,t_station, s_avg, tstep, d[3])

#%% Velocity Profile of whole journey

#compile into big v
v= np.array([*v_0, *v_1, *v_2, *v_3])
t = np.arange(0,len(v),tstep, dtype=int)

# naming the axes and graoh title
plt.xlabel('time (s)') 
plt.ylabel('velocity (m/s)') 
plt.title('Velocity profile of whole journey')
#plt.plot (t,v)

tf_vcode= np.array([len(t_0), len(t_1), len(t_2), len(t_3)])

#%% tractive force

#range figures for tractive force (N)
v1=4.2
v2=24.9
v3=45
#F_tract1= 5000# 0<=v<4.2 
#F_tract2= 56100-1440v 4.2<=v<24.9
#F_tract3=33300-525v #24.9<=v<45

#initalise tractive force
F=  np.zeros(len(v))
t= np.arange(0, len(v),tstep, dtype=int) #global t

#%%
i=0
while i < len(t):
    if 0<=v[i]<v1 :
        F[i]= 50000
    elif v1<=v[i]<v2:
        F[i]= 56100-(1440*v[i])
    elif v2<=v[i]<v3:
        F[i]=33300-(525*v[i])
    i+=1

#compare
#force_v  = [F, v]


#%% tractive power

u=  np.zeros(len(v)) #intialise u
P_tract=  np.zeros(len(v))

for i in t: 
    u[i]= v[i]*((60**2)/1000) #u in km/h
    P_tract[i]=(F[i]*u[i]*0.746)/(375*1.61) #in kW    
#P_tract.sum()       
        
#%% instantaneous energy consumption (kW) (power at each second)

HEP= 25
alpha_1= HEP
alpha_2= 0.05*HEP
beta_1=1 #eq4

# naming the axes and graoh title
plt.xlabel('time (s)') 
plt.ylabel('power (kW)') 
plt.title('Power profile of whole journey')
P= alpha_1*beta_1 + P_tract #+ alpha_2 + beta_2   
plt.plot(t, P) 


#%% energy (kWh) 

E=P*(tstep/(60**2)) #E=P*t
E_total= E.sum()