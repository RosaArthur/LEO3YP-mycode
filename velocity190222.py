# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 16:08:50 2022

@author: Poca
"""

# #inputs
# a=0.8
# t_station= 5*60
# s_avg= 80 #(km/hr) - input, assumption
# s_avg= s_avg*1000*(1/60**2) #m/s
# tstep=1
# d_0=10*1000

def v_profile(a,t_station, s_avg, tstep, d_split):
    
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    
    
    t_journey = 20 #truncated later, must be more than total_dur
    t = np.arange(0,t_journey*60,tstep, dtype=int) #array with 1 second intervals
    
    #initialise
    a = [a] * len(t)
    d_inst = np.zeros(len(t))
    v = np.zeros(len(t))

    #overwrite for accelerating/ stationary
    i=0
    while d_inst.sum() <= 0.5*d_split:
        if v[i]< s_avg: #acceleration
            v[i+1]= v[i] + a[i]*tstep
            d_inst[i]= a[i]*(tstep**2)
            
        elif v[i]>= s_avg: #constant speed
            a[i]=0
            v[i+1]=v[i]
            d_inst[i]= v[i]*tstep
        
        i+=1    

             
    #distance instantaneous for entire journey
    d_now= d_inst[0:i] #mirror velocity
    d_rev= d_now[::-1]
    d_inst[(len(d_now)):(len(d_now)+len(d_rev))] = d_rev

    v_now= v[0:i] #mirror velocity
    v_rev= v_now[::-1]
    v[(len(v_now)):(len(v_now)+len(v_rev))] = v_rev
    t_total = 2*t[i]
    i= 2*i
    total_dur= t_station + t[i]
    #truncate to total duration of travel
    v = v [: total_dur] 
    t = t [: total_dur]
    d_inst = d_inst [: total_dur]
    
    #plt.plot (t,v) 
    

    return v, t, d_inst #, total_dur  


