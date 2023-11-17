#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Fast_fading_model.py
@Time    :   2022/07/03
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''

import random
from re import L
import numpy as np
import math
from sympy import DiracDelta
import os,sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #获取到文件的动态的绝对路径，基于此，在代码中调整其他文件的相对路径
sys.path.insert(0,parentdir) 
from Pathloss import *
from LOS_probability.LOS_probability import *
from Numerical_antenna_model.Numerical_antenna_model import *


def Simulation_Parameter_Setting():
    Scenario = 'UMi_Street_canyon' #RMa, UMa, UMi_Street_canyon, InH_Office
    d_2D_out = 50*math.sqrt(2) 
    f_c = 5.9   #*1000*1000*1000  GHz
    return Scenario, d_2D_out, f_c
    

# step1 Set environment, network layout, and antenna array parameters 设置环境、网络布局和天线阵列参数  TODO Need someone to verify the parameters for me 
# c = 3.0*100*1000*1000 # speed of the llght
# d_2D = 50*math.sqrt(2) 
# h_UT = 1.5    
# h_BS = 50
# θ = 90.0     #zenith angle 
# θ_LOS_ZOD = ZOD #-45.0   # Azimuth angle Of Departure
# θ_LOS_ZOA = ZOA # 45.0   # Azimuth angle Of Arrival

# φ = 0.0     #azimuth angle
# φ_LOS_AOD = AOD # 0.0
# φ_LOS_AOA = AOA # 0.0

# F_rx = 0.0  #BS antenna field patterns 
# F_tx = 0.0  #UT antenna field patterns

# Ω_BS_a = 0.0    #BS bearing angle
# Ω_BS_b = 0.0    #BS downtilt angle
# Ω_BS_c = 0.0    #BS slant angle

# Ω_UT_a = 0.0    #UT bearing angle   方位角 
# Ω_UT_b = 10.0    #UT downtilt angle  下倾角   定义天线阵列的方位
# Ω_UT_c = 0.0    #UT slant angle     倾斜角

# UT_speed = 3.0  # Give speed and direction of motion of UT
# UT_direction = 0.0

# f_c = 5.9*1000*1000*1000    #Specify system centre frequency  3Ghz
# B = 20*1000*1000     #bandwidth   20MKHz

#step2  Assign propagation condition (LOS/NLOS)  确定传播条件
def Propagation_condition(scenario,d_2D_out,d_2D_in = 10,status='SL',d_clutter =10 ,r=0.2 , h_c =5):  #scenario 应用场景
    Pr_LOS = 1
    if scenario == 'RMa':
        Pr_LOS = Pr_LOS_RMa(d_2D_out)
    elif scenario == 'UMa':
        Pr_LOS = Pr_LOS_UMa(d_2D_out,h_UT = 1.5)
    elif scenario == 'UMi_Street_canyon':
        Pr_LOS = Pr_LOS_UMi(d_2D_out)
    elif scenario == 'InH_Office': #用户自行选用对应函数 Pr_LOS_InF的参数含义具体见 Table 7.2-4
        Pr_LOS = Pr_LOS_Indoor_Mixed_office(d_2D_in)
        # Pr_LOS = Pr_LOS_Indoor_Open_office(d_2D_in)
        # Pr_LOS = Pr_LOS_InF(d_2D,status,d_clutter,r,h_BS,h_UT,h_c)
    else:
        print('This scenario is not supported')    
      
    ret = random.random() #产生大于等于0且小于1的浮点数
    if   ret < Pr_LOS:
        propagation_condition = 'LOS'
    else:
        propagation_condition = 'NLOS'
        
    return propagation_condition



#step3  Calculate pathloss with formulas in Table 7.4.1-1 for each BS-UT link to be modelled. 计算每条链路的路径损失(包含阴影衰落)
def Calculate_pathloss(scenario,d_2D,f_c,h_BS = 35,h_UT = 1.5,h = 5,W = 20):
    PL_LOS = 0.0
    PL_NLOS = 0.0
    if scenario == 'RMa':
        PL_LOS , PL_NLOS = Pathloss_RMa.Pass_Loss_RMa_LOS_and_NLOS(d_2D,f_c,h_BS = 35,h_UT = 1.5,h = 5,W = 20)
    elif scenario == 'UMa':
        PL_LOS , PL_NLOS = Pathloss_UMa.Pass_Loss_UMa_LOS_and_NLOS(d_2D,f_c,h_BS = 25,h_UT = 1.5,h = 5,W = 20)
    elif scenario == 'UMi_Street_canyon':
        PL_LOS , PL_NLOS = Pathloss_UMi.Pass_Loss_UMi_LOS_and_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20)
    elif scenario == 'InH_Office':    
        PL_LOS , PL_NLOS = Pathloss_InH.Pass_Loss_InH_LOS_and_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20)  #用户自行选用对应函数        
        # PL_InF_LOS , PL_InF_NLOS_SL , PL_InF_NLOS_DL , PL_InF_NLOS_SH , PL_InF_NLOS_DH = Pathloss_InF.Pass_Loss_InF_LOS_and_NLOS(d_2D,f_c,h_BS = 10,h_UT = 1.5,h = 5,W = 20) 
            
    return PL_LOS , PL_NLOS


#step4  Generate large scale parameters, e.g. delay spread (DS), angular spreASD (ASA, ASD, ZSA, ZSD), Ricean K factor (K) and shadow fading (SF)生成大尺度参数  # sigma： σ
#Limit random RMS azimuth arrival and azimuth departure spread values to 104 degrees, i.e., ASA= min(ASA, 104), ASD = min(ASD, 104). Limit random RMS zenith arrival and zenith departure spread values to 52 degrees, i.e., ZSA = min(ZSA, 52), ZSD = min(ZSD, 52). 

# TODO  μ 和 sigma 组成np.random.normal 是否是正确的处理方式
def Generate_large_scale_parameters(scenario):
    lsp = {}
    if scenario == 'RMa':
        lsp['lg_DS'] = [np.random.normal( - 7.49, 0.55 , 1) ,np.random.normal( -7.43, 0.48 , 1) ,np.random.normal(-7.47, 0.24 , 1)]
        lsp['lg_ASD'] = [np.random.normal( 0.9, 0.38 , 1) ,np.random.normal( 0.95, 0.45 , 1) ,np.random.normal(0.67, 0.18 , 1)]
        lsp['lg_ASA'] = [np.random.normal( 1.52, 0.24 , 1) ,np.random.normal( 1.52, 0.13 , 1) ,np.random.normal(1.66, 0.21 , 1)]
        lsp['lg_ZSA'] = [np.random.normal( 0.47, 0.4 , 1) ,np.random.normal( 0.58, 0.37 , 1) ,np.random.normal(0.63, 0.22 , 1)]
        lsp['lg_ZSD'] = [np.random.normal(max(-1, -0.17*(d_2D/1000)- 0.01*abs(h_UT-1.5) + 0.22), 0.34 , 1) ,np.random.normal(max(-0.1, 0.19*(d_2D/1000)+ 0.01*(h_UT-1.5) + 0.28), 0.3 , 1) ,np.random.normal(max(-0.1, 0.19*(d_2D/1000)+ 0.01*(h_UT-1.5) + 0.28) , 0.3 , 1)]
        lsp['μ_offset_ZOD'] = [0, math.atan(31.5/d_2D) - math.atan(33.5/d_2D), math.atan(31.5/d_2D) - math.atan(33.5/d_2D)]
        lsp['μ_lg_ZSD'] = [max(-1, -0.17*(d_2D/1000)- 0.01*abs(h_UT-1.5) + 0.22), max(-0.1, 0.19*(d_2D/1000)+ 0.01*(h_UT-1.5) + 0.28) ,max(-0.1, 0.19*(d_2D/1000)+ 0.01*(h_UT-1.5) + 0.28)]  #为完成公式(7.5-20)的计算而引入
        
        lsp['K'] = [np.random.normal(7, 4 , 1)]
        lsp['XPR'] = [np.random.normal(12, 4 , 1), np.random.normal(7, 3 , 1), np.random.normal(7, 3 , 1)]
        lsp['μ_XPR'] = [12, 7, 7]
        lsp['sigma_XPR'] = [4, 3, 3]
        lsp['c_DS'] = [5, 11, 11]
        lsp['c_ASD'] = [2, 2, 2]
        lsp['c_ASA'] = [3, 3, 3]
        lsp['c_ZSA'] = [3, 3, 3]
        lsp['ζ'] = [3, 3, 3]
                
        lsp['N'] = [11, 10, 10]
        lsp['M'] = [20, 20, 20]
        
        lsp['r_τ'] = [3.8, 1.7, 1.7] #延迟分布比例因子
        
    elif scenario == 'UMa':
        lsp['lg_DS'] = [np.random.normal(-6.955 - 0.0963*math.log10(f_c), 0.66 , 1) ,np.random.normal(-6.28 - 0.204*math.log10(f_c), 0.39 , 1) ,np.random.normal(-6.62, 0.32 , 1)]
        lsp['lg_ASD'] = [np.random.normal(1.06 + 0.1114*math.log10(f_c), 0.28 , 1) ,np.random.normal(1.5 - 0.1144*math.log10(f_c), 0.28, 1) ,np.random.normal(1.25, 0.42 , 1)]
        lsp['lg_ASA'] = [np.random.normal(1.81, 0.2 , 1) ,np.random.normal(2.08 - 0.27*math.log10(f_c), 0.11 , 1) ,np.random.normal(1.76 , 0.16 , 1)]
        lsp['lg_ZSA'] = [np.random.normal(0.95, 0.16 , 1) ,np.random.normal(-0.3236*math.log10(f_c) + 1.512 , 0.16 , 1) ,np.random.normal(1.01 , 0.43 , 1)]
        lsp['lg_ZSD'] = [np.random.normal(max(-0.5, -2.1*(d_2D/1000) - 0.01*(h_UT-1.5) + 0.75), 0.4 , 1) ,np.random.normal(max(-0.5, -2.1*(d_2D/1000) - 0.01*(h_UT-1.5) + 0.9), 0.49 , 1) ,0.0]
        lsp['μ_offset_ZOD'] = [0, 7.66*math.log10(f_c) - 5.96 - math.pow(10, (0.208*math.log10(f_c) -0.782)* math.log10(max(25,d_2D)) -0.13*math.log10(f_c) + 2.03 -0.07*(h_UT-1.5))] 
        lsp['μ_lg_ZSD'] = [max(-0.5, -2.1*(d_2D/1000) - 0.01*(h_UT-1.5) + 0.75) ,max(-0.5, -2.1*(d_2D/1000) - 0.01*(h_UT-1.5) + 0.9) ,0.0]
               
        lsp['K'] = [np.random.normal(9, 5 , 1)]
        lsp['XPR'] = [np.random.normal(9, 3 , 1), np.random.normal(8, 3 , 1), np.random.normal(9, 5 , 1)]
        lsp['μ_XPR'] = [8, 7, 9]
        lsp['sigma_XPR'] = [4, 3, 5]
        lsp['c_DS'] = [max(0.25,6.5622-3.4084*math.log10(f_c)), max(0.25,6.5622-3.4084*math.log10(f_c)), 11]
        lsp['c_ASD'] = [5, 2, 5]
        lsp['c_ASA'] = [11, 15, 8]
        lsp['c_ZSA'] = [7, 7, 3]
        lsp['ζ'] = [3, 3, 4]
                
        lsp['N'] = [12, 20, 12]
        lsp['M'] = [20, 20, 20]
        
        lsp['r_τ'] = [2.5, 2.3, 2.2]
        
    elif scenario == 'UMi_Street_canyon':
        lsp['lg_DS'] = [np.random.normal(-0.24*math.log10(1+ f_c) - 7.14, 0.38 , 1) ,np.random.normal(-0.24*math.log10(1+ f_c) - 6.83, 0.16*math.log10(1+ f_c) + 0.28 , 1) ,np.random.normal(-6.62, 0.32 , 1)]
        lsp['lg_ASD'] = [np.random.normal(-0.05*math.log10(1+ f_c) + 1.21, 0.41 , 1) ,np.random.normal(-0.23*math.log10(1+ f_c) + 1.53, 0.11*math.log10(1+ f_c) + 0.33 , 1) ,np.random.normal(1.25, 0.42 , 1)]
        lsp['lg_ASA'] = [np.random.normal(-0.08*math.log10(1+ f_c) + 1.73, 0.014*math.log10(1+ f_c) + 0.28 , 1) ,np.random.normal(-0.08*math.log10(1+ f_c) + 1.81, 0.05*math.log10(1+ f_c) + 0.3 , 1) ,np.random.normal(1.76 , 0.16 , 1)]
        lsp['lg_ZSA'] = [np.random.normal(-0.1*math.log10(1+ f_c) + 0.73, -0.04*math.log10(1+ f_c) + 0.34 , 1) ,np.random.normal(-0.04*math.log10(1+ f_c) + 0.92, -0.07*math.log10(1+ f_c) + 0.41 , 1) ,np.random.normal(1.01 , 0.43 , 1)]
        lsp['lg_ZSD'] = [np.random.normal(max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83), 0.35 , 1) ,np.random.normal(max(-0.5, -3.1*(d_2D/1000)+ 0.01*max((h_UT-h_BS),0) + 0.2) , 0.35 , 1)  ,0.0]
        lsp['μ_offset_ZOD'] = [0, - math.pow(10,-1.5*math.log10(max(10, d_2D))+3.3)]
        lsp['μ_lg_ZSD'] = [max(-0.21, -14.8*(d_2D/1000)+ 0.01*abs(h_UT-h_BS) + 0.83) ,max(-0.5, -3.1*(d_2D/1000)+ 0.01*max((h_UT-h_BS),0) + 0.2) ,0.0]
        
        lsp['K'] = [np.random.normal(9, 5 , 1)]
        lsp['XPR'] = [np.random.normal(9, 3 , 1), np.random.normal(8, 3 , 1), np.random.normal(9, 5 , 1)]
        lsp['μ_XPR'] = [9, 8, 9]
        lsp['sigma_XPR'] = [3, 3, 5]
        lsp['c_DS'] = [5, 11, 11]
        lsp['c_ASD'] = [3, 10, 5]
        lsp['c_ASA'] = [17, 22, 8]
        lsp['c_ZSA'] = [7, 7, 3]
        lsp['ζ'] = [3, 3, 4]
        
        lsp['N'] = [12, 19, 12]
        lsp['M'] = [20, 20, 20]
        
        lsp['r_τ'] = [3, 2.1, 2.2]
        
    elif scenario == 'InH_Office':
        pass #暂时偷个懒
    
    
    return lsp



#step5  Generate cluster delays  τ_n
# N = 12      # Number of clusters
# M = 20      # Number of rays per cluster 

#propagation_condition = Propagation_condition(scenario,d_2D_out,d_2D_in = 10,status='SL',d_clutter =10 ,r=0.2 , h_c =5) 放在main内实现

def τ_n(propagation_condition,lsp):
    τ_n_2 = []
    τ_n = []
    if propagation_condition == 'LOS':
        lg_DS = lsp['lg_DS'][0] #LOS
        N = lsp['N'][0]
        r_τ = lsp['r_τ'][0]
        K = lsp['K'][0]
    else:
        lg_DS = lsp['lg_DS'][1] #NLOS
        N = lsp['N'][1]
        r_τ = lsp['r_τ'][1]

    DS = math.pow(10,lg_DS)
    for i in range(N):
        X_n = random.uniform(0, 1)
        τ_n_2.append(-r_τ*DS*math.log(X_n))  #*1000*1000*1000
    τ_n_min = min(τ_n_2)
    for i in range(N):
        τ_n.append(τ_n_2[i] - τ_n_min)
    τ_n = np.sort(τ_n)
    if propagation_condition == 'LOS':
        C_τ = 0.7705 - 0.0433*K + 0.0002*math.pow(K,2) + 0.000017*math.pow(K,3)
        return np.divide(τ_n, C_τ)
    else:      
        return τ_n
#In the case of LOS condition, additional scaling of delays is required to compensate for the effect of LOS peak addition to the delay spread. 

#step6 Generate cluster powers P_n

def P_n(propagation_condition,lsp,τ_n):
    P_n_2 = []
    P_n = []
    if propagation_condition == 'LOS':
        lg_DS = lsp['lg_DS'][0] #LOS
        N = lsp['N'][0]
        r_τ = lsp['r_τ'][0]
        if lsp['K'][0] <=0.0:
            K = 9.0
        else:
            K = lsp['K'][0]
        ζ = lsp['ζ'][0]
    else:
        lg_DS = lsp['lg_DS'][1] #NLOS
        N = lsp['N'][1]
        r_τ = lsp['r_τ'][1]
        ζ = lsp['ζ'][0]

    DS = math.pow(10,lg_DS)

    Z_n = np.random.normal(0.5, 1, 1)
    for i in range(N):
        Z_n = np.random.normal(0.0, math.pow(ζ,2), 1)
        P_n_2.append(math.exp(-τ_n[i]*(r_τ-1)/r_τ/DS)*math.pow(10,-Z_n/10))
    # print('P_n_2',P_n_2)
    sum_P_n_2= sum(P_n_2)
    if propagation_condition != 'LOS':
        for i in range(N):
            P_n.append(P_n_2[i]/sum_P_n_2)
            
    if propagation_condition == 'LOS':
        P1_LOS = K/(K + 1)   #TODO  K_R  need to verify
        # print('K',K)
        for i in range(N):
            if i != 0:  #TODO  δ(n-1)*(P1_LOS) 需要确定δ(n-1)的值  n-1不等于0时：δ(n-1)=0  n-1等于0时：δ(n-1)= +无穷 ？？？？ Solved 除了LOS 其他所有鏃功率和为1/(1+K_R)  LOS+NLOS的归一化功率和为1  仔细读协议 答案一般就在其中 nice job
                P_n.append(P_n_2[i]/sum_P_n_2/(K + 1) + 0*(P1_LOS))
            else:
                P_n.append(P_n_2[i]/sum_P_n_2/(K + 1) + 1*(P1_LOS)) #LOS分量的归一化功率 
                
    # print('P_n',P_n)
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

def φ_n_m_AOA(propagation_condition,lsp,P_n): # AOD follows a procedure similar to AOA
    φ_n_2 = []
    φ_n_m = []

    if propagation_condition == 'LOS':
        lg_ASA = lsp['lg_ASA'][0]
        N = lsp['N'][0]
        M = lsp['M'][0]        
        K = lsp['K'][0]
        c_ASA = lsp['c_ASA'][0]
    else:
        lg_ASA = lsp['lg_ASA'][1]
        N = lsp['N'][1]
        M = lsp['M'][1]   
        c_ASA = lsp['c_ASA'][1]

    ASA= min(math.pow(10,lg_ASA), 104) 
    if propagation_condition == 'LOS':
        C_φ = C_φ_NLOS_A[str(N)]*(1.1035 - 0.028*K - 0.002*math.pow(K,2) + 0.0001*math.pow(K,3))
    else:
        C_φ = C_φ_NLOS_A[str(N)]
    for i in range(N):
        φ_n_2.append(2*(ASA/1.4)*math.sqrt(-math.log(P_n[i]/max(P_n)))/C_φ) 
    if propagation_condition != 'LOS': 
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASA/7,2), 1)
            φ_n = X_n*φ_n_2[i] + Y_n + φ_LOS_AOA
            for j in range(M):
                φ_n_m_element = φ_n + c_ASA*a_m[str(j+1)]
                φ_n_m.append(φ_n_m_element) 
    if propagation_condition == 'LOS':
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ASA/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASA/7,2), 1)
            φ_n = (X_n*φ_n_2[i] + Y_n) -(X_1*φ_n_2[0] + Y_1 - φ_LOS_AOA)
            for j in range(M):
                φ_n_m_element = φ_n + c_ASA*a_m[str(j+1)] 
                φ_n_m.append(φ_n_m_element) 
    return  φ_n_m       

def φ_n_m_AOD(propagation_condition,lsp,P_n):
    φ_n_2 = []
    φ_n_m = []

    if propagation_condition == 'LOS':
        lg_ASD = lsp['lg_ASD'][0]
        N = lsp['N'][0]
        M = lsp['M'][0]        
        K = lsp['K'][0]
        c_ASD = lsp['c_ASD'][0]
    else:
        lg_ASD = lsp['lg_ASD'][1]
        N = lsp['N'][1]
        M = lsp['M'][1]   
        c_ASD = lsp['c_ASD'][1]

    ASD= min(math.pow(10,lg_ASD), 104) 
    if propagation_condition == 'LOS':
        C_φ = C_φ_NLOS_A[str(N)]*(1.1035 - 0.028*K - 0.002*math.pow(K,2) + 0.0001*math.pow(K,3))
    else:
        C_φ = C_φ_NLOS_A[str(N)]
    for i in range(N):
        φ_n_2.append(2*(ASD/1.4)*math.sqrt(-math.log(P_n[i]/max(P_n)))/C_φ) 
    if propagation_condition != 'LOS': 
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASD/7,2), 1)
            φ_n = X_n*φ_n_2[i] + Y_n + φ_LOS_AOD
            for j in range(M):
                φ_n_m_element = φ_n + c_ASD*a_m[str(j+1)]
                φ_n_m.append(φ_n_m_element) 
    if propagation_condition == 'LOS':
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ASD/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ASD/7,2), 1)
            φ_n = (X_n*φ_n_2[i] + Y_n) -(X_1*φ_n_2[0] + Y_1 - φ_LOS_AOD)
            for j in range(M):
                φ_n_m_element = φ_n + c_ASD*a_m[str(j+1)] 
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
                      
def θ_n_m_ZOA(propagation_condition,lsp,P_n, BS_UT_link ='O2I'):  #θ 用 θ 更合适
    θ_n_2 = []
    θ_n_m = []

    if propagation_condition == 'LOS':
        lg_ZSA = lsp['lg_ZSA'][0]
        N = lsp['N'][0]
        M = lsp['M'][0]        
        K = lsp['K'][0]
        c_ZSA = lsp['c_ZSA'][0]
    else:
        lg_ZSA = lsp['lg_ZSA'][1]
        N = lsp['N'][1]
        M = lsp['M'][1]   
        c_ZSA = lsp['c_ZSA'][1]

    ZSA = min(math.pow(10,lg_ZSA), 52) 
    if propagation_condition == 'LOS':
        C_θ = C_θ_NLOS_Z[str(N)]*(1.3086 + 0.0339*K - 0.0077*math.pow(K,2) + 0.0002*math.pow(K,3))
    else:
        C_θ = C_θ_NLOS_Z[str(N)]
    for i in range(N):
        θ_n_2.append(-ZSA*math.log(P_n[i]/max(P_n))/C_θ) 
        
    if BS_UT_link == 'O2I':
        θ_LOS_ZOA_ = 90
    else:
        θ_LOS_ZOA_ = θ_LOS_ZOA

    if propagation_condition != 'LOS':   
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSA/7,2), 1)
            θ_n = X_n*θ_n_2[i] + Y_n + θ_LOS_ZOA_ 
            for j in range(M):
                θ_n_m_element = θ_n + c_ZSA*a_m[str(j+1)]
                θ_n_m.append(θ_n_m_element) 
    if propagation_condition == 'LOS':
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ZSA/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSA/7,2), 1)
            θ_n = (X_n*θ_n_2[i] + Y_n) -(X_1*θ_n_2[0] + Y_1 - θ_LOS_ZOA)
            for j in range(M):
                θ_n_m_element = θ_n + c_ZSA*a_m[str(j+1)] 
                θ_n_m.append(θ_n_m_element) 
    for item in θ_n_m:
        if 180<=item and item<=360:
            item = 360 - item
    return  θ_n_m   

def θ_n_m_ZOD(propagation_condition,lsp,P_n, BS_UT_link ='O2I'):
    θ_n_2 = []
    θ_n_m = []

    if propagation_condition == 'LOS':
        lg_ZSD = lsp['lg_ZSD'][0]
        N = lsp['N'][0]
        M = lsp['M'][0]        
        K = lsp['K'][0]
        # c_ZSD = lsp['c_ZSD'][0]
        μ_lg_ZSD = lsp['μ_lg_ZSD'][0]
        μ_offset_ZOD = lsp['μ_offset_ZOD'][0]
    else:
        lg_ZSD = lsp['lg_ZSD'][1]
        N = lsp['N'][1]
        M = lsp['M'][1]   
        # c_ZSD = lsp['c_ZSD'][1]
        μ_lg_ZSD = lsp['μ_lg_ZSD'][1]
        μ_offset_ZOD = lsp['μ_offset_ZOD'][1]
    ZSD = min(math.pow(lg_ZSD,10), 52) 
    if propagation_condition == 'LOS':
        C_θ = C_θ_NLOS_Z[str(N)]*(1.3086 + 0.0339*K - 0.0077*math.pow(K,2) + 0.0002*math.pow(K,3))
    else:
        C_θ = C_θ_NLOS_Z[str(N)]
    for i in range(N):
        # print(P_n[i],max(P_n),sum(P_n))
        θ_n_2.append(-ZSD*math.log(P_n[i]/max(P_n))/C_θ) 
        
    if BS_UT_link == 'O2I':
        θ_LOS_ZOD_ = 90
    else:
        θ_LOS_ZOD_ = θ_LOS_ZOD  #TODO 是否使用 按协议理解 暂定不用 但保留代码
        
    if propagation_condition != 'LOS':  
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSD/7,2), 1)
            θ_n = X_n*θ_n_2[i] + Y_n + θ_LOS_ZOD + μ_offset_ZOD
            for j in range(M):
                θ_n_m_element = θ_n + 3/8*math.pow(10,μ_lg_ZSD)*a_m[str(j+1)]
                θ_n_m.append(θ_n_m_element) 
    if propagation_condition == 'LOS':
        X_1 = random.uniform(-1, 1)
        Y_1 = np.random.normal(0.0, math.pow(ZSD/7,2), 1)
        for i in range(N):
            X_n = random.uniform(-1, 1)
            Y_n = np.random.normal(0.0, math.pow(ZSD/7,2), 1)
            θ_n = (X_n*θ_n_2[i] + Y_n) -(X_1*θ_n_2[0] + Y_1 - θ_LOS_ZOD)
            for j in range(M):
                θ_n_m_element = θ_n + 3/8*math.pow(10,μ_lg_ZSD)*a_m[str(j+1)] 
                θ_n_m.append(θ_n_m_element) 
    for item in θ_n_m:
        if 180<=item and item<=360:
            item = 360 - item
    return  θ_n_m 
    

#step8  Coupling of rays within a cluster for both azimuth and elevation

#step9  Generate the cross polarization power ratios
def XPR_n_m(propagation_condition,lsp):
    if propagation_condition == 'LOS':
        N = lsp['N'][0]
        M = lsp['M'][0]    
        μ_XPR = lsp['μ_XPR'][0]
        sigma_XPR = lsp['sigma_XPR'][0]   
    else:
        N = lsp['N'][1]
        M = lsp['M'][1]   
        μ_XPR = lsp['μ_XPR'][1]
        sigma_XPR = lsp['sigma_XPR'][1]   
        
    XPR_n_m = []
    for i in range(N):
        for j in range(M):
            X_n_m = np.random.normal(μ_XPR, sigma_XPR, 1)  
            XPR_n_m.append(math.pow(10,X_n_m/10))
    return XPR_n_m

#step10   Draw initial random phases

def Initial_random_phases_n_m(lsp,propagation_condition):
    Fei_θθ_n_m = []
    Fei_θφ_n_m = []
    Fei_φθ_n_m = []
    Fei_φφ_n_m = []

    if propagation_condition == 'LOS':
        N = lsp['N'][0]
        M = lsp['M'][0]        
    else:
        N = lsp['N'][1]
        M = lsp['M'][1]   
    for i in range(N):
        for j in range(M):
            Fei_θθ_n_m.append(random.uniform(-math.pi, math.pi))
            Fei_θφ_n_m.append(random.uniform(-math.pi, math.pi))
            Fei_φθ_n_m.append(random.uniform(-math.pi, math.pi))
            Fei_φφ_n_m.append(random.uniform(-math.pi, math.pi))
    return Fei_θθ_n_m, Fei_θφ_n_m, Fei_φθ_n_m, Fei_φφ_n_m



#step11  Generate channel coefficients for each cluster n and each receiver and transmitter element pair u, s.
def  Generate_channel_coefficients(lsp,propagation_condition,f_c,  φ_n_m_AOA,φ_n_m_AOD,θ_n_m_ZOA,θ_n_m_ZOD,  Fei_θθ_n_m,Fei_θφ_n_m,Fei_φθ_n_m,Fei_φφ_n_m,  XPR_n_m,  τ_n,  P_n ):
    
    F_rx_u_θ = []  # 暂时理解 无需做坐标转换,本就是全局坐标（已经过LCS—>GCS的转化）
    # the field patterns of receive antenna element u in the direction of the spherical basis vectors θ^  according to (7.1-11)
    F_rx_u_φ = []
    # the field patterns of receive antenna element u in the direction of the spherical basis vectors φ^
    F_tx_s_θ = [] 
    # the field patterns of transmit antenna element s in the direction of the spherical basis vectors θ^   
    F_tx_s_φ = [] 
    # the field patterns of transmit antenna element s in the direction of the spherical basis vectors φ^
    
    if propagation_condition == 'LOS':
        lg_ZSD = lsp['lg_ZSD'][0]
        N = lsp['N'][0]
        M = lsp['M'][0]        
        K = lsp['K'][0]
        c_DS = lsp['c_DS'][0]
        # c_ZSD = lsp['c_ZSD'][0]
        μ_lg_ZSD = lsp['μ_lg_ZSD'][0]
        μ_offset_ZOD = lsp['μ_offset_ZOD'][0]
    else:
        lg_ZSD = lsp['lg_ZSD'][1]
        N = lsp['N'][1]
        M = lsp['M'][1]   
        c_DS = lsp['c_DS'][1]
        # c_ZSD = lsp['c_ZSD'][1]
        μ_lg_ZSD = lsp['μ_lg_ZSD'][1]
        μ_offset_ZOD = lsp['μ_offset_ZOD'][1]
        
    for i in range(N):
        for j in range(M):
            F_rx_u_θ.append(1) 
            F_rx_u_φ.append(1) 
            F_tx_s_θ.append(1) 
            F_tx_s_φ.append(1) 
            
    Lambda_0 = c/f_c/(1000*1000*1000)  # the wavelength of the carrier frequency
                
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
    d_rx_u = np.transpose(np.array([0,0,1]))      # the location vector of receive antenna element u   TODO
    d_tx_s = np.transpose(np.array([math.sqrt(2)/2,0,math.sqrt(2)/2]))     # the location vector of transmit antenna element s
    v = 0
    φ_v = 0.0      #  azimuth angle   TODO
    θ_v = 0.0      #  elevation angle
    
      
    v_ = v*np.transpose(np.array([math.sin(math.radians(θ_v))*math.cos(math.radians(φ_v)),math.sin(math.radians(θ_v))*math.sin(math.radians(φ_v)),math.cos(math.radians(θ_v))]))         # the UT velocity vector 

    #For the N – 2 weakest clusters, say n = 3, 4,…, N, the channel coefficients 

    H_u_s_n_NLOS_t_1_and_2 = []
    H_u_s_n_NLOS_t_3_N = []
    H_u_s_n_m_NLOS_t = []
    
    for i in range(N):
        temp_result1 = []
        temp_result2 = []
        for j in range(M):
            if i < 2:
                temp2 = cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_n_m[i*M+j] , np.transpose(d_rx_u))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_tx_n_m[i*M+j],np.transpose(d_tx_s))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_n_m[i*M+j], np.transpose(v_))/Lambda_0)
                print('temp2',temp2)
                
                temp3 = np.dot( np.dot(np.array([F_rx_u_θ[i*M+j],F_rx_u_φ[i*M+j]]),np.array([[cmath.exp(complex(0, Fei_θθ_n_m[i*M+j])),math.sqrt(1/XPR_n_m[i*M+j])*cmath.exp(complex(0, Fei_θφ_n_m[i*M+j]))],[math.sqrt(1/XPR_n_m[i*M+j])*cmath.exp(complex(0, Fei_φθ_n_m[i*M+j])),cmath.exp(complex(0, Fei_φφ_n_m[i*M+j]))]])), np.array([[F_tx_s_θ[i*M+j]],[F_tx_s_φ[i*M+j]]]) )
                print('temp3',temp3)
                
                H_u_s_n_m_NLOS_t = math.sqrt(P_n[i]/M) * np.dot( np.dot(np.array([F_rx_u_θ[i*M+j],F_rx_u_φ[i*M+j]]),np.array([[cmath.exp(complex(0, Fei_θθ_n_m[i*M+j])),math.sqrt(1/XPR_n_m[i*M+j])*cmath.exp(complex(0, Fei_θφ_n_m[i*M+j]))],[math.sqrt(1/XPR_n_m[i*M+j])*cmath.exp(complex(0, Fei_φθ_n_m[i*M+j])),cmath.exp(complex(0, Fei_φφ_n_m[i*M+j]))]])), np.array([[F_tx_s_θ[i*M+j]],[F_tx_s_φ[i*M+j]]]) )    * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_n_m[i*M+j] , np.transpose(d_rx_u))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_tx_n_m[i*M+j],np.transpose(d_tx_s))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_n_m[i*M+j], np.transpose(v_))/Lambda_0)
                print('H_u_s_n_m_NLOS_t',H_u_s_n_m_NLOS_t)                

                for k in range(20):
                    if k < 8 or k == 18 or k == 19:
                        # print(delta_τ(τ_n[i]*1000*1000*1000),(τ_n[i]*1000*1000*1000))
                        temp_result1.append([H_u_s_n_m_NLOS_t*1/20,τ_n[i]])  # default 3.91 ns  step 5         
                    if k >= 8 and k < 12 or k == 16 or k == 17:
                        temp_result1.append([H_u_s_n_m_NLOS_t*1/20,τ_n[i]+ 1.28*c_DS]) 
                    if k >= 12 and k < 16:
                        temp_result1.append([H_u_s_n_m_NLOS_t*1/20,τ_n[i]+ 2.56*c_DS])          
            else:         
                temp_result2.append(  [math.sqrt(P_n[i]/M)* np.dot( np.dot(np.array([F_rx_u_θ[i*M+j],F_rx_u_φ[i*M+j]]) , np.array([[cmath.exp(complex(0, Fei_θθ_n_m[i*M+j])),math.sqrt(1/XPR_n_m[i*M+j])*cmath.exp(complex(0, Fei_θφ_n_m[i*M+j]))],[math.sqrt(1/XPR_n_m[i*M+j])*cmath.exp(complex(0, Fei_φθ_n_m[i*M+j])),cmath.exp(complex(0, Fei_φφ_n_m[i*M+j]))]])), np.array([[F_tx_s_θ[i*M+j]],[F_tx_s_φ[i*M+j]]]) ) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_n_m[i*M+j] , np.transpose(d_rx_u))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_tx_n_m[i*M+j],np.transpose(d_tx_s))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_n_m[i*M+j], np.transpose(v_))/Lambda_0), τ_n[i]])  

        H_u_s_n_NLOS_t_1_and_2 = temp_result1            
        H_u_s_n_NLOS_t_3_N = temp_result2
    H_u_s_NLOS_τ_t =  H_u_s_n_NLOS_t_1_and_2 + H_u_s_n_NLOS_t_3_N
        
    if propagation_condition != 'LOS':
        return H_u_s_NLOS_τ_t
    else:    
        d_3D = math.sqrt(math.pow(d_2D, 2)+math.pow(abs(h_BS-h_UT), 2))
        H_u_s_1_LOS_t = np.dot( np.dot(np.array([1,1]), np.array([[1,0],[0,-1]]) ), np.array([[1],[1]])) * cmath.exp(complex(0, 1)*2*np.pi*d_3D/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_LOS ,np.transpose(d_rx_u))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_tx_LOS ,np.transpose(d_tx_s))/Lambda_0) * cmath.exp(complex(0, 1)*2*np.pi*np.dot(r_rx_LOS , np.transpose(v_))/Lambda_0)

        # H_u_s_LOS_τ_t = math.sqrt(1/(K+1))*H_u_s_NLOS_τ_t + [math.sqrt(K/(K+1))*H_u_s_1_LOS_t,τ_n[0]]
        print(τ_n[0],τ_n)
        H_u_s_LOS_τ_t = math.sqrt(1/(K+1))* np.array(H_u_s_NLOS_τ_t) + math.sqrt(K/(K+1))* np.array(H_u_s_1_LOS_t)*(τ_n[-1]-τ_n[0])
        
        return H_u_s_LOS_τ_t
    #For the two strongest clusters, say n = 1 and 2, rays are spread in delay to three sub-clusters (per cluster), with fixed delay offset.



#step12     Apply pathloss and shadowing for the channel coefficients.

    
    

if __name__=='__main__': #应该使所有的函数以某个周期时间（越快越好）快速迭代运行
    
    scenario, d_2D_out, f_c = Simulation_Parameter_Setting()  #获取实验参数设置
    
    point1, point2, consider_building_occlusion = [0,0,50] , [50,0,1.5], False
    AOD,AOA,ZOD,ZOA = Get_angels(point1,point2, consider_building_occlusion)
    print(AOD,AOA,ZOD,ZOA)

    # step1 Set environment, network layout, and antenna array parameters 设置环境、网络布局和天线阵列参数  TODO Need someone to verify the parameters for me 
    c = 3.0*100*1000*1000 # speed of the llght
    x1,y1,z1 = point1
    x2,y2,z2 = point2
    d_2D = math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1),0.5) #50*math.sqrt(2) 
    h_UT = 1.5    
    h_BS = 50
    θ = 90.0     #zenith angle 
    θ_LOS_ZOD = ZOD #-45.0   # Azimuth angle Of Departure
    θ_LOS_ZOA = ZOA # 45.0   # Azimuth angle Of Arrival

    φ = 0.0     #azimuth angle
    φ_LOS_AOD = AOD # 0.0
    φ_LOS_AOA = AOA # 0.0

    F_rx = 0.0  #BS antenna field patterns 
    F_tx = 0.0  #UT antenna field patterns

    Ω_BS_a = 0.0    #BS bearing angle
    Ω_BS_b = 0.0    #BS downtilt angle
    Ω_BS_c = 0.0    #BS slant angle

    Ω_UT_a = 0.0    #UT bearing angle   方位角 
    Ω_UT_b = 10.0    #UT downtilt angle  下倾角   定义天线阵列的方位
    Ω_UT_c = 0.0    #UT slant angle     倾斜角

    UT_speed = 3.0  # Give speed and direction of motion of UT
    UT_direction = 0.0

    f_c = 5.9   #*1000*1000*1000    #Specify system centre frequency  3Ghz
    B = 20*1000*1000     #bandwidth   20MKHz
    
    result = []
    for i in range(10): #NRT仿真中，不在具有时间的概念，用每次循环表征一个无线传播的时隙(1ns，考虑到多径延时的度量单位为ns)，其他随时间改变的量值，通过对应的时间序列计算获取 
        # TODO  确定多久进行一次是否为LOS路径的估计 1ns太快了吧
        propagation_condition = Propagation_condition(scenario,d_2D_out,d_2D_in = 10,status='SL',d_clutter =10 ,r=0.2 , h_c =5) # step2 计算是否为LOS路径
        print(propagation_condition)
        PL_LOS , PL_NLOS = Calculate_pathloss(scenario,d_2D,f_c,h_BS = 50,h_UT = 1.5,h = 5,W = 20)  # step3 计算每条链路的路径损失(包含阴影衰落)
        print(PL_LOS , PL_NLOS)
        lsp = Generate_large_scale_parameters(scenario)  #step4 生成大尺度参数 
        print('lsp',lsp)
        τ_n_ = τ_n(propagation_condition,lsp)  #step5  Generate cluster delays  τ_n
        print('τ_n_',τ_n_)
        P_n_ = P_n(propagation_condition,lsp,τ_n_)   #step6 Generate cluster powers P_n
        print('P_n_',P_n_)
        # #step7 Generate arrival angles and departure angles for both azimuth and elevation.
        θ_n_m_ZOD_ = θ_n_m_ZOD(propagation_condition,lsp,P_n_, BS_UT_link ='O2I')
        θ_n_m_ZOA_ = θ_n_m_ZOA(propagation_condition,lsp,P_n_, BS_UT_link ='O2I')
        φ_n_m_AOA_ = φ_n_m_AOA(propagation_condition,lsp,P_n_)
        φ_n_m_AOD_ = φ_n_m_AOD(propagation_condition,lsp,P_n_)
        print('θ_n_m_ZOD_',θ_n_m_ZOD_)
        print('θ_n_m_ZOA_',θ_n_m_ZOA_)
        print('φ_n_m_AOA_',φ_n_m_AOA_)
        print('φ_n_m_AOD_',φ_n_m_AOD_)
        # #step8  Coupling of rays within a cluster for both azimuth and elevation
        # # TODO        
        # #step9  Generate the cross polarization power ratios
        XPR_n_m_ = XPR_n_m(propagation_condition,lsp)  
        print('XPR_n_m_',XPR_n_m_)
        # #step10  Draw initial random phases
        Fei_θθ_n_m, Fei_θφ_n_m, Fei_φθ_n_m, Fei_φφ_n_m = Initial_random_phases_n_m(lsp,propagation_condition)
        print('Fei_θθ_n_m',Fei_θθ_n_m)
        print('Fei_θφ_n_m',Fei_θφ_n_m)
        print('Fei_φθ_n_m',Fei_φθ_n_m)
        print('Fei_φφ_n_m',Fei_φφ_n_m)
        # #step11  Generate channel coefficients for each cluster n and each receiver and transmitter element pair u, s.
        H_u_s = Generate_channel_coefficients(lsp,propagation_condition,f_c,  φ_n_m_AOA_,φ_n_m_AOD_,θ_n_m_ZOA_,θ_n_m_ZOD_,  Fei_θθ_n_m,Fei_θφ_n_m,Fei_φθ_n_m,Fei_φφ_n_m,  XPR_n_m_,  τ_n_,  P_n_ )
        print('H_u_s',H_u_s)
        # #step12   Apply pathloss and shadowing for the channel coefficients.
        # # TODO
        
        # result.append([H_u_s])

    



#主要问题：1.初始参数的合理设置；2.全局坐标系与各对象（基站与移动终端）的位置、终端的运动状态（矢量）生成；3.delta_τ函数的有效实现，ns级的仿真如何进行（是否可以用1ms的仿真时间对应1ns的实际时间，可以的话，考虑如何实现）  想法 不需要严格以1ms对应1ns,可以考虑在lms的时间内生成1*1000*1000个对应的相关结果；4.如何获得完整的验证数据集（以方便进行多种工况下、各个中间变量的模拟计算值与验证值的对比）;5.合适的循环(调度)计算机制，计算周期