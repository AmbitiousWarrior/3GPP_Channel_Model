#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Dual_mobility.py
@Time    :   2022/06/29
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import math
import numpy as np



r_rx_avg = np.array([math.sin(math.radians(θ_v_rx))*math.cos(math.radians(φ_v_rx)),math.sin(math.radians(θ_v_rx))*math.sin(math.radians(φ_v_rx)),math.cos(math.radians(θ_v_rx))])

r_tx_avg = np.array([math.sin(math.radians(θ_v_tx))*math.cos(math.radians(φ_v_tx)),math.sin(math.radians(θ_v_tx))*math.sin(math.radians(φ_v_tx)),math.cos(math.radians(θ_v_tx))])




r_rx_n_m = []      
r_tx_n_m = []        
v_n_m = [] 
a_n_m = []  #random variable from -v_scatt to v_scatt( TODO 命名上来看：散射体的速度 还是说明： 最大杂波速度  the maximum speed of the clutter),
D_n_m = []  #a random variable of Bernoulli distribution with mean p, and v_scatt is the maximum speed of the clutter  A typical value of p is 0.2


#For the LOS path, the Doppler frequency

for i in range(N):
    for j in range(M):
        v_n_m.append( (r_rx_n_m[i*M+j]*r_rx_avg + r_tx_n_m[i*M+j]*r_tx_avg)/Lambda_0  )
        a_n_m.append(np.random.uniform(-v_scatt, v_scatt))
        D_n_m.append(np.random.binomial(1, 0.2, 1))
        
        
#For all other paths, the Doppler frequency component
for i in range(N):
    for j in range(M):
        v_n_m.append( (r_rx_n_m[i*M+j]*r_rx_avg + r_tx_n_m[i*M+j]*r_tx_avg + 2*a_n_m[i*M+j]*D_n_m[i*M+j] )/Lambda_0  )


if __name__=='__main__':
    pass