#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   PhysicalLayer2ApplicationLayer_channelmodel.py
@Time    :   2023/04/03
@Author  :   LuDaYong
@Version :   1.0
@parameter: 
'''

#Latency time and PRR(Packet Reception Ratio) will be the ultimate goals.


import numpy as np
import math
import cmath
import random
import operator


c = 3.0*100000000 # speed of the llght

#基础参数配置：





#在这里设置用于无线传输的资源  帧 frame 10ms; 子帧 subframe 1ms; 时隙 slot
def get_Numerologies(μ): #获取无线传输物理层参数集  μ可取 0 1 2 3 4 
    N_slot_symbol = 14                    #一个时隙对应多少个OFDM符号(理论上OFDM符号持续时间即为码元持续时间Ts = 1/delt_f,例如μ=0时，delt_f=15kHz，subframe中有1个slot,包含14个时隙，一个OFDM符号持续时间应该为1/15ms,理论上可包含15个时隙，但考虑保护间隔，保留14个OFDM符号)
    N_frame_μ_slot = 10*math.pow(2,μ)     #frame中有几个slot
    N_subframe_μ_slot = 1*math.pow(2,μ)   #subframe中有几个slot
    
    delt_f = math.pow(2,μ)*15             #子载波间隔 kHz  可能值：15  30  60  120  240 对应时隙值1 0.5 0.25 0.125 0.0625ms  即(1000 500 250 125 62.5us)/slot
    slot_time = 1/delt_f                  #理论OFDM符号持续时间（码元持续时间） 单位 毫秒ms
    return N_slot_symbol,N_frame_μ_slot,N_subframe_μ_slot,delt_f

#OFDM符号:一个时隙内的OFDM符号的数量是固定的，有14个OFDM符号 (常规CP)
#一个OFDM符号至少可以承载1bit数据的信息（具体看调制方式：例如：256(2的8次方)QAM对应8bit）
#时隙长度因为子载波间隔不同会有所不同，随着子载波间隔变大，时隙长度变小 见图1 (个人见解，μ不同，但时频MAP上每个slot所占的面积都是相同的，即OFDM符号所占时频资源也可看做相同)
#时隙slot越短，越适用于5G低延时的要求（其实也就是μ越大，子载波间隔越大，对低延时越有益）

#RE(Resource Element): 频率一个子载波及时域上一个OFDM symbol(即 OS), 物理资源上最小最基本的单位 见图2
#RB(Resource Block)：频域上连续的12个子载波，并没有对RB的时域进行定义 见图3

#FR1(5G主频段) Sub6G 450~6000MHz    FR2(5G扩展频段) 毫米波 24250~52600MHz    

#SSB介绍 (Synchronization Signal ar PBCH Block) 同与信号和物理广播信道块  见图4 



def Wireless_Resource_Configure():
    
    
    
    pass 




#关于延时，目前主要考虑 TTI（Transmission Time Interval：动态调度资源的基本时间单位，暂定为整数ms）、SDS（sub-carrier space：子载波间隔）、多次HARQ重传 
def Latency_time_Calculate (now_time,TTI,SDS,slot_time,tx_time):
    circulation = int(now_time/TTI) + 1   #第几个TTI周期  now_time从0时刻开始，最小度量为1ms，以1递加；
    wait_to_send_time = int(tx_time)%TTI  #因TTI导致的延时
    
    
    latency_for_SDS = 2 * slot_time       #暂定两个码元的持续时间
    
    
    latency_time = wait_to_send_time + latency_for_SDS + 1
    return latency_time

def Latency_time_Calculate_2 (now_time,TTI,SDS,slot_time,tx_time, wireless_resource_condition, ):
    circulation = int(now_time/TTI) + 1   #第几个TTI周期  now_time从0时刻开始，最小度量为0.1ms，以0.1递加；
    wait_to_send_time = int(tx_time)%TTI  #因TTI导致的延时
    
    
    latency_for_SDS = 2 * slot_time       #暂定两个码元的持续时间
    
    
    latency_time = wait_to_send_time + latency_for_SDS + 1
    return latency_time
 
 
def get_wireless_resource_condition(UE_num, now_time,TTI, resource_configuration):  #生成无线资源占用情况
    wireless_resource_condition = []
    for i in range(UE_num):
        generate_time = random.uniform(0,TTI)
        PHY_packet_size = random.random(200,30000)
        level = random.random(1,3)
        #  https://www.bilibili.com/read/cv19032869?spm_id_from=333.999.0.0
        PHY_packet_id = i*10000 + now_time #UE的发送信息的编号
        wireless_resource_condition.append({'UE_id':i+1,'level':level, 'generate_time':generate_time, 'PHY_packet_id':PHY_packet_id,'PHY_packet_size':PHY_packet_size})
    
    return wireless_resource_condition
    
    
def wireless_resource_configuration(total_resources,UE_num,base_single_resource_size):  #返回各UE分配到的资源
    resource_configuration = []
    for i in range(UE_num):
        average_single_resource = total_resources/UE_num
        if base_single_resource_size < average_single_resource:
            resources_acquired = base_single_resource_size
            resource_configuration.append({'id':i, 'resources_acquired':resources_acquired})
        else:
            resources_acquired = average_single_resource
            resource_configuration.append({'id':i, 'resources_acquired':resources_acquired})
    return resource_configuration 
   

#   为每个UE预保留固定资源，又允许高等级信息调用其他UE资源 https://zhuanlan.zhihu.com/p/582447543   
#   Mode 1：基站调度UE用于sidelink传输的sidelink资源
#   Mode 2: UE确定（即基站不调度）由网络配置的sidelink资源或预配置的sidelink传输资源 
 
#关于丢包，目前主要考虑 SNR (信噪比)、重传机制
#考虑直接使用天线接收信号强度阈（dB）,低于其值，则算丢包 。2023 10 11
#https://support.huawei.com/enterprise/zh/doc/EDOC1000113314/ad382ac7
# def PRR_Calculate (SNR,RT_Parameters): # d_2D_out,d_2D,f_c,h_BS = 25,h_UT = 1.5,h = 5,W = 20
def PRR_Calculate(Antenna_recv_threshold_value,Antenna_send_power_value,Antenna_send_gain,Antenna_recv_gain,fast_fading_model_vaule):   #2023 10 11
    if Antenna_send_power_value + Antenna_send_gain + Antenna_recv_gain + fast_fading_model_vaule>Antenna_recv_threshold_value:
        PRR = 1
    else:
        PRR = 0

    return PRR




#Note:	The LOS probability is derived with assuming antenna heights of 3m for indoor, 10m for UMi, and 25m for UMa
    
    

if __name__=='__main__':
    SDS = 30        #kHz
    TTI = 1         #调度周期 子帧切换速度（LTE TTI=1ms）https://zhuanlan.zhihu.com/p/440684294
    
    
    # 天线模型（暂时以参数输入的方式确定天线仿真结果）https://support.huawei.com/enterprise/zh/doc/EDOC1000113314/c3242b10   https://support.huawei.com/enterprise/zh/doc/EDOC1000113314/b4231b86
    Antenna_recv_threshold_value = -65      #天线接收信号强度阈值 单位 dB  接收端只能接收识别一定阈值以上信号强度的无线信号
    Antenna_send_power_value = 30           #天线对接收对象的发送信号强度 单位 dB
    Antenna_send_gain = 6                   #发射端天线增益 单位 dB 
    Antenna_recv_gain = 0                   #接收端天线增益 单位 dB 
    
    
    
    

    UE_num = 20     # + random.random(-3,3) #当前场景有多少个对象
    modulation_type = '256_QAM'     #调制方式：例如：256(2的8次方)QAM对应8bit
    modulation_result = {'128_QAM':4, '256_QAM':8}
    total_resources = 10000 * modulation_result['256_QAM']    #每毫秒可用于传输的OFDM符号数量 (例如：UE_num的default值为20)
    base_single_resource_size = 30000   #由实际V2X数据包大小PHY_packet_size = random.random(200,30000)、决定 

    result = [] #Fast_fading_model_with_addtional_modeling_components的计算结果
    fast_fading_model_vaule = result
    Latency_time_Calculate_2()
    PRR_Calculate(Antenna_recv_threshold_value,Antenna_send_power_value,Antenna_send_gain,Antenna_recv_gain,fast_fading_model_vaule)
    
    current_send_resources_zise = []        #当前时刻发送的bits数量
    current_resources_left = []             #当前时刻剩余资源
    current_PHY_packet_left_to_send = []    #当前时刻剩余待发送bits
    total_PHY_packet_sent = []              #当前时刻剩余待发送bits
    
    for i in range(1000): # i即为时间 单位 1ms（即为TTI）   仿真1秒时间内的丢包、延时情况
        now_time = i
        resource_configuration = wireless_resource_configuration(total_resources, UE_num, base_single_resource_size)
        wireless_resource_condition = get_wireless_resource_condition(UE_num, now_time, TTI, resource_configuration)
        total_PHY_packet_size = 0
        
        # current_send_resources_zise.append(0)           #初始时刻，未发送bits
        # current_resources_left.append(80000)            #初始时刻，还没有UE调用无线资源
        # current_PHY_packet_left_to_send.append(0)       #初始时刻，无剩余待发送bit
        
        current_send_resources_zise.append(0)           #初始时刻，未发送bits
        current_resources_left.append(80000)            #初始时刻，还没有UE调用无线资源
        current_PHY_packet_left_to_send.append(0)       #初始时刻，无剩余待发送bit
        
        wireless_resource_condition  = wireless_resource_condition + current_PHY_packet_left_to_send  #将剩余的包加回到当前队列
        sorted(wireless_resource_condition, key = operator.itemgetter('level'))     #按level升序排列
        #{'UE_id':i+1,'level':level, 'generate_time':generate_time, 'PHY_packet_id':PHY_packet_id,'PHY_packet_size':PHY_packet_size}
        PHY_packet_size_list = []
        PHY_packet_size_accumulation = []
        
        # 依次累加当前时刻的各 UE 的 PHY_packet_size
        for i in range(len(wireless_resource_condition)):     
            PHY_packet_size_list.append(wireless_resource_condition[i]['PHY_packet_size'])
        for i in range(len(PHY_packet_size_list)): 
            PHY_packet_size_accumulation.append(sum(PHY_packet_size_list[:i]))
            
        # for UE_attributes in wireless_resource_condition: 
        #     total_PHY_packet_size += UE_attributes['PHY_packet_size']
        for i in range(len(PHY_packet_size_accumulation)): 
            if PHY_packet_size_accumulation[i] > total_resources:
                current_PHY_packet_left_to_send.append(wireless_resource_condition[i])
            else:
                PHY_packet_size_accumulation[i]['send_time'] = i
                total_PHY_packet_sent.append(PHY_packet_size_accumulation[i])           #所有已发送的数据包的集合，用于后分析，得出latency等数据 
                
            
            

    
    # 资源在时域与频域上同时划分，最小调度周期为TTI，不同的UE有不同的TTI周期起点（但暂时假设周期起点按规律分布，例如UE1在0时刻开始，UE2在0+TTI开始）




#Link level simulation assumptions 链路级模拟假设必须包含的考量因数
'''
- Carrier frequency                                                     载波频率    1
- Channel model (e.g. fast fading model)                                信道模型（例如快速衰落模型）    1
- PHY packet size                                                       物理包大小  1
- Channel codes (for control and data channels)                         信道编码
- Modulation and code rates (for control and data channels)             调制与编码率
- Signal waveform (for control and data channels)                       信号波形
- Subcarrier Spacing                                                    子载波间隔  1
- CP length                                                             循环前缀长度
- Frequency synchronization error                                       频率同步误差
- Time synchronization error                                            时间同步误差
- Channel estimation (e.g. DMRS pattern and symbol location)            信道估计(DeModulation Reference Signal)解调参考信号样式与符号位置
- Number of retransmission and combining (if applied)                   重传次数与组合
- Number of antennas (at UE and BS)                                     天线数量
- Transmission diversity scheme (if applied)                            传输分集方案
- UE receiver algorithm                                                 用户设备接收器算法
- AGC settling time and guard period                                    自适应增益稳定时间和保护期
- EVM (at TX and RX)                                                    误差矢量幅度
'''


# 确定场景 单播、组播、广播
# 确定总的信道资源与单个UE所分配到的信道资源
# 确定单个UE所分配得到的资源中有多少可用于发送具体数据（除去循环前缀、SSB、PSB、保护空字符等）
# 确定最小调度周期
# 确定
# https://www.researchgate.net/figure/Link-level-simulation-assumptions_tbl1_257879590
# https://ww2.mathworks.cn/help/comm/link-level-simulation.html