#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Correlation_modelling_for_multi-frequency_simulations.py  多频率状态
@Time    :   2022/06/27
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math


c = 3.0*100000000 # speed of the llght

N = 12
M = 20

μ_DS_UMi_LOS = -0.24*math.log10(1+ f_c) - 7.14
sigma_DS_UMi_LOS = 0.38 
DS = math.pow(10, np.random.normal(μ_DS_UMi_LOS, sigma_DS_UMi_LOS, 1))  #UMi_LOS, 由f_c决定 μ 与 sigma 的取值
ASD = math.pow(10, np.random.normal(μ_ASD_UMi_LOS, sigma_ASD_UMi_LOS, 1))
ASA = math.pow(10, np.random.normal(μ_ASA_UMi_LOS, sigma_ASA_UMi_LOS, 1))
ZSD = math.pow(10, np.random.normal(μ_ZSD_UMi_LOS, sigma_ZSD_UMi_LOS, 1) +ZOD_UMi_LOS_offset)
ZSA = math.pow(10, np.random.normal(μ_ZSA_UMi_LOS, sigma_ZSA_UMi_LOS, 1))

#7.6.5.1 Alternative channel generation method

#r is a proportionality factor, r=1.5.

r_proportionality_factor = 1.5

#Step 5': Generate nominal delays and angles
τ_n_2 = []
φ_AOD_n_2 = []
φ_AOA_n_2 = []
θ_ZOD_n_2 = []
θ_ZOD_n_2 = []

for i in range(N):
    X_n = np.random.uniform(0,1)
    Y_n = np.random.normal(0,1)
    Z_n = np.random.normal(0,1)
    V_n = np.random.uniform(0,1)
    W_n = np.random.uniform(0,1)

    τ_n_2.append(-r_proportionality_factor*DS_0*math.log(X_n))   # an anchor frequency, e.g. 2 GHz    DS_0、ASD_0等为在频率为2GHz时的值

    f_Y_n=np.exp((complex(0,0-r_proportionality_factor*ASD_0*Y_n)))
    # np.real(f) #实部  # np.imag(f) #虚部  z = r*(cosθ + i sinθ)
    φ_AOD_n_2.append(math.atan(np.imag(f_Y_n)/np.real(f_Y_n))*180/math.pi)   #(-180,180)  python math.atan(x) 返回 x 的反正切值，以弧度为单位，结果范围在 -pi/2 到 pi/2 之间

    f_Z_n=np.exp((complex(0,0-r_proportionality_factor*ASA_0*Z_n)))
    φ_AOA_n_2.append(math.atan(np.imag(f_Z_n)/np.real(f_Z_n))*180/math.pi)

    f_V_n=np.exp((complex(0,0-r_proportionality_factor*ZSD_0*np.sign(V_n-0.5)*math.log(1-2*abs(V_n-0.5))/math.sqrt(2))))
    θ_ZOD_n_2.append(math.atan(np.imag(f_V_n)/np.real(f_V_n))*180/math.pi)

    f_W_n=np.exp((complex(0,0-r_proportionality_factor*ZSA_0*np.sign(W_n-0.5)*math.log(1-2*abs(W_n-0.5))/math.sqrt(2))))
    θ_ZOD_n_2.append(math.atan(np.imag(f_W_n)/np.real(f_W_n))*180/math.pi)


#In case of LOS
τ_n_2[0] = 0
φ_AOD_n_2[0] = 0
φ_AOA_n_2[0] = 0
θ_ZOD_n_2[0] = 0
θ_ZOD_n_2[0] = 0

#Step 6': Generate cluster powers P_n .
P_n_2 = []
P_n = []
g_DS = max(r_proportionality_factor*DS_0 - DS,0)/(DS*r_proportionality_factor*DS_0)
g_ASD =math.sqrt(max(math.pow(r_proportionality_factor*ASD_0,2) -math.pow(ASD,2) ,0))/(ASD*r_proportionality_factor*ASD_0)
g_ASA =math.sqrt(max(math.pow(r_proportionality_factor*ASA_0,2) -math.pow(ASA,2) ,0))/(ASA*r_proportionality_factor*ASA_0)
g_ZSD = max(r_proportionality_factor*ZSD_0 - ZSD,0)/(ZSD*r_proportionality_factor*ZSD_0)
g_ZSA = max(r_proportionality_factor*ZSA_0 - ZSA,0)/(ZSA*r_proportionality_factor*ZSA_0)

for i in range(N):
    Q_n = np.random.normal(0,ζ*ζ)
    P_n_2.append(np.exp(-τ_n_2[i]*g_DS - math.pow(φ_AOD_n_2[i]*g_ASD,2)/2 - math.pow(φ_AOA_n_2[i]*g_ASA,2)/2 - math.pow(2,0.5)*abs(θ_ZOD_n_2[i])*g_ZSD - math.pow(2,0.5)*abs(θ_ZOA_n_2[i])*g_ZSA) * math.pow(10, -Q_n/10)) 

sum_P_n_2 = sum(P_n_2)
for i in range(N):
    P_n.append(P_n_2[i]/sum_P_n_2)


#  in the case of LOS, so that
for i in range(N):
    if i==0 :
        P_n.append((1/(1+K_R))*P_n_2[i]/sum_P_n_2 + K_R/(1+K_R))
    else:        
        P_n.append((1/(1+K_R))*P_n_2[i]/sum_P_n_2)



#Step 7': Generate delays and angles
τ_n = []
φ_AOA_n_m = []
φ_AOD_n_m = []
θ_ZOA_n_m = []
θ_ZOD_n_m = []
#NLOS
τ_n = τ_n_2
for i in range(N):
    for i in range(M):
        φ_AOA_n_m.append(φ_AOA_n + φ_LOS_AOA + c_ASA*alpha_m)  #a_m
        φ_AOD_n_m.append(φ_AOD_n + φ_LOS_AOD + c_ASD*alpha_m)
        θ_ZOA_n_m.append(φ_ZOA_n + φ_LOS_ZOA + c_ZSA*alpha_m)
        θ_ZOD_n_m.append(φ_ZOD_n + φ_LOS_ZOD + c_ZOD*alpha_m)


#LOS
τ_n = [i * math.sqrt(1 + K_R/2) for i in τ_n_2]  
for i in range(N):
    for i in range(M):
        φ_AOA_n_m.append(math.sqrt(1 + K_R)*φ_AOA_n + φ_LOS_AOA + c_ASA*alpha_m)  #a_m
        φ_AOD_n_m.append(math.sqrt(1 + K_R)*φ_AOD_n + φ_LOS_AOD + c_ASD*alpha_m)
        θ_ZOA_n_m.append(math.sqrt(1 + K_R)*φ_ZOA_n + φ_LOS_ZOA + c_ZSA*alpha_m)
        θ_ZOD_n_m.append(math.sqrt(1 + K_R)*φ_ZOD_n + φ_LOS_ZOD + c_ZSD*alpha_m)




if __name__=='__main__':
    pass