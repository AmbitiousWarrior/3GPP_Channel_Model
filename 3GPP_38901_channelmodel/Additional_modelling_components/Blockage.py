#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Blockage.py  空间一致性
@Time    :   2022/06/26
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math


c = 3.0*100000000 # speed of the llght

N = 12
τ_n_2 = []
τ_n = []
P_n = []
θ_n_AOA_2 = []
θ_n_AOD_2 = []
θ_n_ZOA_2 = []
θ_n_ZOD_2 = []

P_n_2 = []
Z_n = []

K_R = 1 #TODO my default value = 1

# Procedure B
    
μ_DS_UMi_LOS = -0.24*math.log10(1+ f_c) - 7.14  # 考虑把所有表格数据变成全局变量！！！！！！！！！
sigma_DS_UMi_LOS = 0.38 
μ_ASA_UMi_LOS = -0.08*math.log10(1+ f_c) + 1.73
sigma_ASA_UMi_LOS = 0.014*math.log10(1+ f_c) + 0.28 

μ_ZSA_UMi_LOS = -0.1*math.log10(1+ f_c) + 0.73
sigma_ZSA_UMi_LOS = -0.04*math.log10(1+ f_c) + 0.34

μ_ASD_UMi_LOS = -0.05*math.log10(1+ f_c) + 1.21
sigma_ASD_UMi_LOS = 0.41 

μ_ZSD_UMi_LOS = max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83)
sigma_ZSD_UMi_LOS = 0.35

ζ_UMi_LOS = 3

DS = 0.000   #用0.000作为个人的未知默认值或为引用的全局值
ASA = 0.000
ASD = 0.000
ZSA = 0.000
ZSD = 0.000

for i in range(N): # The autocorrelation distance for  τ_n_2 is  2*c*math.pow(10,μ_DS_UMi_LOS + sigma_DS_UMi_LOS)
    τ_n_2.append(np.random.uniform(0, 2*math.pow(10,μ_DS_UMi_LOS + sigma_DS_UMi_LOS)))        
    #In the case of LOS, set the delay of the first cluster τ_1 to 0
for i in range(N):
    τ_n.append(τ_n_2[i] - min(τ_n_2)) 
    
for i in range(N):
    θ_n_AOA_2.append(2*math.pow(10,μ_ASA_UMi_LOS + sigma_ASA_UMi_LOS) * np.random.uniform(-1, 1))    
    θ_n_AOD_2.append(2*math.pow(10,μ_ASD_UMi_LOS + sigma_ASD_UMi_LOS) * np.random.uniform(-1, 1))
    θ_n_ZOA_2.append(2*math.pow(10,μ_ZSA_UMi_LOS + sigma_ZSA_UMi_LOS) * np.random.uniform(-1, 1))
    θ_n_ZOD_2.append(2*math.pow(10,μ_ZSD_UMi_LOS + sigma_ZSD_UMi_LOS) * np.random.uniform(-1, 1))
    Z_n.appe(np.random.normal(0, math.pow(2,ζ_UMi_LOS), 1))
    
for i in range(N):
    P_n_2.append(math.exp(-τ_n_2[i]/DS)*math.exp(-math.pow(2,0.5)*abs(θ_n_AOA_2[i])/ASA)*math.exp(-math.pow(2,0.5)*abs(θ_n_AOD_2[i])/ASD)*math.exp(-math.pow(2,0.5)*abs(θ_n_ZOA_2[i])/ZSA)*math.exp(-math.pow(2,0.5)*abs(θ_n_ZOD_2[i])/ZSD))*math.pow(10,-Z_n[i]/10)
sum_P_n_2 = sum(P_n_2)
for i in range(N):
    P_n.append(P_n_2/sum_P_n_2)

#In the case of LOS condition  
DS = DS * math.sqrt(1 + K_R/2)
ASA = ASA * math.sqrt(1 + K_R)
ASD = ASD * math.sqrt(1 + K_R)
ZSA = ZSA * math.sqrt(1 + K_R)
ZSD = ZSD * math.sqrt(1 + K_R)
for i in range(N):
    P_n_2.append(math.exp(-τ_n_2[i]/DS)*math.exp(-math.pow(2,0.5)*abs(θ_n_AOA_2[i])/ASA)*math.exp(-math.pow(2,0.5)*abs(θ_n_AOD_2[i])/ASD)*math.exp(-math.pow(2,0.5)*abs(θ_n_ZOA_2[i])/ZSA)*math.exp(-math.pow(2,0.5)*abs(θ_n_ZOD_2[i])/ZSD))*math.pow(10,-Z_n[i]/10)
    
P_n_2_to_N = []
for i in range(N): 
    P_1_LOS = K_R/(K_R + 1)   
    if i>0: 
        P_n_2_to_N.append(1/(K_R + 1)*P_n[i]/sum(P_n[1,N]) ) 
            
#Apply offset angles
φ_n_m_AOA = φ_n_AOA_2 + φ_LOS_AOA + c_ASA*a_m
φ_n_m_AOD = φ_n_AOD_2 + φ_LOS_AOD + c_ASD*a_m
    
if O2I ==True:
    avg_φ_ZOA = 90
else:
    avg_φ_ZOA = φ_LOS_ZOA
φ_n_m_ZOA = φ_n_ZOA_2 + avg_φ_ZOA + c_ZSA*a_m


μ_lg_ZSD = max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83)
c_ZSD = 3/8*math.pow(10,μ_lg_ZSD)
φ_n_m_ZOD = φ_n_ZOD_2 + φ_LOS_ZOD + c_ZSD*a_m + ZOD_UMi_LOS_offset
    
    
    
#7.6.3.3	LOS/NLOS, indoor states and O2I parameters
G = np.random.normal(loc=0.0, scale=1.0, size=None) # loc:均值 scale:标准差   需要确定这里的标准差

Pr_LOS_d = 0.0 #the distance dependent LOS probability function

F_d = math.sqrt(2)*1/math.erf(2*Pr_LOS_d-1)

LOS_soft =  0.5 + 1/math.pi * math.atan(math.sqrt(20/lambda_)* G * F_d)

# 7.6.3.4	Applicability of spatial consistency


if __name__=='__main__':
    pass