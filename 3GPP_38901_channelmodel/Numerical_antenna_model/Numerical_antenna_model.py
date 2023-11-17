#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Numerical_antenna_model.py
@Time    :   2023/11/16
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''
# 以局部三维笛卡尔坐标系为基准，计算RSU与OBU之间的角度关
# 对天线三维空间内的发送信号强度，直接以预设数值替代（例如MIMO、波束赋型的增益直接在数值上体现————数值模型）

import numpy as np
import math
import cmath


c = 3.0*100000000 # speed of the llght

#LOS probability (distance is in meters)
def Get_angels(point1,point2, consider_building_occlusion):
    x1,y1,z1 = point1
    x2,y2,z2 = point2

    if consider_building_occlusion:  #考虑建筑物遮挡
        
        pass
    else:
        ZOD = math.acos((z2-z1)/math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1),0.5)) /math.pi*180
        ZOA = math.acos((z1-z2)/math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1),0.5)) /math.pi*180
        # AOA = math.acos((x2-x1)/math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1),0.5)) /math.pi*180
        # ZOA = math.acos((x1-x2)/math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1),0.5)) /math.pi*180
        # 应该是三维向量在水平面上的投影与X轴的夹角，而不是三维向量与X轴的夹角
        AOD = math.acos((x2-x1)/math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1),0.5)) /math.pi*180
        AOA = math.acos((x1-x2)/math.pow((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1),0.5)) /math.pi*180
        
        
    return AOD,AOA,ZOD,ZOA
 
def  Transmitted_signal_strength():
    transmitted_signal_strength = 10  #单位 Db
    return transmitted_signal_strength

if __name__=='__main__':
    pass