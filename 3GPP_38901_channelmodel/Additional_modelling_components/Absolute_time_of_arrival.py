#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Absolute_time_of_arrival.py
@Time    :   2022/06/29
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


μ_lg_delt_τ = -7.5
sigma_lg_delt_τ = 0.4
lg_delt_τ = np.random.normal(μ_lg_delt_τ, sigma_lg_delt_τ, 1)


Correlation_distance_in_the_horizontal_plane = 6    # InF-SL, InF-DL[m]
Correlation_distance_in_the_horizontal_plane = 11   # InF-SH, InF-DH

delta_t = math.pow( lg_delt_τ ,10)



if __name__=='__main__':
    pass