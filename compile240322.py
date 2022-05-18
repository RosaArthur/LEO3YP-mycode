# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 16:08:50 2022

@author: Poca
"""


def compilevt(Ndoors, capacity, N_cars, W, m, w, tstep):
    
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    
    
    #inputs
    a=0.8
    s_avg= 120 #(km/hr) - input, assumption based on max
    s_avg= s_avg*1000*(1/60**2) #m/s
    
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
    
    from time240322 import tmodel
    t_station= int(tmodel(d, a, s_avg, Beta, tau, Ndoors, capacity, N_cars, W, m, w))
    
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
    
    cd_1=cumsum(d_1)+ cd_0[-1]
    cd_2=cumsum(d_2)+ cd_1[-1]
    cd_3=cumsum(d_3)+ cd_2[-1]
    
    #%% Velocity Profile of whole journey
    
    #compile into big v
    v= np.array([*v_0, *v_1, *v_2, *v_3])
    d=np.array([*d_0, *d_1, *d_2, *d_3])
    cd= np.array([*cd_0, *cd_1, *cd_2, *cd_3])
    t = np.arange(0,len(v),tstep, dtype=int)
    
    # naming the axes and graph title
    #plt.xlabel('time (s)') 
    #plt.ylabel('velocity (m/s)') 
    #plt.title('Velocity profile of whole journey')
    #fig, axs =plt.subplots(2)
    #plt.plot (t,v, "r")
    
    tf_vcode= np.array([len(t_0), len(t_1), len(t_2), len(t_3)])


    return v, t, cd_0, cd, d