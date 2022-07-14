#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Oxygen_absorption.py
@Time    :   2022/06/20
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math


c = 3.0*100000000 # speed of the llght

alpha_f = {
    '0-52':0.0,
    '53':1,
    '54':2.2,
    '55':4,
    '56':6.6,
    '57':9.7,
    '58':12.6,
    '59':14.6,
    '60':15,
    '61':14.6,
    '62':14.3,
    '63':10.5,
    '64':6.8,
    '65':3.9,
    '66':1.9,
    '67':1.0,
    '68-100':0.0 
}

#TODO 线性差值函数 done

def Oxygen_absorption(d_2D,fc,τ_n,h_BS = 10,h_UT = 1.5,is_LOS = True,is_large_bandwidth = False, delta_f = 0):# τ_n 可由 τ_n_UMi_LOS 获得

    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))

    if is_LOS ==True:
        τ_t_2 = 0
    else:
        τ_t_2 = min(τ_n)
        
    if fc <= 52:
        alpha_fc = alpha_f['0-52']
    elif fc >= 68:
        alpha_fc = alpha_f['68-100']
    else:
        if is_large_bandwidth != False: 
            fc = fc + delta_f
        fractional_part = math.modf(fc) 
        alpha_fc = alpha_f[str(int(fc))] + fractional_part[0]*(alpha_f[str(int(fc+1))]-alpha_f[str(int(fc))])
    
    if is_large_bandwidth ==False:    
        OL_n_fc = alpha_fc/1000*(d_3D + c*(τ_n + τ_t_2))
        return OL_n_fc
    else: # For large channel bandwidth  The oxygen loss, OLn(fc+ Δf) for cluster n at frequency fc+ Δf     Δf is in [-B/2, B/2]   
        OL_n_fc_plus_delta_f = alpha_fc/1000*(d_3D + c*(τ_n + τ_t_2))                      
        return OL_n_fc_plus_delta_f
    
    
    

if __name__=='__main__':
    pass