#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Large_bandwidth_and_large_antenna_array.py
@Time    :   2022/06/21
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math



c = 3.0*100000000 # speed of the llght

N = 12      # Number of clusters
M = 20      # Number of rays per cluster 
B = 100*1000     # Hz
#UMi
c_DS = 5 
c_ASA = 3
c_ASD = 17
c_ZSA = 7
μ_lg_ZSD = max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83)
c_ZSD = 3/8*math.pow(10,μ_lg_ZSD)

M_t = 4* 0.5 * c_DS * B
# D_h and  D_v are the array size in m in horizontal and vertical dimension, B is bandwidth in Hz, lambda_ is the wavelength
M_AOD = 4* 0.5 * c_ASD * math.pi * D_h/180/lambda_ 
M_ZOD = 4* 0.5 * c_ZSD * math.pi * D_v/180/lambda_
M_max = 20 #  M_max is the upper limit of  , and it should be selected by the user of channel model based on the trade-off between simulation complexity and accuracy.
M = min(max(M_t*M_AOD*M_ZOD,20),M_max)   #***式7.6-3中的key值，可用于修改（拓展）Fast_fading_model的H_u_s_n_NLOS

P_n_m_2 = []
τ_n_m_2_2 = []


for i in range(N):
    for j in range(M):        
        τ_n_m_2_2.append(math.random.uniform(0, 2*c_DS)) 

for i in range(N):
    min_τ_n_m_2_2 = min(τ_n_m_2_2)
    for j in range(M):
        τ_n_m_2 = τ_n_m_2_2[i*M+j] - min_τ_n_m_2_2
        τ_n_m = τ_n + τ_n_m_2  #***式7.6-3中的key值，可用于修改（拓展）Fast_fading_model的H_u_s_n_NLOS
        P_n_m_2.append(math.exp(-τ_n_m_2/c_DS)*math.exp(-math.pow(2,0.5)*abs(alpha_n_m_AOA)/c_ASA)*math.exp(-math.pow(2,0.5)*abs(alpha_n_m_AOD)/c_ASD)*math.exp(-math.pow(2,0.5)*abs(alpha_n_m_ZOA)/c_ZSA)*math.exp(-math.pow(2,0.5)*abs(alpha_n_m_ZOD)/c_ZSD))
        
       

for i in range(N):
    sum_P_n_m_2 = sum(P_n_m_2[i*N,i*N + M])
    for j in range(M):        
        P_n_m = P_n*P_n_m_2[i*M+j]/sum_P_n_m_2  #***式7.6-3中的key值，可用于修改（拓展）Fast_fading_model的H_u_s_n_NLOS

    
    
    

if __name__=='__main__':
    pass