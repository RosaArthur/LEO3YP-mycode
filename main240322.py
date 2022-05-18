# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:53:06 2022

@author: Poca
"""
import pandas as pd

#track data(google earth)
#import track data
df = pd.read_excel("elevationdata.xlsx")  
df= pd.DataFrame(df, columns= ['distance', 'slope'])
  

#train data
Ndoors= 2 #doors per car
capacity=150 #capacity of train
N_cars= 3

W=92 #mass of train (tons)
m= W*1000 #mass of train (kg) ** tons to tonnes to kg
w=16 #weight per axle (tons) 
n=4 #number of axles per car
#*mass will decrease with journey

tstep=1 #for v and force profile

#velocity profile over whole journey
from compile240322 import compilevt
[v,t,cd_0, cd, d]= compilevt(Ndoors, capacity, N_cars, W, m, w, tstep)

#%%

import numpy as np
import math
import matplotlib.pyplot as plt

#inputs as speeds, mass, gradient(alpha)
#output as instantaneous resultant force

g=9.81

# from compile240322 import compilevt
# [v,t]= compilevt() #v is in m/s
V= v*(3600/1000) #instantaenous speed in km/h)

#from tractiveforce250322 import tractiveforce
#[c]= tractiveforce(v,V, t,tstep,d,cd, cd_0, df, W, m, w, n)

#power and forces
from forces250322 import forcemodel
[P, E_total, F_d, F, b]= forcemodel(v,t,tstep,d,cd, cd_0, df, W, m, w, n)
