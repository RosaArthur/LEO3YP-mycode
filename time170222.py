# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:15:35 2022

@author: Poca
"""
    
def tmodel(d):
    
    #track data(google earth)
    import numpy as np 
    
    #train data
    Ndoors= 2 #doors per car
    capacity=150 #capacity of train
    N_cars= 3
    
    
    W=92 #mass of train (tons)
    m= W*1000 #mass of train (kg) ** tons to tonnes to kg
    w=16 #weight per axle (tons) 
    #*mass will decrease with journey
    
    q=capacity/N_cars #capacity of train car
    
    
    # In[6]:
    
    
    #Beta = [p_carterton, p_witney, p_eynsham] #proportion of passengers embarking or disembarking
    Beta = np.array([[0.35,0], [0.35,0.05], [0.3,0.05], [0,0.9]])
    print(Beta)
    
    #[embarking, disembarking] each row is a station (carterton, witney, eynsham, oxford)
    tau= 0.35 #train occupancy rate
    
    # d= np.array([10, 7.72, 5.02, 7.195]) #distance(km)
    # d=d*1000 #in m
    # #slope data
    
    
    # In[8]:
    
    
    #speed and acceleration inputs
    
    a= 0.8 #acceleration rate (rest to avg_speed) speed converted to m/s^2
    
    s_avg= 80 #(km/hr) - input, assumption
    s_avg= s_avg*1000*(1/60**2) #m/s
    
    
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
    t_margin_depart= 60 #assumption based on doors can close up to a minute before departure
    t_margin= t_margin_arrive + t_margin_depart
    
    
    # In[12]:
    
    
    t_board= 0.1*60 #time of embarking or disembarking per passenger (s) (assumption) 6seconds
    
    
    # In[13]:
    
    #dwell time
    #tau=0.35
    t_station = t_margin + N_cars*2*(t_board*tau*q)/Ndoors # for all stations (embark and disembark)
    print(t_station/60)
    
    #t_board_c= (t_board*Beta[0][0]*tau*q)/Ndoors + (t_board*Beta[1][0]*tau*q)/Ndoors 
    
    #w_e
    #e_o
    
    #t_station = t_margin + (t_board*Beta[]*tau*q)/Ndoors + (t_board*Beta[]*tau*q)/Ndoors # station breakdown 
    
    
    # In[14]:
    
    
    #time of train in motion
    #t_avg from 4 parts of journey
    #accelerates and decelerates 8 times in total
    t_track = 2*4*t_acc + t_avg[0] +t_avg[1] +t_avg[2] + t_avg[3]
    print(t_track/60)
    
    tf= (2*t_acc) + t_avg
    
    print()
    
    # In[16]:
    
    
    #journey time
    
    t_journey= t_station + t_track #4 stations, 4 betas, 4 dwell times, index t_station
    print(t_journey/60)
    
    return t_station
