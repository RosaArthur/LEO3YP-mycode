# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 17:24:45 2022

@author: Poca
"""
#import libraries
import numpy as np
import math
import matplotlib.pyplot as plt

#constants
g=9.81

#inputs

#train data
#track data
d_0=10*1000


#speed and acceleration inputs
a=0.8

s_avg= 80 #(km/hr) - input, assumption
s_avg= s_avg*1000*(1/60**2) #m/s



#time model
t_station= 5*60 # t station as a return of time model


#velocity profile
tstep=1 #define remaining inputs
from velocity_profile import v_profile

v_profile(a,t_station, s_avg, tstep, d_0)

#force model

#energy calc