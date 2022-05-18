# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 22:44:51 2022

@author: Poca
"""

def tractiveforce(V,v,t,tstep,d,cd, cd_0, df, W, m, w, n):

    import numpy as np
    import math
    import matplotlib.pyplot as plt
    
    # tractive force using a higher fidelity model
      
    #starting tractive effort

    #variables defined earlier
    #W weight in tons
    #w weight per railcar axle
    #n number of axles per car
    #V in km/h
    K=0.07      #K train drag coefficient
    #theta road grade (%) linear between points         
    #L distance (m) train moved in 1 second  
    ft_2=  np.zeros(len(cd_0))
    theta= np.zeros(len(cd_0)) #change to t later


    j=0
    slope_i=0

    #index as slope_i
    while slope_i < df.shape[0]-1: #number of rows in df

        #over course of journey in time
        while j < len(cd_0): #len(t)
        
            #find the distances in table it's between to at a given time (checking each)
            if  df.loc[slope_i,'distance']< cd[j] <df.loc[slope_i +1,'distance']:
                x1= df.loc[slope_i,'distance']
                x2= cd[j]
                x3= df.loc[slope_i+1,'distance']
                y1= df.loc[slope_i,'slope']
                y3= df.loc[slope_i +1,'slope']
            #linearly interpolate slope
                theta[j] = y1+ ((x2-x1)*(y3-y1))/(x3-x1)
                
            #tractive force
                ft_2[j]= 4.4482*W*(0.6+(20/w)+(0.01*V[j]/1.61)+ (K*((V[j]/1.61)**2)/w*n) + (20*theta[j]) + ((70*(V[j])**2-(V[j-1])**2)/8.4*d[j]))
            #issue with j-1 at the start
                j += 1
            #elif cd[j] >= df.loc[slope_i,'distance']: #extrapolate for those at upper ends
                #theta[j] = 2
                #j+=1
            else:
               
                break 
     
#then do for next distance
    slope_i += 1
    
    c=plt.plot(cd_0, ft_2)
    
    #%% tractive power
    
    u=  np.zeros(len(cd_0)) #intialise u
    P_tract=  np.zeros(len(cd_0))
    
    for i in cd_0: 
        u[i]= v[i]*((60**2)/1000) #u in km/h
        P_tract[i]=(ft_2[i]*u[i]*0.746)/(375*1.61) #in kW    
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
    
    e= plt.plot(t, P) 
    
    return c, e