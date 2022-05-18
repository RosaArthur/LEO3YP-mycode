# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:53:06 2022

@author: Poca
"""


#tractive force inline
import pandas as pd
import math

#track data(google earth)
#import track data
df = pd.read_excel("elevationdata.xlsx")  
df= pd.DataFrame(df, columns= ['distance', 'slope'])
  
#train data
Ndoors= 2 #doors per car
capacity=150 #capacity of train
N_cars= 3


w_a=20 #weight per axle (tons) 
n=8 #number of axles per car
#*mass will decrease with journey
W=w_a*n*3 #mass of train (tons)
m= W*1000 #mass of train (kg) ** tons to tonnes to kg

n_people= 220
w_person= 65*0.00110231#avg person (in tons)
M= n_people*w_person + W

tstep=1 #for v and force profile

#inputs
a=0.8
s_avg_kph= 120 #(km/hr) - input, assumption based on max
s_avg_ms= s_avg_kph*1000*(1/60**2) #m/s

#velocity profile over whole journey
from compile290322 import compilevt
[v,t,cd_0, cd, d, a_i]= compilevt(a, s_avg_ms, Ndoors, capacity, N_cars, W, m, w_a, tstep) #input a is a scalar, output a is a vector

a=a_i
#%%

import numpy as np
import math
import matplotlib.pyplot as plt

#inputs as speeds, mass, gradient(alpha)
#output as instantaneous resultant force

g=9.81

# from compile240322 import compilevt
# [v,t]= compilevt() #v is in m/s
v_kph= v*(3600/1000) #instantaenous speed in km/h)


#%% tractive force using a higher fidelity model
  
#starting tractive effort

#variables defined earlier
#W weight in tons
#w weight per railcar axle
#n number of axles per car
#V in km/h
K=0.07      #K train drag coefficient
#theta road grade (%) linear between points         
#L distance (m) train moved in 1 second  
ft_2=  np.zeros(len(t))
ft_3= np.zeros(len(t))
theta= np.zeros(len(cd)) #change to t later
end_term= np.zeros(len(t))
init_term= np.zeros(len(t))

#starting tractive effort data
track_r= 0 #60kg rail, =1 for 52kg  track resistance
track_c= 0 #good track condition, =2 poor rails, good crossties, 
dry = 0#dry rail
wet= 2 #wet rail
n_wet = 100
icy= 10#icy rail
n_icy = 33.7 #met office data
weather_r= ((wet*n_wet) + (icy*n_icy))/365
avg_UK_temp= 51.926 #farenheit (15.02C - 7.12)=11.07 avg
bearing_r= 10 -0.1*(avg_UK_temp-50)


j=0
slope_i=0

#index as slope_i
while slope_i < df.shape[0]-1: #number of rows in df

    #over course of journey in time
    while j < len(t): #len(t)
    
        #issue with j-1 at the start
        #find the distances in table it's between to at a given time (checking each)
        if  j==0 : # initially we do not want j-1 term involved
            
        #tractive force + (20*theta[j])
        
            ft_2[j]= 4.4482*M*((0.6+(20/w_a) +(0.01*v_kph[j]/1.61) + (K*((v_kph[j]/1.61)**2)/(w_a*n)))) #+ (70*((V[j])**2-(V[j-1])**2)/(8.4*d[j])))
            ft_3[j]= 0.0005*M*907.185*(track_r + track_c + weather_r + bearing_r)# + grade_r)  #lb/ton -> N/kg -> N

            j += 1
            
        #elif cd[j] >= df.loc[slope_i,'distance']: #extrapolate for those at upper ends
            #theta[j] = 2
            
        elif v_kph[j]==0 and v_kph[j-1]==0: #if stationary, ft_2= 0, no tractive effort
            
            ft_2[j] =0
            
            j+=1
        
        elif v_kph[j]>0 and v_kph[j-1]==0:
            ft_3[j]= 0.0005*M*907.185*(track_r + track_c + weather_r + bearing_r)# + grade_r)  #lb/ton -> N/kg -> N

            j += 1
            
        elif v_kph[j]==0 and v_kph[j-1]<1:
            ft_2[j] =0
            
            j+=1
            
        # elif v_kph[j]==0 and v_kph[j-1]<1:# for the deceleration last term with speed, then 0, we want all terms but div by 0 (last term)
        #     init_term[j]= (0.6+(20/w_a) +(0.01*v_kph[j]/1.61) + (K*((v_kph[j]/1.61)**2)/(w_a*n)))
        #     ft_2[j]= 4.4482*W*(init_term[j])
        #     j+=1
            
        #find the distances in table it's between to at a given time (checking each)
        elif  df.loc[slope_i,'distance']< cd[j] <df.loc[slope_i +1,'distance']: #and v_kph[j]>0:
            x1= df.loc[slope_i,'distance']
            x2= cd[j]
            x3= df.loc[slope_i+1,'distance']
            y1= df.loc[slope_i,'slope']
            y3= df.loc[slope_i +1,'slope']
        #linearly interpolate slope
            theta[j] = y1+ ((x2-x1)*(y3-y1))/(x3-x1)
                
            
        #tractive force + (20*theta[j])
            end_term[j] = 70*(((v_kph[j])**2)-((v_kph[j-1])**2))/(8.4*d[j])
            init_term[j]= (0.6+(20/w_a) +(0.01*v_kph[j]/1.61) + (K*((v_kph[j]/1.61)**2)/(w_a*n)))
            ft_2[j]= 4.4482*W*(init_term[j]+ end_term[j])
        
            j += 1
            
        #elif cd[j] >= df.loc[slope_i,'distance']: #extrapolate for those at upper ends
            #theta[j] = 2
            #j+=1
            
        # elif 0 <v_kph[j]< s_avg_kph: #sqrt during acceleration
        
        #     end_term[j] = 70*(((v_kph[j])**2)-((v_kph[j-1])**2))/(8.4*d[j])
        #     ft_2[j]= 4.4482*W*(0.6+(20/w_a) +(0.01*v_kph[j]/1.61) + (K*((v_kph[j]/1.61)**2)/(w_a*n)) + end_term[j])
        #     j+= 1
            
        else:
           
            break 
     
    #then do for next distance
    slope_i += 1



#%% tractive power

P_tract=  np.zeros(len(t))


for i in t[0:len(t)]: 
    P_tract[i]=(ft_2[i]*v_kph[i]*0.746)/(375*1.61) #in kW    
    #P_tract.sum()       


#%% instantaneous energy consumption (kW) (power at each second)

HEP= 25
alpha_1= HEP
alpha_2= 0.05*HEP
beta_1=1 #eq4
beta_2=0 # model begins from beginning of trip, no point for no ventilation/ lights

#distinction in power with positve and neg/0 tractive power
# correct alphas/betas

#initalise P, overall power
P= np.zeros(len(t))

i=0
while i< len(t): 
    if P_tract[i]>0:
        P[i]= alpha_1*beta_1 + P_tract[i] + alpha_2*beta_2
    elif P_tract[i]<=0: #if stationary/ neg tractive effort, this is not in power req
        P[i]= alpha_1*beta_1 + alpha_2*beta_2
    i+=1
    
P_max= P.max()

# naming the axes and graoh title
# plt.xlabel('time (s)') 
# plt.ylabel('power (kW)') 
# plt.title('Power profile of whole journey')

plt.plot(cd[0:341], theta[0:341])

# g= plt.figure(1)
# plt.subplot(311)
# plt.plot (t, P) #[0:len(theta)] #ft_2
# plt.subplot(312)
# plt.plot (t, ft_2)
# plt.subplot(313)
# plt.plot (t, v)


#power and forces
#from forces240322 import forcemodel
#[P, E_total, F_d, F, slope_plot]= forcemodel(v,t,tstep,d,df, W, m, w, n)

#%% energy consumption(kWh)

E=P*(tstep/(60**2)) #E=P*t
E_total= E.sum()

#%% regenerative braking

regen_eff= np.zeros(len(t)) #initialise regenerative efficiency
E_re= np.zeros(len(t)) #initialise regenerated energy
alpha= 0.65

#calculate regenerated efficiency to use in regenerated energy calc

i =0
while i< len(t) :
      if a[i]<0: #during deceleration
          regen_eff[i]= 1/((math.e)**abs(alpha/a[i]))  #regenerative efficiency
          E_re[i]= regen_eff[i]*P[i] # for positive P
      else:
          regen_eff[i]= 0
          E_re[i]= regen_eff[i]*P[i]
      i+=1

# E_avg = np.zeros(len(t))
# E_avg = (E_re+ E)/ d.sum() 








