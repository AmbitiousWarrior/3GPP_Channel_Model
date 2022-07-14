#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Time-varying_Doppler_shift.py  时变多普勒频移
@Time    :   2022/06/27
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math
import scipy.integrate
from numpy import exp


# hard to calculate the r_rx_n_m_t[i*M+j]  and   v_t  很难获取实时的r_rx_n_m_t[i*M+j] 与 v_t 并将他们矢量相乘求积分  暂时放弃

f = lambda t:r_rx_n_m_t[i*M+j] * v_t
i = scipy.integrate.quad(f, 0, t_now)  #http://t.zoukankan.com/huanghanyu-p-13170521.html


#方程(7.5-22)仅对时不变多普勒频移成立
math.exp(complex(0, 1)*2*math.pi*   (r_rx_n_m_t[i*M+j] * v_t)   /Lambda_0)







if __name__=='__main__':
    pass