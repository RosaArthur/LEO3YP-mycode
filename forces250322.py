# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 17:36:04 2022

@author: Poca
"""

#force model

def forcemodel(v,t,tstep,d,cd, cd_0, df, W, m, w, n):

    import numpy as np
    import math
    import matplotlib.pyplot as plt
    
    #inputs as speeds, mass, gradient(alpha)
    #output as instantaneous resultant force
    
    g=9.81
    
    # from compile240322 import compilevt
    # [v,t]= compilevt() #v is in m/s
    V= v*(3600/1000) #instantaenous speed in km/h)
    
    #%% tractive force (effort)
    
    #range figures for tractive force (N)
    v1=4.2
    v2=24.9
    v3=45
    #F_tract1= 5000# 0<=v<4.2 
    #F_tract2= 56100-1440v 4.2<=v<24.9
    #F_tract3=33300-525v #24.9<=v<45
    
    #initalise tractive force
    F=  np.zeros(len(v))
    
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
    # plt.xlabel('time (s)') 
    # plt.ylabel('power (kW)') 
    # plt.title('Power profile of whole journey')
    P= alpha_1*beta_1 + P_tract #+ alpha_2 + beta_2
    P_total= P.sum()
    P_max= P.max()   
    #plt.plot(t, P) 
    
    
    #%% energy (kWh) 
    
    E=P*(tstep/(60**2)) #E=P*t
    E_total= E.sum()
    
    
    
    
    #%%
    
    # A_2=9.4/(math.sqrt(w)) + 12.5/w
    # B_2=8*W*V*10**-5
    # C_2=6*(10**-7)*W*V**2
    
    # #running resistance
    # F_d_2=A_2+B_2*V+C_2*V**2 #running resistance in kg/ton
    # F_d_2= F_d_2*W*g #converted in N
    
    A_1=1.43
    B_1=0.0054
    C_1=0.000253
    
    #F_t
    
    #running resistance
    F_d=A_1+B_1*V+C_1*V**2 #running resistance in kg/ton
    F_d= F_d*W*g #converted in N
    
    
    #f= m*g*slope+A/R_L #slope resistance and curve resistance
    
    
    #%%
    
    #using a different model
    
    B= 0.09*m*g
    Q= 2000 +20*v + 3.5*v**2
    
    #F_slope= m*g*sin
    
    RF= F-Q-B #-F_slope
    a= RF/m
    
    #plot the two models against time
    # plt.xlabel('time (s)') 
    # plt.ylabel('force (N)') 
    # plt.title('Force profile of journey')
    # plt.plot(t, F_d)
    # plt.plot(t, Q)
    # b= plt.plot(t, F)
    # plt.legend(['F_d', 'Q','F_t'] )
    
    b= plt.plot(cd,F)
    
    return P, E_total, F_d, F, b