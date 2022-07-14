#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   O2I_car_penetration_loss.py
@Time    :   2022/06/13
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math
import cmath


c = 3.0*100000000 # speed of the llght

# PL_b is the basic outdoor path loss , choose proper Pathloss channelmodel in directory 'Pathloss' 
def PL_O2I_car_penetration_loss(PL_b):
    
    N = np.random.normal(9, 25, 1)  #Normal distribution  or called Gaussian distribution
    PL_O2I_car = PL_b + N

    return PL_O2I_car




#Note:	 μ = 9, and σP = 5.  The O2I car penetration loss models are applicable for at least 0.6-60 GHz. 
    
    

if __name__=='__main__':
    pass