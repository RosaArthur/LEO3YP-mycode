#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import math
import matplotlib.pyplot as plt


# In[3]:


#constants
g=9.81


# In[4]:


#train data
Ndoors= 2 #doors per car
capacity=150 #capacity of train
N_cars= 3


W=92 #mass of train (tons)
m= W*1000 #mass of train (kg) ** tons to tonnes to kg
w=16 #weight per axle (tons) 
#*mass will decrease with journey

q=capacity/N_cars #capacity of train car


# In[ ]:





# In[6]:


#Beta = [p_carterton, p_witney, p_eynsham] #proportion of passengers embarking or disembarking
Beta = np.array([[0.35,0], [0.35,0.05], [0.3,0.05], [0,0.9]])
print(Beta)

#[embarking, disembarking] each row is a station (carterton, witney, eynsham, oxford)
tau= 0.35 #train occupancy rate


# In[7]:


#track data(google earth)
d=np.array([10, 7.72, 5.02, 7.195]) #distance(km)
d=d*1000 #in m
print(d)
#slope data


# In[8]:


#speed and acceleration inputs

a= 0.8 #acceleration rate (rest to avg_speed) speed converted to m/s^2
print (a)

s_avg= 80 #(km/hr) - input, assumption
s_avg= s_avg*1000*(1/60**2) #m/s
print(s_avg)


# In[9]:


#acceleration and deceleration

d_acc= (s_avg**2)/(2*a) #using train acceleration data #distance over which train accelerates (km)
print(d_acc)

t_acc=s_avg/a #time spent accelerating (s)
print (t_acc)


# In[10]:


#avg runnning speed

d_avg_s= d - 2*d_acc #distance travelling at average speed
print (d_avg_s)
t_avg= d_avg_s/s_avg #time travelling at avg speed for each split (s)
print (t_avg/60)


# In[ ]:


#force model
#V= #V (instantaenous speed in km/h)
alpha #(instantaneous gradient )

A=9.4/(math.sqrt(w)) + 12.5/w
B=8*10**-5*W*V
C=6*10**-7*W*V**2


#F_t
F_d=A+Bv+Cv**2 #running resistance in kg/ton
F_d= F_d*W*g #running resistance in N
#f= m*g*slope+A/R_L #slope resistance and curve resistance


# In[ ]:


#Energy calculation

#energy and power requirements for accelerating
F= m*a
E_acc=F*d_acc
P_acc= E_acc/t_acc

#energy and power requirements for average journey
E_avg_s= 1/2 *m* (s_avg)^2
P_avg_s= E_avg_s/t_avg


# In[11]:


#operational margin
t_margin_arrive= 30 #assumption
t_margin_depart= 60 #assumption based on doors can close up to a minute before departure
t_margin= t_margin_arrive + t_margin_depart


# In[12]:


t_board= 0.1*60 #time of embarking or disembarking per passenger (s) (assumption)


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


# In[16]:


#journey time

t_journey= t_station + t_track #4 stations, 4 betas, 4 dwell times, index t_station
print(t_journey/60)


# In[17]:



print(t_avg)
from numpy import cumsum, ones
ct_avg= cumsum(t_avg)
for n in range(4): 
    count = 5
    if n==0 and count>0:
        ct_avg=np.zeros(5)
        #count= count - 1
    
    print(n)
    
    print(ct_avg)
    
    #print(ct_avg[n-1])

    
from numpy import cumsum, ones
a = np.array([[1], [2], [3], [4]])
#print(a)
#print(cumsum(a))
#array([  1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.])


# In[27]:


#speed/acceleration/ deceleration profile
t_journey=31
t = np.arange(0,t_journey*60,1, dtype=int) #array with 1 second intervals
#print(t)

#initialise speed array # it is at average speed for majority of time
speed = [s_avg] * len(t) 

#cumulative time spent at avg speed
from numpy import cumsum, ones
ct_avg= cumsum(t_avg)


#initialise
inst_d= = np.arange(0,t_journey*60,1, dtype=int)
d_0=d[0]

#overwrite for accelerating/ stationary

for i in t:
    if v< s_avg:
        s_acc= a*t[i]#instantaneous speed
        
        #print(s_acc)
        speed[i]= s_acc
        
        
        
        
        
        
        
        
for n in range(4):
        
        #elif 2*n*t_acc + n*t_station + ct_avg[n-1] < i < ((2*n)+1)*t_acc + n*t_station + ct_avg[n-1]:#time spent accelerating
#0-t_acc, etc etc
            #s_acc= a*t[i]#instantaneous speed while accelerating
            #speed[i]= s_acc

        #elif ((2*n)+1)*t_acc + n*t_station + ct_avg[n] < i < ((2*n)+2)*t_acc + n*t_station + ct_avg[n]: #time decelerating
                                                #t_acc+t_avg - 2*t_acc + t_avg #tavg is split station wise e.g. t_avg[0]
            # t_dec as time begins upon deceleration
            #t_dec = i- (((2*n)+1)*t_acc + n*t_station + ct_avg[n-1]) 
        
            #s_dec= s_avg -a*t_dec 
            #speed[i] = s_dec
 
        
        #elif ((2*n)+2)*t_acc + ct_avg[n] + n*t_station < i < ((2*n)+2)*t_acc + ct_avg[n] + (n+1)*t_station: #time stationary (at station)
            #speed[i]=0

print(speed)


# In[23]:


#plt.plot(t,speed)
#plt.xlabel= ('time(s)')
#plt.ylabel=('speed(m/s)')


# In[ ]:




