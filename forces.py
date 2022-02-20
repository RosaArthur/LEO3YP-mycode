# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 17:36:04 2022

@author: Poca
"""

#force model

#inputs as speeds, mass, gradient(alpha)
#output as instantaneous resultant force

#V= # (instantaenous speed in km/h)

A=9.4/(math.sqrt(w)) + 12.5/w
B=8*10**-5*W*V
C=6*10**-7*W*V**2


#F_t
F_d=A+B*v+C*v**2 #running resistance in kg/ton
F_d= F_d*W*g #running resistance in N
#f= m*g*slope+A/R_L #slope resistance and curve resistance