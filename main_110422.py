# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:53:06 2022

@author: Poca
"""
#different a

#tractive force inline
import pandas as pd
import math

#track data(google earth)
#import track data
df = pd.read_excel("elevation1.xlsx")  
df= pd.DataFrame(df, columns= ['distance', 'slope'])
  
#train data
Ndoors= 2 #doors per car
capacity=200 #capacity of train
N_cars= 3


w_a=20 #weight per axle (tons) 
n=8 #number of axles per car
#*mass will decrease with journey
W=w_a*n*N_cars #mass of train (tons)
m= W*1000 #mass of train (kg) ** tons to tonnes to kg
conv= 0.0005*907.185 # lb/ton > kg/ton
n_people= 200
w_person= 65*0.00110231#avg person (in tons)
M= n_people*w_person + W

tstep=1 #for v and force profile

#inputs
a=1.2
print('a =' + str(a))
s_avg_kph= 120 #(km/hr) - input, assumption based on max
s_avg_ms= s_avg_kph*1000*(1/60**2) #m/s

#velocity profile over whole journey
from compile300322 import compilevt
[v,t,cd_0, cd, d_inst, a_i]= compilevt(a, s_avg_ms, Ndoors, capacity, N_cars, W, m, w_a, tstep) #input a is a scalar, output a is a vector

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

#inst acceleration calculation
k=0
while k<len(t):
    if k==0:
        a_i[k]=0.8
    else: #acceleration as difference in speed (v=constant, a=0)
        a_i[k]= (v[k]-v[k-1])/tstep
        
    k+=1

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
slope_term= np.zeros(len(t))
init_term= np.zeros(len(t))

#starting tractive effort data
track_r= 0 #60kg rail, =1 for 52kg  track resistance
track_c= 0 #good track condition, =2 poor rails, good crossties, 
dry = 0#dry rail
wet= 2 #wet rail
n_wet = 110
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
            
            
        if v_kph[j]==0 and v_kph[j-1]==0 : # and v_kph[j+1]==0 and j<(len(t)-)  #if stationary, ft_2= 0, no tractive effort
            # won't do for last one since +1 will be outside range
            
            ft_2[j] =0 #0
            
            j+=1
        
            
        #find the distances in table it's between to at a given time (checking each)
        elif  df.loc[slope_i,'distance']< cd[j] <df.loc[slope_i +1,'distance']: #and v_kph[j]>0:
            x1= df.loc[slope_i,'distance']
            x2= cd[j]
            x3= df.loc[slope_i+1,'distance']
            y1= df.loc[slope_i,'slope']
            y3= df.loc[slope_i +1,'slope']
        #linearly interpolate slope
            theta[j] = y1+ ((x2-x1)*(y3-y1))/(x3-x1)
                
            
        #tractive force terms
            init_term[j]= (0.6+(20/w_a) +(0.01*v_kph[j]/1.61) + (K*((v_kph[j]/1.61)**2)/(w_a*n)))
            slope_term[j]=(20*theta[j])
            #end term defined later
            
            if slope_term[j]<0:
                    slope_term[j]=0
           
            #issue with j-1 at the start
            #find the distances in table it's between to at a given time (checking each)
            if  j==0 : # initially we do not want j-1 term involved
                
            #tractive force + (20*theta[j])
            
                #ft_2[j]= 4.4482*M*((0.6+(20/w_a) +(0.01*v_kph[j]/1.61) + (K*((v_kph[j]/1.61)**2)/(w_a*n)))) #+ (70*((V[j])**2-(V[j-1])**2)/(8.4*d[j])))
                ft_2[j]= conv*M*(track_r + track_c + weather_r + bearing_r + slope_term[j])  #lb/ton -> N/kg -> N

                j += 1
                
            #elif cd[j] >= df.loc[slope_i,'distance']: #extrapolate for those at upper ends
                #theta[j] = 2
                
            elif v_kph[j-1]==0 and v_kph[j]==0 and j<(len(t)-1) and v_kph[j+1]>0 :
                ft_3[j]= conv*M*(track_r + track_c + weather_r + bearing_r + slope_term[j])  #lb/ton -> N/kg -> N
#0.0005*M*907.185
                j += 1
        
            elif v_kph[j]==0 and v_kph[j-1]>0:
                
                # for the deceleration last term with speed, then 0, we want all terms but div by 0 (last term)
                ft_2[j]= 4.4482*M*(init_term[j] + slope_term[j])
                j+=1
                
            else: 
                #redefine acceleration
    
                
                # if v_kph[j]<v_kph[j-1]: #deceleration
                #     a[j]= (v_kph[j]-v_kph[j-1])/tstep #defining the deceleration value(negative)
                
                end_term[j] = 70*(((v_kph[j])**2)-((v_kph[j-1])**2))/(8.4*d_inst[j])
                ft_2[j]= conv*M*(init_term[j]+ slope_term[j]+ end_term[j])
        
                j +=1
            
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
P_nonre= np.zeros(len(t))

i=0
while i< len(t): 
    if P_tract[i]==0: #if stationary - no power req
        P_nonre[i]= alpha_1*beta_1 + alpha_2*beta_2
        
    else:
        P_nonre[i]= alpha_1*beta_1 + P_tract[i] + alpha_2*beta_2
    i+=1
    
P_max= P_nonre.max()

# naming the axes and graoh title
# plt.xlabel('time (s)') 
# plt.ylabel('power (kW)') 
# plt.title('Power profile of whole journey')

# plt.plot(cd[0:341], theta[0:341])




#power and forces
#from forces240322 import forcemodel
#[P, E_total, F_d, F, slope_plot]= forcemodel(v,t,tstep,d,df, W, m, w, n)



#%% regenerative braking

regen_eff= np.zeros(len(t)) #initialise regenerative efficiency
P_re= np.zeros(len(t)) #initialise regenerated energy
E_re =P_re
alpha= 0.65

#calculate regenerated efficiency to use in regenerated energy calc

i =0
while i< len(t) :
      if a_i[i]<0: #during deceleration
          regen_eff[i]= 1/((math.e)**abs(alpha/a_i[i]))  #regenerative efficiency
          P_re[i]= regen_eff[i]*P_nonre[i] # for positive P
      else:
          regen_eff[i]= 0
          P_re[i]= regen_eff[i]*P_nonre[i]
      i+=1

# E_avg = np.zeros(len(t))
# E_avg = (E_re+ E)/ d.sum() 

#want profile with part of neg captured 
#power profile, positive is nonre, negative part is re (amount of non re captured)

P= np.zeros(len(t))

i =0
while i< len(t) :
    if P_nonre[i] <0:
        P[i]=P_re[i]
    else:
        P[i]= P_nonre[i]
    i+=1
 #positive of P_nonre + P_re



#%% energy consumption(kWh)

E_nonre=P_nonre*(tstep/(60**2)) #E=P*t instantaneous energy (without regeneration)
E_re= P_re*(tstep/(60**2))
E= P*(tstep/(60**2))
# should only include positive tractive effort in both energy calcs


j=0 
while j< len(t):
    if E_nonre[j]<0:
        E_nonre[j]= 0    
    j+=1

E_total_nonre= E_nonre.sum() # total energy (without regeneration) (adds every element)


#%%cumulative

#initalise
E_cumulative_nonre= np.zeros(len(t)) 
E_cumulative_re= np.zeros(len(t))
P_cumulative = np.zeros(len(t))
E_t= np.zeros(len(t))

j=0
while j< len(t):
    E_cumulative_nonre[j]=E_nonre[0:j].sum() #energy profile over time
    E_cumulative_re[j]=E_re[0:j].sum() 
    P_cumulative[j]= P[0:j].sum()
    E_t[j]= E[0:j].sum()
    j+=1
E_cumulative= E_cumulative_nonre + E_cumulative_re

E_total_re= E_cumulative[-1] # total energy (with regeneration)

#%% plots
figure_3= plt.figure(3)
plt.subplot(311)
plt.ylabel('Velocity (m/s)') 
plt.plot (t, v) #[0:len(theta)] #ft_2

plt.subplot(312)
plt.ylabel('Power (kW)') 
plt.plot (t, P) #, P_re)

plt.subplot(313)
plt.plot (t, E_cumulative, E_cumulative_nonre ) #P_cumulative) 
plt.legend(['with regeneration', 'without'])
plt.ylabel('Energy (kWh)') 
plt.xlabel('time (s)') 

#plt.plot(t,E_re)

# #%%
figure_1= plt.figure(1)
plt.ylabel('Velocity (m/s)') 
plt.xlabel('time (s)') 
plt.plot (t, v) #[0:len(theta)] #ft_2

figure_2= plt.figure(2)
plt.ylabel('Slope (%)') 
plt.xlabel('distance (m)') 
plt.plot(cd,theta)

#%% area under graph

N = 1000000 #number of steps
#initialise linearly interpolated 
X= np.zeros(N)

# lower & upper limits of the integral
lb = 0
ub = len(t) -1

# step size
h = (ub - lb) / N

#R=

# Simpson's rule
s = P[lb] + P[ub]
for i in range(1, N):
    x2 = lb + i * h
    #nearest whole number x is close to (bigger than x)
    #nearest whole number x is close to (smaller than x)
    x1= int(math.floor(x2))#lb of x, a key in P
    x3= int(math.ceil(x2))#ub of x, a key in P
    y1=P[x1]
    y3=P[x3]
    
    X[i]= y1+ ((x2-x1)*(y3-y1))/(x3-x1) #linearly interpolate
    
    if i % 2 == 1: #division gives remainder 1 (odd)
        s += 4.0 * X[i]
    else:
        s += 2.0 * X[i]
        
Area= h/3 * s
Area= Area/3600

#plt.plot( list(range(1,N+1)), X )
#plt.plot(t,P)
#%%

print('energy req =' + str(E_total_re))
print('energy (non-re) req =' + str(E_total_nonre))

#%%
# Sum the values for Simpson's integration
# s = f(m, x, lb) + f(m, x, ub)
# for i in range(1, N):
#     t = lb + i * h
#     if i % 2 == 1:
#         s += 4.0 * f(m, x, t)
#     else:
#         s += 2.0 * f(m, x, t)


