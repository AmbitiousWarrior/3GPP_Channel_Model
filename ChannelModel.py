#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ChannelModel.py
@Time    :   2022/05/13
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''


import numpy as np
import math
import cmath

# The Friis Transmission Equation (弗里斯传输公式理论计算)  %distance:km  freq:MHz
# https://zhuanlan.zhihu.com/p/386225442  https://blog.csdn.net/JiGuang1107/article/details/119382411
def Friis_Transmission_Model_Loss(dist,fre,Gt=2.15,Gr=2.15):
    distance=dist/1e3
    freq=fre/1e6
    Loss_dB=-32.44-20*math.log10(distance)-20*math.log10(freq)+Gt+Gr #Pr(dBm = Pt - Loss_dB)
    #Loss_dB=-20*math.log10(4*math.p1*distance*freq)+Gt+Gr  #Another form
    return Loss_dB

#简化双径模型   详见 博士学位论文：车对路边单元的无线信道测量与建模研究  第三章
#ht:发送天线高度(m) hr:接收天线高度(m)  ds:收发两者地面直线距离(m)
def Two_Ray_Ground_Reflection_Transmission_Simple_Model_Loss(ds,ht,hr,G=2.15):
    Loss_dB=-40*math.log10(ds)+10*math.log10(G)-20*math.log10(ht*hr)
    return Loss_dB


#精确双径模型   详见 博士学位论文：车对路边单元的无线信道测量与建模研究 第三章
#d1+d2:反射路径的距离(m) α:反射路径与地面的夹角(m)  发送天线高度(m) hr:接收天线高度(m)    pow(144, 0.5)
#ds:收发两者地面直线距离(m)  ε epsilon：介电常数  Rgf:地面反射因子
def Two_Ray_Ground_Reflection_Transmission_Accuate_Model_Loss(wave_longth,d1,d2,ds,ht,hr,epsilon,Gl=2.15,Gr=2.15):
    cos_a = ds/(d1+d2)
    sin_a = (ht+hr)/(d1+d2)
    Rgf = (sin_a-pow(epsilon-cos_a*cos_a,0.5))/(sin_a+pow(epsilon-cos_a*cos_a,0.5))
    data_phase = 4*math.pi*ht*hr/(wave_longth*ds)#d->ds?
    Loss_dB=-20*math.log10(4*math.pi/wave_longth)+20*math.log10(abs(pow(Gl,0.5)/wave_longth)+Rgf*pow(Gr,0.5)*(math.log((complex(0,0-data_phase))))/((d1+d2)))
    return Loss_dB

#V2I场景中 主要原因为树木遮挡造成的额外损耗计算公式  
#详见 博士学位论文：车对路边单元的无线信道测量与建模研究 第三章
#n：树木的数量  f:工作频率 MHz   Ltc:树冠长度    d:车辆行驶的距离     ht:车辆高度   hr:rsu高度    
#wr:车距路边的宽度   wh:树冠宽度的半数   wto:RSU与第一棵树的距离   wtt:相邻树之间的距离
def V2I_Foliage_Extra_Loss(n,f,Ltc,d,ht,hr,wr,wh,wto,wtt,A=0.2,B=0.3,C=0.6):#ABC由经验模型ITU-R模型拟合所得
    if n%2==0:
        d_ir = n/2*Ltc*((pow((ht+hr)*(ht+hr)+wr*wr+d*d)),0.5)+(pow((hr-ht)*(hr-ht)+wr*wr+d*d),0.5)/d  #d_ir单位为m
    else:       
        d_ir = (wh/wr*d-wto-(n-1)/2*wtt)*((pow((ht+hr)*(ht+hr)+wr*wr+d*d)),0.5)+(pow((hr-ht)*(hr-ht)+wr*wr+d*d),0.5)/d
    Loss_dB=A*pow(f,B)*pow(d_ir,C)
    return Loss_dB


#V2I场景中 主要原因为树木遮挡造成的大尺度衰落（第三章采用确定性方法分析V2I路径损耗，模型复杂，计算量大，且有应用范围限制）
#本模型为基于几何特征的统计模型  详见 博士学位论文：车对路边单元的无线信道测量与建模研究 第四章
#最常用的统计模型为基于距离的对数路径损耗模型  PL_d= PL_d0 + 10nlog10()d/d0 + X(X为大尺度阴影衰落分量)
def Log_Distance_Path_Loss_Model(link_type,H):
    if link_type == 'LOS-B':
        n = 0.5743*H + 3.389/H - 1.012
        # X ~ N (0.533,0.497)
    if link_type == 'NLOSF':
        n = 0.44808*H + 0.43814    
        # X ~ N (0.124,2.865)
    if link_type == 'LOS-A':
        n = -0.02849*H*H + 0.51577*H + 0.63977
        # X ~ N (0.6,0.78)
    return n


#https://github.com/Jonathan-Browning/Rician-Fading-Python   https://blog.csdn.net/weixin_45662974/article/details/115361895
#V2I场景中基于距离的莱斯K因子被建模为下面的式子  K = 8.948 - 0.026d



if __name__=='__main__':
    pass