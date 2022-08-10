#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ChannelModel_UMi.py  (street canyon)
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
def Pass_Loss_UMi_LOS_and_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20):# h = avg. building height 1.5m<h_UT<22.5m  
    PL_UMi_LOS = 0.0
    PL_UMi_NLOS = 0.0
    h_E = 1.0 #UMi
    g_d2D = 0
    if g_d2D <= 18:
        g_d2D = 0
    if g_d2D <= d_2D:
        g_d2D = 1.25*math.pow((d_2D/100),3)*np.exp(-d_2D/150)
    
    if h_UT < 13:
        C_d2d_and_hUT = 0
    if 13<=h_UT and h_UT<=23:
        C_d2d_and_hUT = math.pow(((h_UT-13)/10),1.5)*g_d2D
        
    probability = 1/(1 + C_d2d_and_hUT)  #TODO need to verify this
    p =  np.random.uniform() # np.random.uniform(0,1) 0-1之间按照均匀分布采样： 0-1 之间的小数
    if p < probability:
        h_E = 1.0 
    else: # a discrete uniform distribution uniform(12,15,…,(hUT-1.5)) ???????????????
        h_E = h_UT - 1.5 
    h_BS_2 = h_BS - h_E
    h_UT_2 = h_UT - h_E
    d_BP_2 = 2*math.pi*h_BS_2*h_UT_2*f_c*c
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    PL_1 = 32.4 + 21*math.log10(d_3D) + 20*math.log10(f_c) 
    PL_2 = 32.4 + 40*math.log10(d_3D) + 20*math.log10(f_c) - 9.5*math.log10(math.pow(d_BP_2,2) + math.pow((h_BS - h_UT),2))
    
    if  10 < d_2D and d_2D <= d_BP_2:
        PL_UMi_LOS = PL_1 + 4
    
    if  d_BP_2 < d_2D and d_2D <= 5*1000:
        PL_UMi_LOS = PL_2 + 4
    
    
    PL_UMi_NLOS_2 = 22.4 + 35.3*math.log10(d_3D) + 21.3*math.log10(f_c) - 0.3*(h_UT - 1.5)
    if 10 < d_2D and d_2D <= 5*1000:
        PL_UMi_NLOS = max(PL_UMi_LOS, PL_UMi_NLOS_2) + 7.82
        
    return PL_UMi_LOS , PL_UMi_NLOS

#Break point distance dBP = 2π hBS hUT fc/c, where fc is the centre frequency in Hz, c = 3.0  108 m/s is the propagation velocity in free space, and hBS and hUT are the antenna heights at the BS and the UT, respectively.

#Optional 
def Pass_Loss_UMi_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20):
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    PL_UMi = 32.4+ 20*math.log10(f_c) + 31.9*math.log10(d_3D) 
    return PL_UMi + 8.2
    
    

if __name__=='__main__':
    pass