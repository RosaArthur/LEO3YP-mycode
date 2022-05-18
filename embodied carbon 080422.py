# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:03:38 2022

@author: Poca
"""

#embodied carbon
import numpy as np
import matplotlib.pyplot as plt

d=np.array([10.003, 7.725, 5.021, 7.201]) # d in km
years= 30
Nsignal= 6 #sets of signalling
#values 
#properties of track
new_track_length = d[0]+d[1]+d[2]
track_length= d.sum() #track length in km 

#%%
#construction
embodiedcarbon= (941+168)*new_track_length #tCO2

#operation

#%% a different study

embodiedcarbon_2=50*new_track_length*years

#%%

#another study
Ncars=3
Ntrains=8
i=new_track_length*Ncars*Ntrains
l_shortbridge= 0.005*new_track_length
l_s_avgtunnel= 0.005*new_track_length

carbon= np.zeros(8)

#carbonmaintenance
carbon[0]= (14.4+6.81)*i
#rolling stock
carbon[1]=(93.9+0.662)*Ncars*Ntrains #ton co2 #manufacture #aluminium bodu
#turnouts
carbon[3]= 8.99*10 #everytime single to double or vice versa, at least 2 near every station

#structure
#carbonballast
carbon[2]= 0.356*new_track_length*10**3 #ballasted track
#carbonsignal 
carbon[4]= 1.52*Nsignal
#carbonbridge
carbon[5]= 3.75*l_shortbridge #prestressed bridge
#carbontunnel 
carbon[6]= 16.1*l_s_avgtunnel

#earthworks
carbon[7]= (3.29*1000) +(6.02*1000) #1km embankment and 1km cut

carbonstructure= carbon.sum()

#%%

#carbon emissions
labels2 = 'Rail Maintenance', 'Rolling stock Maintenance and Disposal', 'Structure- Slab', 'Structure - Signal & Turnout', 'Structure- Bridge, Tunnel & Earthworks'

carbon2 = np.zeros(5)
carbon2[0]= carbon[0]
carbon2[1]= carbon[1]
carbon2[2]= carbon[2]
carbon2[3]= carbon[3] + carbon[4]
carbon2 [4]= carbon [5] + carbon[6] +carbon[7]

# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(carbon2, autopct='%1.1f%%',  pctdistance=1.13, startangle=180, textprops={'fontsize':14})
plt.legend(labels2,loc=2)
plt.title('Embodied carbon')

# show plot
plt.show()
