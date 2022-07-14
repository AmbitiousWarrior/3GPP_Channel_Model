#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Fast_fading_model.py
@Time    :   2022/06/16
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import random
from re import L
import numpy as np
import math
from sympy import DiracDelta

# step1 Set environment, network layout, and antenna array parameters 设置环境、网络布局和天线阵列参数
c = 3.0*100000000 # speed of the llght
d_2D = 0.0
h_UT = 1.5
h_BS = 50
θ = 0.0     #zenith angle 
θ_LOS_ZOD = 0.0
θ_LOS_ZOA = 0.0

φ = 0.0     #azimuth angle
φ_LOS_AOD = 0.0
φ_LOS_AOA = 0.0

F_rx = 0.0  #BS antenna field patterns 
F_tx = 0.0  #UT antenna field patterns

Ω_BS_a = 0.0    #BS bearing angle
Ω_BS_b = 0.0    #BS downtilt angle
Ω_BS_c = 0.0    #BS slant angle

Ω_UT_a = 0.0    #UT bearing angle   方位角
Ω_UT_b = 0.0    #UT downtilt angle  下倾角
Ω_UT_c = 0.0    #UT slant angle     倾斜角


f_c = 0.0    #Specify system centre frequency
B = 0.0      #bandwidth 

#step2  Assign propagation condition (LOS/NLOS)  分配传播条件

#step3  Calculate pathloss with formulas in Table 7.4.1-1 for each BS-UT link to be modelled. 计算每条链路的路径损失

#step4  Generate large scale parameters, e.g. delay spread (DS), angular spreASD (ASA, ASD, ZSA, ZSD), Ricean K factor (K) and shadow fading (SF)生成大尺度参数  # sigma： σ
#Limit random RMS azimuth arrival and azimuth departure spread values to 104 degrees, i.e., ASA= min(ASA, 104), ASD = min(ASD, 104). Limit random RMS zenith arrival and zenith departure spread values to 52 degrees, i.e., ZSA = min(ZSA, 52), ZSD = min(ZSD, 52).

#UMi
#UMi_DS 
#lg_DS_UMi_LOS 
μ_DS_UMi_LOS = -0.24*math.log10(1+ f_c) - 7.14
sigma_DS_UMi_LOS = 0.38 
lg_DS_UMi_LOS = np.random.normal(μ_DS_UMi_LOS, sigma_DS_UMi_LOS, 1) # TODO μ_DS_UMi_LOS + sigma_DS_UMi_LOS 38901  7.6.3.2章节
#lg_DS_UMi_NLOS 
μ_DS_UMi_NLOS = -0.24*math.log10(1+ f_c) - 6.83
sigma_DS_UMi_NLOS = 0.16*math.log10(1+ f_c) + 0.28 
lg_DS_UMi_NLOS = np.random.normal(μ_DS_UMi_NLOS, sigma_DS_UMi_NLOS, 1)
#lg_DS_UMi_O2I
μ_DS_UMi_O2I = -6.62
sigma_DS_UMi_O2I = 0.32
lg_DS_UMi_O2I = np.random.normal(μ_DS_UMi_O2I, sigma_DS_UMi_O2I, 1)

#UMi_ASD
#lg_ASD_UMi_LOS 
μ_ASD_UMi_LOS = -0.05*math.log10(1+ f_c) + 1.21
sigma_ASD_UMi_LOS = 0.41 
lg_ASD_UMi_LOS = np.random.normal(μ_ASD_UMi_LOS, sigma_ASD_UMi_LOS, 1)
#lg_ASD_UMi_NLOS 
μ_ASD_UMi_NLOS = -0.23*math.log10(1+ f_c) + 1.53
sigma_ASD_UMi_NLOS = 0.11*math.log10(1+ f_c) + 0.33 
lg_ASD_UMi_NLOS = np.random.normal(μ_ASD_UMi_NLOS, sigma_ASD_UMi_NLOS, 1)
#lg_ASD_UMi_O2I
μ_ASD_UMi_O2I = 1.25
sigma_ASD_UMi_O2I = 0.42
lg_ASD_UMi_O2I = np.random.normal(μ_ASD_UMi_O2I, sigma_ASD_UMi_O2I, 1)

#UMi_ASA
#lg_ASA_UMi_LOS 
μ_ASA_UMi_LOS = -0.08*math.log10(1+ f_c) + 1.73
sigma_ASA_UMi_LOS = 0.014*math.log10(1+ f_c) + 0.28 
lg_ASA_UMi_LOS = np.random.normal(μ_ASA_UMi_LOS, sigma_ASA_UMi_LOS, 1)
#lg_ASA_UMi_NLOS 
μ_ASA_UMi_NLOS = -0.08*math.log10(1+ f_c) + 1.81
sigma_ASA_UMi_NLOS = 0.05*math.log10(1+ f_c) + 0.3
lg_ASA_UMi_NLOS = np.random.normal(μ_ASA_UMi_NLOS, sigma_ASA_UMi_NLOS, 1)
#lg_ASA_UMi_O2I
μ_ASA_UMi_O2I = 1.76
sigma_ASA_UMi_O2I = 0.16
lg_ASA_UMi_O2I = np.random.normal(μ_ASA_UMi_O2I, sigma_ASA_UMi_O2I, 1)

#UMi_ZSA
#lg_ZSA_UMi_LOS 
μ_ZSA_UMi_LOS = -0.1*math.log10(1+ f_c) + 0.73
sigma_ZSA_UMi_LOS = -0.04*math.log10(1+ f_c) + 0.34
lg_ZSA_UMi_LOS = np.random.normal(μ_ZSA_UMi_LOS, sigma_ZSA_UMi_LOS, 1)
#lg_ZSA_UMi_NLOS 
μ_ZSA_UMi_NLOS = -0.04*math.log10(1+ f_c) + 0.92
sigma_ZSA_UMi_NLOS = -0.07*math.log10(1+ f_c) + 0.41
lg_ZSA_UMi_NLOS = np.random.normal(μ_ZSA_UMi_NLOS, sigma_ZSA_UMi_NLOS, 1)
#lg_ZSA_UMi_O2I
μ_ZSA_UMi_O2I = 1.01
sigma_ZSA_UMi_O2I = 0.43
lg_ZSA_UMi_O2I = np.random.normal(μ_ZSA_UMi_O2I, sigma_ZSA_UMi_O2I, 1)

#UMi_ZSD
#lg_ZSD_UMi_LOS 
μ_ZSD_UMi_LOS = max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83)
sigma_ZSD_UMi_LOS = 0.35
ZOD_UMi_LOS_offset = 0.0
lg_ZSD_UMi_LOS = np.random.normal(μ_ZSD_UMi_LOS, sigma_ZSD_UMi_LOS, 1) +ZOD_UMi_LOS_offset
#lg_ZSD_UMi_NLOS 
μ_ZSD_UMi_NLOS = max(-0.5, -3.1*(d_2D/1000)+ 0.01*max((h_UT-h_BS),0) + 0.2)
sigma_ZSD_UMi_NLOS = 0.35
ZOD_UMi_NLOS_offset = -math.pow(10,-1.5*math.log10(max(10, d_2D))+3.3)  # TODO verify: -10^{-1.5*math.log10(max(10, d_2D))+3.3}
lg_ZSD_UMi_NLOS = np.random.normal(μ_ZSD_UMi_NLOS, sigma_ZSD_UMi_NLOS, 1)+ZOD_UMi_NLOS_offset

#UMi_XPR
#XPR_UMi_LOS
μ_XPR_UMi_LOS = 9
sigma_XPR_UMi_LOS = 3
#XPR_UMi_NLOS
μ_XPR_UMi_LOS = 8.0
sigma_XPR_UMi_LOS = 3
#XPR_UMi_O2I
μ_XPR_UMi_LOS = 9
sigma_XPR_UMi_LOS = 5

#UMi_C_ASA
C_ASA_UMi_LOS = 17
C_ASA_UMi_NLOS = 22
C_ASA_UMi_O2I = 8
#UMi_C_ASD
C_ASD_UMi_LOS = 3
C_ASD_UMi_NLOS = 10
C_ASD_UMi_O2I = 5
#UMi_C_ZSA
C_ZSA_UMi_LOS = 7
C_ZSA_UMi_NLOS = 7
C_ZSA_UMi_O2I = 3
# #UMi_C_ZSD
# μ_ZSD_UMi_NLOS = max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83)
# sigma_ZSD_UMi_NLOS = 0.35
# lg_ZSD_UMi_LOS = np.random.normal(μ_ZSD_UMi_NLOS, sigma_ZSD_UMi_NLOS, 1)+ZOD_UMi_NLOS_offset

# C_ZSD_UMi_NLOS = 7
# C_ZSD_UMi_O2I = 3

#UMi_C_DS
C_DS_UMi_LOS = 5
C_DS_UMi_NLOS = 11
C_DS_UMi_O2I = 11

#UMi_#UMi_ζ
ζ_UMi_LOS = 3
ζ_UMi_NLOS = 3
ζ_UMi_O2I = 4

#TODO  其他情况的枚举

#step5  Generate cluster delays  τ_n
N = 12      # Number of clusters
M = 20      # Number of rays per cluster 
r_τ = 0.0
N_Umi_LOS = 12
N_Umi_NLOS = 19
N_Umi_O2I = 12
K_Umi_LOS = np.random.normal(9, 5, 1)
r_τ_UMi_LOS = 3.0
r_τ_UMi_NLOS = 2.1
r_τ_UMi_O2I = 2.2

def τ_n_UMi_LOS(N_Umi_LOS,is_LOS = True): # 参数is_LOS，判断是否为LOS 场景
    τ_n_2 = []
    τ_n = []
    DS = math.pow(10,lg_DS_UMi_LOS)  #need to verify
    for i in range(N_Umi_LOS):
        X_n = random.uniform(0, 1)
        τ_n_2.append(-r_τ*DS*math.log(X_n))
    τ_n_min = min(τ_n_2)
    for i in range(N_Umi_LOS):
        τ_n = τ_n_2[i] - τ_n_min
    τ_n = np.sort(τ_n)
    if is_LOS == True:
        C_τ = 0.7705 - 0.0433*K_Umi_LOS + 0.0002*math.pow(K_Umi_LOS,2) + 0.000017*math.pow(K_Umi_LOS,3)
        return  np.divide(τ_n, C_τ)
    return τ_n
#In the case of LOS condition, additional scaling of delays is required to compensate for the effect of LOS peak addition to the delay spread. 

#step6 Generate cluster powers P_n
Per_cluster_shadowing_std_UMi_LOS = 3
Per_cluster_shadowing_std_UMi_NLOS = 3
Per_cluster_shadowing_std_UMi_O2I = 4

def P_n_UMi_LOS(N_Umi_LOS, τ_n, is_LOS = True):
    P_n_2 = []
    P_n = []
    DS = math.pow(10,lg_DS_UMi_LOS)
    Z_n = np.random.normal(0.5, 1, 1)
    for i in range(N_Umi_LOS):
        Z_n = np.random.normal(0.0, Per_cluster_shadowing_std_UMi_LOS, 1)
        P_n_2.append(math.exp(-τ_n(i)*(r_τ_UMi_LOS-1)/r_τ_UMi_LOS/DS)*math.pow(10,-Z_n/10))
    sum_P_n_2= sum(P_n_2)
    if is_LOS != True:
        for i in range(N_Umi_LOS):
            P_n.append(P_n_2[i]/sum_P_n_2)
    P1_LOS = K_Umi_LOS/(K_Umi_LOS + 1)   #K_R  need to verify
    if is_LOS == True:
        for i in range(N_Umi_LOS):
            if i != 0:  #TODO  δ(n-1)*(P1_LOS) 需要确定δ(n-1)的值  n-1不等于0时：δ(n-1)=0  n-1等于0时：δ(n-1)= +无穷 ？？？？ Solved 除了LOS 其他所有鏃功率和为1/(1+K_R)  LOS+NLOS的归一化功率和为1  仔细读协议 答案一般就在其中 nice job
                P_n.append(P_n_2[i]/sum_P_n_2/(K_Umi_LOS + 1) + 0.0*(P1_LOS))
            else:
                P_n.append(P1_LOS) #LOS分量的归一化功率 
    return P_n    
    
#In the case of LOS condition an additional specular component is added to the first cluster. 
#Assign the power of each ray within a cluster as Pn / M, where M is the number of rays per cluster.
#Remove clusters with less than -25 dB power compared to the maximum cluster power. The scaling factors need not be changed after cluster elimination.

#step7   Generate arrival angles and departure angles for both azimuth and elevation.
C_φ_NLOS_A = {
    '4':0.779,
    '5':0.860,
    '8':1.108,
    '10':1.090,
    '11':1.123,
    '12':1.146,
    '14':1.190,
    '15':1.211,
    '16':1.226,
    '19':1.273,
    '20':1.289,
    '25':1.358,
}
a_m = {
    '1':0.0447,
    '2':-0.0447,
    '3':0.01413,
    '4':-0.01413,
    '5':0.2492,
    '6':-0.2492,
    '7':0.3715,
    '8':-0.3715,
    '9':0.5129,
    '10':-0.5129,
    '11':0.6797,
    '12':-0.6797,
    '13':0.8844,
    '14':-0.8844,
    '15':1.1481,
    '16':-1.1481,
    '17':1.5195,
    '18':-1.5195,
    '19':2.1551,
    '20':-2.1551 
}
def φ_n_AOA_UMi_LOS(N, P_n, is_LOS = True): # AOD follows a procedure similar to AOA
    φ_n_2 = []
    φ_n_m = []
    ASA = math.pow(lg_ASA_UMi_LOS)
    if is_LOS == True:
        C_φ = C_φ_NLOS_A[str(N)]
    else:
        C_φ = C_φ_NLOS_A[str(N)]*(1.1035 - 0.028*K_Umi_LOS - 0.002*math.pow(K_Umi_LOS,2) + 0.0001*math.pow(K_Umi_LOS,3))
    for i in range(N):
        φ_n_2.append(2*(ASA/1.4)*math.sqrt(-math.log(P_n[i]/max(P_n)))/C_φ) 
    if is_LOS != True:    
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASA/7,2), 1)
            φ_n = X_n*φ_n_2[i] + Y_n + φ_LOS_AOA
            for j in range(M):
                φ_n_m_element = φ_n + C_ASA_UMi_LOS*a_m[str(j+1)]
                φ_n_m.append(φ_n_m_element) 
    if is_LOS == True:
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ASA/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASA/7,2), 1)
            φ_n = (X_n*φ_n_2[i] + Y_n) -(X_1*φ_n_2[0] + Y_1 - φ_LOS_AOA)
            for j in range(M):
                φ_n_m_element = φ_n + C_ASA_UMi_LOS*a_m[str(j+1)] 
                φ_n_m.append(φ_n_m_element) 
    return  φ_n_m       

def φ_n_AOD_UMi_LOS(N, P_n, is_LOS = True): # AOD follows a procedure similar to AOD
    φ_n_2 = []
    φ_n_m = []
    ASD = math.pow(lg_ASD_UMi_LOS)
    if is_LOS == True:
        C_φ = C_φ_NLOS_A[str(N)]
    else:
        C_φ = C_φ_NLOS_A[str(N)]*(1.1035 - 0.028*K_Umi_LOS - 0.002*math.pow(K_Umi_LOS,2) + 0.0001*math.pow(K_Umi_LOS,3))
    for i in range(N):
        φ_n_2.append(2*(ASD/1.4)*math.sqrt(-math.log(P_n[i]/max(P_n)))/C_φ) 
    if is_LOS != True:    
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASD/7,2), 1)
            φ_n = X_n*φ_n_2[i] + Y_n + φ_LOS_AOD
            for j in range(M):
                φ_n_m_element = φ_n + C_ASD_UMi_LOS*a_m[str(j+1)]
                φ_n_m.append(φ_n_m_element) 
    if is_LOS == True:
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ASD/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASD/7,2), 1)
            φ_n = (X_n*φ_n_2[i] + Y_n) -(X_1*φ_n_2[0] + Y_1 - φ_LOS_AOD)
            for j in range(M):
                φ_n_m_element = φ_n + C_ASD_UMi_LOS*a_m[str(j+1)] 
                φ_n_m.append(φ_n_m_element) 
    return  φ_n_m  

C_θ_NLOS_Z = {
    '8':0.889,
    '10':0.957,
    '11':1.031,
    '12':1.104,
    '15':1.1088,
    '19':1.184,
    '20':1.178,
    '25':1.282
}                        
def θ_n_ZOA_UMi_LOS(N, P_n, is_LOS = True,BS_UT_link ='O2I'):  #θ 用 θ 更合适
    θ_n_2 = []
    θ_n_m = []
    ZSA = math.pow(lg_ZSA_UMi_LOS)
    if is_LOS == True:
        C_θ = C_θ_NLOS_Z[str(N)]
    else:
        C_θ = C_θ_NLOS_Z[str(N)]*(1.3086 + 0.0339*K_Umi_LOS - 0.0077*math.pow(K_Umi_LOS,2) + 0.0002*math.pow(K_Umi_LOS,3))
    for i in range(N):
        θ_n_2.append(-ZSA*math.log(P_n[i]/max(P_n))/C_θ) 
        
    if BS_UT_link == 'O2I':
        θ_LOS_ZOA_ = 90
    else:
        θ_LOS_ZOA_ = θ_LOS_ZOA

    if is_LOS != True:    
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSA/7,2), 1)
            θ_n = X_n*θ_n_2[i] + Y_n + θ_LOS_ZOA_ 
            for j in range(M):
                θ_n_m_element = θ_n + C_ZSA_UMi_LOS*a_m[str(j+1)]
                θ_n_m.append(θ_n_m_element) 
    if is_LOS == True:
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ZSA/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSA/7,2), 1)
            θ_n = (X_n*θ_n_2[i] + Y_n) -(X_1*θ_n_2[0] + Y_1 - θ_LOS_ZOA)
            for j in range(M):
                θ_n_m_element = θ_n + C_ZSA_UMi_LOS*a_m[str(j+1)] 
                θ_n_m.append(θ_n_m_element) 
    for item in θ_n_m:
        if 180<=item and item<=360:
            item = 360 - item
    return  θ_n_m   


def θ_n_ZOD_UMi_LOS(N, P_n, is_LOS = True,BS_UT_link ='O2I'):
    θ_n_2 = []
    θ_n_m = []
    ZSD = math.pow(lg_ZSD_UMi_LOS)
    if is_LOS == True:
        C_θ = C_θ_NLOS_Z[str(N)]
    else:
        C_θ = C_θ_NLOS_Z[str(N)]*(1.3086 + 0.0339*K_Umi_LOS - 0.0077*math.pow(K_Umi_LOS,2) + 0.0002*math.pow(K_Umi_LOS,3))
    for i in range(N):
        θ_n_2.append(-ZSD*math.log(P_n[i]/max(P_n))/C_θ) 
        
    if BS_UT_link == 'O2I':
        θ_LOS_ZOD_ = 90
    else:
        θ_LOS_ZOD_ = θ_LOS_ZOD  #TODO 是否使用 按协议理解 暂定不用 但保留代码
        
    if is_LOS != True:    
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSD/7,2), 1)
            θ_n = X_n*θ_n_2[i] + Y_n + θ_LOS_ZOD +  ZOD_UMi_NLOS_offset
            for j in range(M):
                θ_n_m_element = θ_n + 3/8*math.pow(10,μ_ZSD_UMi_NLOS)*a_m[str(j+1)]
                θ_n_m.append(θ_n_m_element) 
    if is_LOS == True:
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ZSD/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSD/7,2), 1)
            θ_n = (X_n*θ_n_2[i] + Y_n) -(X_1*θ_n_2[0] + Y_1 - θ_LOS_ZOD)
            for j in range(M):
                θ_n_m_element = θ_n + 3/8*math.pow(10,μ_ZSD_UMi_LOS)*a_m[str(j+1)] 
                θ_n_m.append(θ_n_m_element) 
    for item in θ_n_m:
        if 180<=item and item<=360:
            item = 360 - item
    return  θ_n_m 
    


#step8  Coupling of rays within a cluster for both azimuth and elevation

#step9  Generate the cross polarization power ratios
def XPR_n_m_UMi():
    μ_XPR = μ_XPR_UMi_LOS
    sigma_XPR = sigma_XPR_UMi_LOS
    XPR_n_m = []
    for i in range(N):
        for j in range(M):
            X_n_m = np.random.normal(μ_XPR, sigma_XPR, 1)  
            XPR_n_m.append(math.pow(10,X_n_m/10))
    return XPR_n_m

#step10   Draw initial random phases
Fei_θθ_n_m = []
Fei_θφ_n_m = []
Fei_φθ_n_m = []
Fei_φφ_n_m = []
def Initial_random_phases_n_m_UMi():
    for i in range(N):
        for j in range(M):
            Fei_θθ_n_m.append(random.uniform(-math.pi, math.pi))
            Fei_θφ_n_m.append(random.uniform(-math.pi, math.pi))
            Fei_φθ_n_m.append(random.uniform(-math.pi, math.pi))
            Fei_φφ_n_m.append(random.uniform(-math.pi, math.pi))
    return Fei_θθ_n_m, Fei_θφ_n_m, Fei_φθ_n_m, Fei_φφ_n_m



#step11  Generate channel coefficients for each cluster n and each receiver and transmitter element pair u, s.

F_rx_u_θ = []  # 暂时理解 无需做坐标转换,本就是全局坐标（已经过LCS—>GCS的转化）
# the field patterns of receive antenna element u in the direction of the spherical basis vectors θ^  according to (7.1-11)
F_rx_u_φ = []
# the field patterns of receive antenna element u in the direction of the spherical basis vectors φ^
F_tx_s_θ = [] 
# the field patterns of transmit antenna element s in the direction of the spherical basis vectors  θ^   
F_tx_s_φ = [] 
# the field patterns of transmit antenna element s in the direction of the spherical basis vectors φ^
for i in range(N):
    for j in range(M):
        F_rx_u_θ.append([[θ_n_m_ZOA[i*M+j]],φ_n_m_AOA[i*M+j]])  #θ_n_m_ZOA等的值由φ_n_AOA_UMi_LOS等函数获取
        F_rx_u_φ.append([[θ_n_m_ZOA[i*M+j]],φ_n_m_AOA[i*M+j]])
        F_tx_s_θ.append([[θ_n_m_ZOD[i*M+j]],φ_n_m_AOD[i*M+j]])
        F_tx_s_φ.append([[θ_n_m_ZOD[i*M+j]],φ_n_m_AOD[i*M+j]])
        
Lambda_0 = 0   # the wavelength of the carrier frequency
             
r_rx_n_m = []      
r_tx_n_m = []         
for i in range(N):
    for j in range(M):
        r_rx_n_m.append(np.array([math.sin(math.radians(θ_n_m_ZOA[i*M+j]))*math.cos(math.radians(φ_n_m_AOA[i*M+j])),math.sin(math.radians(θ_n_m_ZOA[i*M+j]))*math.sin(math.radians(φ_n_m_AOA[i*M+j])),math.cos(math.radians(θ_n_m_ZOA[i*M+j]))]))
        r_tx_n_m.append(np.array([math.sin(math.radians(θ_n_m_ZOD[i*M+j]))*math.cos(math.radians(φ_n_m_AOD[i*M+j])),math.sin(math.radians(θ_n_m_ZOD[i*M+j]))*math.sin(math.radians(φ_n_m_AOD[i*M+j])),math.cos(math.radians(θ_n_m_ZOD[i*M+j]))]))
        
r_rx_LOS = np.array([math.sin(math.radians(θ_LOS_ZOA))*math.cos(math.radians(φ_LOS_AOA)),math.sin(math.radians(θ_LOS_ZOA))*math.sin(math.radians(φ_LOS_AOA)),math.cos(math.radians(θ_LOS_ZOA))])
r_tx_LOS = np.array([math.sin(math.radians(θ_LOS_ZOD))*math.cos(math.radians(φ_LOS_AOD)),math.sin(math.radians(θ_LOS_ZOD))*math.sin(math.radians(φ_LOS_AOD)),math.cos(math.radians(θ_LOS_ZOD))])



#TODO   θ_n_m_ZOA 的单位 角度还是弧度 math 与 cmath 三角函数的区别  整个项目函数库尽量统一 done 用math库 其输入为弧度
# θ_n_m_ZOA 的单位应该为角度  使用math.radians()将角度转化为弧度
d_rx_u = 0     # the location vector of receive antenna element u
d_tx_s = 0     # the location vector of transmit antenna element s
v = 0
φ_v = 0.0      #  azimuth angle
θ_v = 0.0      #  elevation angle
v_ = v*np.transpose(np.array([math.sin(math.radians(θ_v))*math.cos(math.radians(φ_v)),math.sin(math.radians(θ_v))*math.sin(math.radians(φ_v)),math.cos(math.radians(θ_v))]))         # the UT velocity vector 

#For the N – 2 weakest clusters, say n = 3, 4,…, N, the channel coefficients 

def delta_τ(t): #TODO to verify
    return DiracDelta(t)

H_u_s_n_NLOS_t_1_and_2 = []
H_u_s_n_NLOS_t_3_N = []
H_u_s_n_m_NLOS_t = []
for i in range(N):
    temp_result1 = []
    temp_result2 = []
    for j in range(M):
        if j < 2:
            H_u_s_n_m_NLOS_t = math.sqrt(P_n_UMi_LOS/M) * np.array([F_rx_u_θ[i*M+j],F_rx_u_φ[i*M+j]]) * np.array([math.exp(complex(0, Fei_θθ_n_m[i*M+j])),math.sqrt(1/XPR_n_m[i*M+j])*math.exp(complex(0, Fei_θφ_n_m[i*M+j]))],[math.sqrt(1/XPR_n_m[i*M+j])*math.exp(complex(0, Fei_φθ_n_m[i*M+j])),math.exp(complex(0, Fei_θθ_n_m[i*M+j]))]) * np.array([F_tx_s_θ[i*M+j],F_tx_s_φ[i*M+j]]) * math.exp(complex(0, 1)*2*math.pi*(r_rx_n_m[i*M+j] * d_rx_u)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_tx_n_m[i*M+j] * d_tx_s)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_rx_n_m[i*M+j] * v_)/Lambda_0)
            for k in range(20):
                if k < 8 or k == 18 or k == 19:
                    temp_result1.append(H_u_s_n_m_NLOS_t*delta_τ(τ_n[k])*1/20)# default 3.91 ns  step 5                  
                if k >= 8 and k < 12 or k == 16 or k == 17:
                    temp_result1.append(H_u_s_n_m_NLOS_t*delta_τ(τ_n[k] + 1.28*C_DS_UMi_NLOS)*1/20) 
                if k >= 12 and k < 16:
                    temp_result1.append(H_u_s_n_m_NLOS_t*delta_τ(τ_n[k] + 2.56*C_DS_UMi_NLOS)*1/20)
            H_u_s_n_NLOS_t_1_and_2.append(sum(temp_result1))
            
        else:           
            temp_result2.append( np.array([F_rx_u_θ[i*M+j],F_rx_u_φ[i*M+j]]) * np.array([math.exp(complex(0, Fei_θθ_n_m[i*M+j])),math.sqrt(1/XPR_n_m[i*M+j])*math.exp(complex(0, Fei_θφ_n_m[i*M+j]))],[math.sqrt(1/XPR_n_m[i*M+j])*math.exp(complex(0, Fei_φθ_n_m[i*M+j])),math.exp(complex(0, Fei_θθ_n_m[i*M+j]))]) * np.array([F_tx_s_θ[i*M+j],F_tx_s_φ[i*M+j]]) * math.exp(complex(0, 1)*2*math.pi*(r_rx_n_m[i*M+j] * d_rx_u)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_tx_n_m[i*M+j] * d_tx_s)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_rx_n_m[i*M+j] * v_)/Lambda_0) )
        # H_u_s_n_m_NLOS_t.append(math.sqrt(P_n_UMi_LOS/M)*temp_result2)        
    H_u_s_n_NLOS_t_3_N.append(math.sqrt(P_n_UMi_LOS/M)*sum(temp_result2))  #TODO need to verify
    
    d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
    H_u_s_1_LOS_t = np.array([θ_LOS_ZOA,φ_LOS_AOA],[θ_LOS_ZOA,φ_LOS_AOA]) *np.array([1,0],[0,-1]) * np.array([θ_LOS_ZOD,φ_LOS_AOD],[θ_LOS_ZOD,φ_LOS_AOD]) * math.exp(complex(0, 1)*2*math.pi*d_3D/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_rx_LOS * d_rx_u)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_tx_LOS * d_tx_s)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_rx_LOS* v_)/Lambda_0)
    
    H_u_s_NLOS_τ_t =  H_u_s_n_NLOS_t_1_and_2 + H_u_s_n_NLOS_t_3_N
    H_u_s_LOS_τ_t = math.sqrt(1/(K_Umi_LOS+1))*H_u_s_NLOS_τ_t + math.sqrt(K_Umi_LOS/(K_Umi_LOS+1))*H_u_s_1_LOS_t*delta_τ(τ_n[0])
#For the two strongest clusters, say n = 1 and 2, rays are spread in delay to three sub-clusters (per cluster), with fixed delay offset.



#step12     Apply pathloss and shadowing for the channel coefficients.

    
    

if __name__=='__main__':
    pass