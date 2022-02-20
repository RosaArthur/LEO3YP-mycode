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


s_avg= 80 #(km/hr) - input, assumption
s_avg= s_avg*1000*(1/60**2) #m/s
tstep=1

#track data(google earth)
d=np.array([10, 7.72, 5.02, 7.195]) #distance(km)
d=d*1000 #in m

from time170222 import tmodel
t_station= int(tmodel(d))

from velocity160222 import v_profile
##do for each distance vsplit and then compile into one big v, for use in force
[v_0, t_0]= v_profile(a,t_station, s_avg, tstep, d[0])
[v_1, t_1]= v_profile(a,t_station, s_avg, tstep, d[1])
[v_2, t_2] = v_profile(a,t_station, s_avg, tstep, d[2])
[v_3, t_3] = v_profile(a,t_station, s_avg, tstep, d[3])

#compile into big v

v= [*v_0, *v_1, *v_2, *v_3]
tf1= np.array([len(t_0), len(t_1), len(t_2), len(t_3)])

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

for i in t: 
    if 0<v[i]<v1 :
        F[i]= 5000
    elif v1<=v[i]<v2:
        F[i]= 56100-(1440*v[i])
    elif v2<=v[i]<v3:
        F[i]=33300-(525*v[i])
        break

# i=0
# while 0<=v[i]<v1 :
#     F[i]= 5000
# i+=1
# while v1<=v[i]<v2:
#     F[i]= 56100-1440*v[i]
# i+=1
# while v2<=v[i]<v3:
#     F[i]=33300-525*v[i]
# i+=1
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


P= alpha_1*beta_1 + P_tract #+ alpha_2 + beta_2    

#%% energy (kWh) 

E=P*(tstep/(60*60))
E_total= E.sum()