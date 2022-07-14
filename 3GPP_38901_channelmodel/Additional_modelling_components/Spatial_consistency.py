#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Spatial_consistency.py  空间一致性
@Time    :   2022/06/21
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
为了在移动性的情况下提供真实的模型输出,即当UE移动时或者在MU-MIMO场景下,使用Spatial_consistency.py来修正信道实现的空间分布
对于基线模型,仅修正簇间参数。然而,对于高分辨率可选模型,簇内的参数也要修正。相关距离范围为10~50 m,取决于参数和场景。该方法确实使得信道随UE的移动而连续变化。然而不能确保变化反应实际情况,如在多普勒和生灭过程中。例如对于室外用户，信道状态可能是平稳的，直到用户移动到街道十字路口拐角附近。对于室内用户，当从一个房间移动到另一个房间时，可能有同样的影响。这可能对基于动态无线信道的波束跟踪技术的优化产生重要影响。出于这个原因，下一节将用阻挡模型提供一个更实际的基于几何的选项。
'''


import numpy as np
import math

import scipy


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

#7.6.4.1	Blockage model A


# For self-blocking    the blocking region in UT LCS
Portrait_mode = {
    'φ_sb_2': 260,
    'x_sb': 120,
    'θ_sb_2': 100,
    'y_sb': 80
}

Landscape_mode = {
    'φ_sb_2': 40,
    'x_sb': 160,
    'θ_sb_2': 110,
    'y_sb': 75
}

if Portrait_mode['θ_sb_2'] - Portrait_mode['y_sb']/2 <= θ and θ <= Portrait_mode['θ_sb_2'] + Portrait_mode['y_sb']/2:
    if Portrait_mode['φ_sb_2'] - Portrait_mode['x_sb']/2 <= θ and θ <= Portrait_mode['φ_sb_2'] + Portrait_mode['x_sb']/2:
        if abs(φ_AOA_2 - Portrait_mode['φ_sb_2']) < Portrait_mode['x_sb']/2 and abs(φ_ZOA_2 - Portrait_mode['θ_sb_2']) < Portrait_mode['y_sb']/2:
            is_blocked = True
            attenuation = 30


# For non-self-blocking k = 1, …, 4, the blocking region in GCS
InH_scenario = {
    'φ_k': np.random.uniform(0,360),
    'x_k': np.random.uniform(15,45),
    'θ_k': 90,
    'y_k': np.random.uniform(5,15),
    'r': 2
}

UMi_UMa_RMa_scenarios = {
    'φ_k': np.random.uniform(0,360),
    'x_k': np.random.uniform(5,15),
    'θ_k': 90,
    'y_k': 5,
    'r': 10
}
status = 'UMi_UMa_RMa_scenarios'
if status == 'UMi_UMa_RMa_scenarios':
    φ_k = UMi_UMa_RMa_scenarios['φ_k']
    x_k = UMi_UMa_RMa_scenarios['x_k']
    θ_k = UMi_UMa_RMa_scenarios['θ_k']
    y_k = UMi_UMa_RMa_scenarios['y_k']
    r = UMi_UMa_RMa_scenarios['r']

if -y_k <θ_ZOA-θ_k and φ_ZOA-θ_k <= -y_k/2:
    if x_k/2 < φ_AOA-φ_k and φ_AOA-φ_k <= x_k:
        symbol_A1 = -1
        symbol_A2 = 1
        symbol_Z1 = 1
        symbol_Z2 = -1
    elif -x_k/2 < φ_AOA-φ_k and φ_AOA-φ_k <= x_k/2:
        symbol_A1 = 1
        symbol_A2 = 1
        symbol_Z1 = 1
        symbol_Z2 = -1        
    elif -x_k < φ_AOA-φ_k and φ_AOA-φ_k <= -x_k/2:
        symbol_A1 = 1
        symbol_A2 = -1
        symbol_Z1 = 1
        symbol_Z2 = -1
elif -y_k/2 <θ_ZOA-θ_k and φ_ZOA-θ_k <= y_k/2:
    if x_k/2 < φ_AOA-φ_k and φ_AOA-φ_k <= x_k:
        symbol_A1 = -1
        symbol_A2 = 1
        symbol_Z1 = 1
        symbol_Z2 = 1
    elif -x_k/2 < φ_AOA-φ_k and φ_AOA-φ_k <= x_k/2:
        symbol_A1 = 1
        symbol_A2 = 1
        symbol_Z1 = 1
        symbol_Z2 = 1        
    elif -x_k < φ_AOA-φ_k and φ_AOA-φ_k <= -x_k/2:
        symbol_A1 = 1
        symbol_A2 = -1
        symbol_Z1 = 1
        symbol_Z2 = 1
elif y_k/2 <θ_ZOA-θ_k and φ_ZOA-θ_k <= y_k:
    if x_k/2 < φ_AOA-φ_k and φ_AOA-φ_k <= x_k:
        symbol_A1 = -1
        symbol_A2 = 1
        symbol_Z1 = -1
        symbol_Z2 = 1
    elif -x_k/2 < φ_AOA-φ_k and φ_AOA-φ_k <= x_k/2:
        symbol_A1 = 1
        symbol_A2 = 1
        symbol_Z1 = -1
        symbol_Z2 = 1        
    elif -x_k < φ_AOA-φ_k and φ_AOA-φ_k <= -x_k/2:
        symbol_A1 = 1
        symbol_A2 = -1
        symbol_Z1 = -1
        symbol_Z2 = 1

if θ_k - y_k/2 <= θ and θ <= θ_k + y_k/2:
    if  φ_k - x_k/2 <= θ and θ <= φ_k + x_k/2:
        
        A1 = φ_AOA - (φ_k + x_k/2)
        F_A1 = 1/math.tan(symbol_A1*math.pi/2*math.sqrt(math.pi/lambda_*r*(1-math.cos(A1)-1)))
        A2 = φ_AOA - (φ_k - x_k/2)
        F_A1 = 1/math.tan(symbol_A2*math.pi/2*math.sqrt(math.pi/lambda_*r*(1-math.cos(A2)-1)))
        
        Z1 = θ_ZOA - (θ_k + y_k/2)
        F_Z1 = 1/math.tan(symbol_Z1*math.pi/2*math.sqrt(math.pi/lambda_*r*(1-math.cos(Z1)-1)))
        Z2 = θ_ZOA - (θ_k - y_k/2)
        F_Z2 = 1/math.tan(symbol_Z2*math.pi/2*math.sqrt(math.pi/lambda_*r*(1-math.cos(Z2)-1)))
                
        L_dB = -20*math.log10(1 - (F_A1 + F_A2)*(F_Z1 + F_Z2))
        is_blocked = True
    
# Spatial and temporal consistency of each blocker.
d_corr_UMi_LOS = 10
d_corr_UMi_NLOS = 10
d_corr_UMi_O2I = 5

d_corr_UMa_LOS = 10
d_corr_UMa_NLOS = 10
d_corr_UMa_O2I = 5

d_corr_RMa_LOS = 10
d_corr_RMa_NLOS = 10
d_corr_RMa_O2I = 5

d_corr_InH_LOS = 5
d_corr_InH_NLOS = 5

t_corr = d_corr/v  #v is the speed of the moving blocker.
R_datle_x_and_datle_t = math.exp(-abs(datle_x)/d_corr+abs(datle_t)/t_corr) #TODO


if __name__=='__main__':
    pass