#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ChannelModel_InH.py  (Office)
@Time    :   2022/06/13
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math
import cmath


c = 3.0*100000000 # speed of the llght

#Pathloss [dB], fc is in GHz and d is in meters
def Pass_Loss_InH_LOS_and_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20):#  1m<d_3D<150m  
    PL_InH_LOS = 0.0
    PL_InH_NLOS = 0.0
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    PL_InH_LOS = 32.4 + 17.3*math.log10(d_3D) + 20*math.log10(f_c) + 3
       
    PL_InH_NLOS_2 = 17.30 + 38.3*math.log10(d_3D) + 24.9*math.log10(f_c)
    PL_InH_NLOS = max(PL_InH_LOS, PL_InH_NLOS_2) + 8.03
        
    return PL_InH_LOS , PL_InH_NLOS


#Optional 
def PL_InH_NLOS_2(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20):
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    PL_InH_NLOS_2 = 32.4+ 20*math.log10(f_c) + 31.9*math.log10(d_3D) + 8.29
    return PL_InH_NLOS_2
    
    

if __name__=='__main__':
    pass