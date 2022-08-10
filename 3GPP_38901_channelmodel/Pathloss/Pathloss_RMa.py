#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ChannelModel_RMa.py
@Time    :   2022/06/12
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math
import cmath


c = 3.0*100000000 # speed of the llght

#Pathloss [dB], fc is in GHz and d is in meters
def Pass_Loss_RMa_LOS_and_NLOS(d_2D,f_c,h_BS = 35,h_UT = 1.5,h = 5,W = 20):# h = avg. building height 5m<h<50m  W = avg. street width   5m<W<50m 
    PL_RMa_LOS = 0.0
    PL_RMa_NLOS = 0.0
    d_BP = 2*math.pi*h_BS*h_UT*f_c*c
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    PL_1 = 20*math.log10(40*math.pi*d_3D*f_c/3) +  min(0.03*math.pow(h, 1.72) , 10)*math.log10(d_3D) - min(0.044*math.pow(h, 1.72) , 14.77) + 0.002*math.log10(h) *d_3D
    PL_2 = PL_1 + 40*math.log10(d_3D/d_BP)
    
    if  10 < d_2D and d_2D <= d_BP:
        PL_RMa_LOS = PL_1 + 4 #阴影衰落
    
    if  d_BP < d_2D and d_2D <= 10*1000:
        PL_RMa_LOS = PL_2 + 6
    
    
    PL_RMa_NLOS_2 = 161.04 - 7.1*math.log10(40*W) + 7.5*math.log10(h) -(24.37 - 3.7*(h/h_BS)*(h/h_BS))*math.log10(h_BS) + (43.42 - 3.1 * math.log10(h_BS))*(math.log10(d_3D)-3) + 20*math.log10(f_c) - (3.2*math.pow(math.log10(11.75*h_UT), 2) - 4.97)
    if 10 < d_2D and d_2D <= 5*1000:
        PL_RMa_NLOS = max(PL_RMa_LOS, PL_RMa_NLOS_2) + 8
        
    return PL_RMa_LOS , PL_RMa_NLOS

#Break point distance dBP = 2π hBS hUT fc/c, where fc is the centre frequency in Hz, c = 3.0  108 m/s is the propagation velocity in free space, and hBS and hUT are the antenna heights at the BS and the UT, respectively.



if __name__=='__main__':
    pass