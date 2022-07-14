#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Explicit_ground_reflection_model.py 
@Time    :   2022/06/28
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import math
import numpy as np


'''
In case the ground reflection shall be modelled explicitly
'''


c = 3.0*100000000 # speed of the llght

Material_properties = {
    'Concrete':{
        'a_Epsilon': 5.31,
        'b_Epsilon': 0,
        'c_sigma': 0.0326,
        'd_sigma': 0.8095
    },
    'Brick':{
        'a_Epsilon': 3.75,
        'b_Epsilon': 0,
        'c_sigma': 0.038,
        'd_sigma': 0.0
    },
    'Plasterboard':{
        'a_Epsilon': 2.94,
        'b_Epsilon': 0,
        'c_sigma': 0.0116 ,
        'd_sigma': 0.7076
    },
    'Wood':{
        'a_Epsilon': 1.99,
        'b_Epsilon': 0,
        'c_sigma': 0.0047,
        'd_sigma': 1.0718
    },
    'Floorboard':{
        'a_Epsilon': 3.66,
        'b_Epsilon': 0,
        'c_sigma': 0.0044,
        'd_sigma': 1.3515
    },
    'Metal':{
        'a_Epsilon': 1.0,
        'b_Epsilon':0.0 ,
        'c_sigma': 1e+7,
        'd_sigma': 0
    },
    'Very_dry_ground':{
        'a_Epsilon': 3.0,
        'b_Epsilon': 0,
        'c_sigma': 0.00015,
        'd_sigma': 2.52
    },
    'Medium_dry_ground':{
        'a_Epsilon': 15,
        'b_Epsilon': -0.1,
        'c_sigma': 0.035,
        'd_sigma': 1.63
    },
    'Wet_ground':{
        'a_Epsilon':30,
        'b_Epsilon': -0.4,
        'c_sigma': 0.15,
        'd_sigma': 1.30
    }

}




d_GR = math.sqrt(math.pow(h_tx + h_rx,2) + math.pow(d_2D,2))
τ_GR = d_GR/c


d_3D = math.sqrt(math.pow(h_tx - h_rx,2) + math.pow(d_2D,2))
τ_GR = d_3D/c



θ_GR_ZOD = 180 - math.atan(d_2D/(h_tx + h_rx))*180/math.pi
φ_GR_AOD = φ_LOS_AOD
θ_GR_ZOA = θ_GR_ZOD
φ_GR_AOA = φ_GR_AOD + 180

Epsilon_0 = 8.854187817e-12      #8.854187817... × 10−12 F·m−1.
Epsilon_r = a_Epsilon * math.pow(f_c/1e9,b_Epsilon)    #f_c being the center frequency in Hz
sigma = c_sigma * math.pow(f_c/1e9,d_sigma)
Epsilon_GR = (Epsilon_r - complex(0, 1)*sigma/(2*math.pi*f_c*Epsilon_0)) * Epsilon_0

R_GR_ll = (Epsilon_GR/Epsilon_0*(math.cos(θ_GR_ZOD)) + math.sqrt(Epsilon_GR/Epsilon_0 - math.pow(math.sin(θ_GR_ZOD),2)))/(Epsilon_GR/Epsilon_0*(math.cos(θ_GR_ZOD)) - math.sqrt(Epsilon_GR/Epsilon_0 - math.pow(math.sin(θ_GR_ZOD),2)))

R_GR_l_ = (math.cos(θ_GR_ZOD) + math.sqrt(Epsilon_GR/Epsilon_0 - math.pow(math.sin(θ_GR_ZOD),2)))/(math.cos(θ_GR_ZOD) - math.sqrt(Epsilon_GR/Epsilon_0 - math.pow(math.sin(θ_GR_ZOD),2)))

r_tx_GR = np.array([math.sin(math.radians(θ_GR_ZOD))*math.cos(math.radians(φ_GR_AOD)),math.sin(math.radians(θ_GR_ZOD))*math.sin(math.radians(φ_GR_AOD)),math.cos(math.radians(θ_GR_ZOD))])

r_rx_GR = np.array([math.sin(math.radians(θ_GR_ZOA))*math.cos(math.radians(φ_GR_AOA)),math.sin(math.radians(θ_GR_ZOA))*math.sin(math.radians(φ_GR_AOA)),math.cos(math.radians(θ_GR_ZOA))])


H_u_s_GR_t = np.array([θ_GR_ZOA,φ_GR_AOA],[θ_GR_ZOA,φ_GR_AOA]) *np.array([R_GR_ll,0],[0,-R_GR_l_]) * np.array([θ_GR_ZOD,φ_GR_AOD],[θ_GR_ZOD,φ_GR_AOD]) * math.exp(complex(0, 1)*2*math.pi*d_GR/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_rx_GR * d_rx_u)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_tx_GR * d_tx_s)/Lambda_0) * math.exp(complex(0, 1)*2*math.pi*(r_rx_GR* v_)/Lambda_0)



H_u_s_LOS_τ_t = math.sqrt(1/(K_Umi_LOS+1))*H_u_s_NGR_τ_τ_LOS_t + math.sqrt(K_Umi_LOS/(K_Umi_LOS+1))*(H_u_s_1_LOS_t*delta_τ(τ_n[0]-τ_LOS) + d_3D/d_GR * H_u_s_GR_t*delta_τ(τ-τ_GR))





if __name__=='__main__':
    pass