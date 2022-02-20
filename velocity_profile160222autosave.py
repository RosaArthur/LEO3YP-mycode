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
t_station= 5*60
s_avg= 80 #(km/hr) - input, assumption
s_avg= s_avg*1000*(1/60**2) #m/s
tstep=1
d_0=10*1000

#track data(google earth)
d=np.array([10, 7.72, 5.02, 7.195]) #distance(km)
d=d*1000 #in m

from 160222 import v_profile
##do for each distance vsplit and then compile into one big v, for use in force
v_0= v_profile(a,t_station, s_avg, tstep, d[0])
#v_1= v_profile(a,t_station, s_avg, tstep, d[1])
#v_2= v_profile(a,t_station, s_avg, tstep, d[2])
#v_3= v_profile(a,t_station, s_avg, tstep, d[3])

#compile into big v
#%% tractive force

#range figures for tractive force (N)
v1=4.2
v2=24.9
v3=45
#F_tract1= 5000# 0<=v<4.2 
#F_tract2= 56100-1440v 4.2<=v<24.9
#F_tract3=33300-525v #24.9<=v<45

#initalise tractive force
F=  np.zeros(len(t))

for i in t: 
    if 0<=v[i]<v1 :
        F[i]= 5000
    elif v1<=v[i]<v2:
        F[i]= 56100-1440*v[i]
    elif v2<=v[i]<v3:
        F[i]=33300-525*v[i]
        break
#%% tractive power

u=  np.zeros(len(t)) #intialise u
u[i]= v[i]/(1000*(1/60**2)) #u in km/h
P_tract=(F[i]*u[i]*0.746)/(375*1.61) #in kW   
        
        
#%% instantaneous energy consumption (kW)

HEP= 25
alpha_1= HEP
alpha_2= 0.05*HEP
beta_1=1 #eq4


P= alpha_1*beta_1 + P_tract #+ alpha_2 + beta_2     