#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ChannelModel_InF.py  (Office)
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
def Pass_Loss_InF_LOS_and_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20):#  1m<d_3D<600m  
    PL_InF_LOS = 0.0
    PL_InF_NLOS_SL = 0.0
    PL_InF_NLOS_DL = 0.0
    PL_InF_NLOS_SH = 0.0
    PL_InF_NLOS_DH = 0.0
    
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    PL_InF_LOS = 31.84 + 21.5*math.log10(d_3D) + 19*math.log10(f_c) + 4 
       
    PL_InF_NLOS_SL = 33 + 25.5*math.log10(d_3D) + 20*math.log10(f_c)
    PL_InF_NLOS_SL = max(PL_InF_LOS, PL_InF_NLOS_SL) + 5.7
    
    PL_InF_NLOS_DL = 18.6 + 35.7*math.log10(d_3D) + 20*math.log10(f_c)
    PL_InF_NLOS_DL = max(PL_InF_LOS, PL_InF_NLOS_DL,PL_InF_NLOS_SL) + 7.2 
    
    PL_InF_NLOS_SH = 32.4 + 23*math.log10(d_3D) + 20*math.log10(f_c)
    PL_InF_NLOS_SH = max(PL_InF_LOS, PL_InF_NLOS_SH) + 5.9 
    
    PL_InF_NLOS_DH = 33.63 + 21.9*math.log10(d_3D) + 20*math.log10(f_c)
    PL_InF_NLOS_DH = max(PL_InF_LOS, PL_InF_NLOS_DH) + 4.0
    
        
    return PL_InF_LOS , PL_InF_NLOS_SL , PL_InF_NLOS_DL , PL_InF_NLOS_SH , PL_InF_NLOS_DH

 

if __name__=='__main__':
    pass