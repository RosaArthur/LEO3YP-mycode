# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 16:08:50 2022

@author: Poca
"""


def v_profile(a,t_station, s_avg, tstep, d_0):

    import numpy as np
    import math
    import matplotlib.pyplot as plt
    
    
    t_journey = 20 #truncated later, must be more than total_dur
    t = np.arange(0,t_journey*60,tstep, dtype=int) #array with 1 second intervals
    
    #initialise
    a = [a] * len(t)
    d = np.zeros(len(t))
    v=  np.zeros(len(t))
    
    #overwrite for accelerating/ stationary
    
    for i in t:
        if v[i]< s_avg: #acceleration
            v[i+1]= v[i] + a[i]*tstep
            d[i]= a[i]*(tstep**2)
            
        elif v[i]>= s_avg: #constant speed
            a[i]=0
            v[i+1]=v[i]
            d[i]= v[i]*tstep
            
        if d.sum()> 0.5*d_0:
            #copy and mirror
            v_now= v[0:i]
            v_rev= v_now[::-1]
            v[i+1:2*i+1] = v_rev
            t_total = 2*t[i]
            i= 2*i
            total_dur= t_station + t[i]
            #truncate to total duration of travel
            v = v [: total_dur] 
            t = t [: total_dur]
            break
      
        
    v_profile = plt.plot (t,v)
    
    return v, t, total_dur, v_profile