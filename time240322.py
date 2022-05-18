# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:15:35 2022

@author: Poca
"""
    
def tmodel(d, a, s_avg, Beta, tau, Ndoors, capacity, N_cars, W, m, w):
    
    q=capacity/N_cars #capacity of train car
    
    
    # In[9]:
    
    #acceleration and deceleration
    
    d_acc= (s_avg**2)/(2*a) #using train acceleration data #distance over which train accelerates (km)
    
    t_acc=s_avg/a #time spent accelerating (s)
    
    
    # In[10]:
    
    
    #avg runnning speed
    
    d_avg_s= d - 2*d_acc #distance travelling at average speed
    t_avg= d_avg_s/s_avg #time travelling at avg speed for each split (s)
    
    # In[11]:
    
    
    #operational margin
    t_margin_arrive= 30 #assumption
    t_margin_depart= 30 #assumption 
    t_margin= t_margin_arrive + t_margin_depart
    
    
    # In[12]:
    
    
    t_board= 0.08*60 #time of embarking or disembarking per passenger (s) (assumption) 5seconds
    
    
    # In[13]:
    
    #dwell time
    #tau=0.35
    t_station = t_margin + 2*(t_board*tau*q)/Ndoors # for all stations (embark and disembark)
    print('time station=' + str(t_station/60))
    
    #t_board_c= (t_board*Beta[0][0]*tau*q)/Ndoors + (t_board*Beta[1][0]*tau*q)/Ndoors 
    
    #w_e
    #e_o
    
    #t_station = t_margin + (t_board*Beta[]*tau*q)/Ndoors + (t_board*Beta[]*tau*q)/Ndoors # station breakdown 
    
    
    # In[14]:
    
    
    #time of train in motion
    #t_avg from 4 parts of journey
    #accelerates and decelerates 8 times in total
    t_track = 2*4*t_acc + t_avg[0] +t_avg[1] +t_avg[2] + t_avg[3]
    #print(t_track/60)
    
    tf= (2*t_acc) + t_avg + t_station
    
    
    # In[16]:
    
    
    #journey time
    
    t_journey= tf.sum() #4 stations, 4 betas, 4 dwell times, index t_station
    print('journey time=' + str(t_journey/60))
    
    return t_station
