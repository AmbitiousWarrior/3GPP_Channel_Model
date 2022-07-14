#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   LOS_probability.py
@Time    :   2022/06/13
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math
import cmath


c = 3.0*100000000 # speed of the llght

#LOS probability (distance is in meters)
def Pr_LOS_RMa(d_2D_out):

    if d_2D_out <= 10:
        Pr_LOS = 1
    if 10 < d_2D_out:
        Pr_LOS = np.exp(-(d_2D_out-10)/1000)
    return Pr_LOS
 
 
def Pr_LOS_UMi(d_2D_out): # d_2D_out,d_2D,f_c,h_BS = 25,h_UT = 1.5,h = 5,W = 20

    if d_2D_out <= 18:
        Pr_LOS = 1
    if 10 < d_2D_out:
        Pr_LOS = 18/d_2D_out + np.exp(-d_2D_out/36)*(1-18/d_2D_out )
    return Pr_LOS


def Pr_LOS_UMa(d_2D_out,h_UT = 1.5):
    
    C_h_UT = 0
    if h_UT <= 13:
        C_h_UT = 0
    if 13 < h_UT and h_UT <= 23:
        C_h_UT = math.pow((h_UT-13)/100,1.5)

    if d_2D_out <= 18:
        Pr_LOS = 1
    if 10 < d_2D_out:
        Pr_LOS = (18/d_2D_out + np.exp(-d_2D_out/63)*(1-18/d_2D_out))*(1 + 1.25*C_h_UT*math.pow(d_2D_out/100,3)*np.exp(-d_2D_out/150))
    return Pr_LOS


def Pr_LOS_Indoor_Mixed_office(d_2D_in):

    if d_2D_in <= 1.2:
        Pr_LOS = 1
    if 1.2 < d_2D_in and d_2D_in < 6.5:
        Pr_LOS = np.exp(1.2 - d_2D_in/4.7)
    if 6.5 <= d_2D_in:
        Pr_LOS = np.exp(6.5 - d_2D_in/32.6)*0.32
    return Pr_LOS


def Pr_LOS_Indoor_Open_office(d_2D_in):

    if d_2D_in <= 5:
        Pr_LOS = 1
    if 5 < d_2D_in and d_2D_in < 49:
        Pr_LOS = np.exp(5 - d_2D_in/70.8)
    if 49 <= d_2D_in:
        Pr_LOS = np.exp(49 - d_2D_in/211.7)*0.54
    return Pr_LOS

def Pr_LOS_InF(d_2D,status,d_clutter,r,h_BS,h_UT,h_c): # lazy guy

    if status == 'SL' or status == 'DL':
        k_subsce = -d_clutter/math.log(1 - r)
    if status == 'SH' or status == 'DH':
        k_subsce = -d_clutter/math.log(1 - r)*((h_BS - h_UT)/(h_c - h_UT))

    Pr_LOS = np.exp(-d_2D/k_subsce)
    return Pr_LOS



#Note:	The LOS probability is derived with assuming antenna heights of 3m for indoor, 10m for UMi, and 25m for UMa
    
    

if __name__=='__main__':
    pass