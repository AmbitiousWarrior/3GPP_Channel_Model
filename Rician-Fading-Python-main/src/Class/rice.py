# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:55:46 2020
@author: Jonathan Browning
"""
import numpy as np
from scipy.stats import gaussian_kde as kdf
from scipy import special as sp

class Rice:
    numSamples = 2*(10**6)  # the number of samples used in the simulation
    r = np.linspace(0, 6, 6000) # theoretical envelope PDF x axes
    theta = np.linspace(-np.pi, np.pi, 6000)    # theoretical phase PDF x axes
    
    def __init__(self, K, r_hat_2, phi):       
        # user input checks and assigns value  检查输入是否合理
        self.K = self.input_Check(K, "K", 0, 50)
        self.r_hat_2 = self.input_Check(r_hat_2, "\hat{r}^2", 0.5, 2.5)  
        self.phi = self.input_Check(phi, "\phi", -np.pi, np.pi)
        
        # simulating and theri densities    模拟值及其发布密度
        self.multipathFading = self.complex_Multipath_Fading()
        self.xdataEnv, self.ydataEnv = self.envelope_Density()
        self.xdataPh, self.ydataPh = self.phase_Density()
        
        # theoretical PDFs calculated    计算理论PDF 概率分布函数（Probability Distribution Function） or 概率密度函数（Probability Density Function）
        self.envelopeProbability = self.envelope_PDF()
        self.phaseProbability = self.phase_PDF()

    def input_Check(self, data, inputName, lower, upper):
        # input_Check checks the user inputs  输入检查
        
        # has a value been entered
        if data == "":
            raise ValueError(" ".join((inputName, "must have a numeric value")))
        
        # incase of an non-numeric input 
        try:
            data = float(data)
        except:    
            raise ValueError(" ".join((inputName, "must have a numeric value")))
    
        # data must be within the range
        if data < lower or data > upper:
            raise ValueError(" ".join((inputName, f"must be in the range [{lower:.2f}, {upper:.2f}]")))
        
        return data

    def calculate_Means(self):
        # calculate_means calculates the means of the complex Gaussians representing the
        # in-phase and quadrature components    计算表示同相分量和正交分量的复高斯的平均值
        # 按照惯例，在正交处理中，频谱的实部被叫做同相分量，虚部被叫做正交分量
        p = np.sqrt(self.K * self.r_hat_2 / (1+self.K)) * np.cos(self.phi)
        q = np.sqrt(self.K * self.r_hat_2 / (1+self.K)) * np.sin(self.phi)
       
        return p, q
    
    def scattered_Component(self):
        # scattered_Component calculates the power of the scattered signal component  计算散射信号分量的功率
        # 并且由此可知r_hat_2-2*sigma*sigma = s*s，因此r_hat_2为总接收功率，2*sigma*sigma为NLOS多径分量的平均功率，s*s为LOS分量的功率！！！！！！！！！！！！！
        sigma = np.sqrt(self.r_hat_2 / ( 2 * (1+self.K) ) )    
        return sigma
    
    def generate_Gaussians(self, mean, sigma):
        # generate_Gaussians generates the Gaussian random variables  生成高斯随机变量
        
        gaussians = np.random.default_rng().normal(mean, sigma, self.numSamples)
        
        return gaussians
    
    def complex_Multipath_Fading(self):
        # complex_Multipath_Fading generates the complex fading random variables  产生复杂的衰落随机变量
        
        p, q = self.calculate_Means()
        sigma = self.scattered_Component()
        multipathFading = self.generate_Gaussians(p, sigma) + (1j*self.generate_Gaussians(q, sigma))
        
        return multipathFading
    
    def envelope_PDF(self):
        # envelope_PDF calculates the theoretical envelope PDF  计算理论莱斯分布
        
        PDF = 2 * (1+self.K) * self.r / self.r_hat_2 \
            * np.exp(- self.K - ((1+self.K)*self.r**2)/self.r_hat_2) \
            * np.i0(2 * self.r * np.sqrt(self.K*(1+self.K)/self.r_hat_2))
            
        return PDF

    def phase_PDF(self):
        # phase_PDF calculates the theoretical phase PDF  计算理论莱斯相位分布
        
        def q_func(x):
        # Q-function       
            return 0.5-0.5*sp.erf(x/np.sqrt(2))     
        
        PDF = (1/(2*np.pi))* np.exp(- self.K) * (1 + (np.sqrt(4*np.pi*self.K) \
              * np.exp(self.K * (np.cos(self.theta-self.phi))**2) *np.cos(self.theta-self.phi)) \
              * (1 - q_func(np.sqrt(2*self.K) * np.cos(self.theta-self.phi))))
        
        return PDF
        
    
    def envelope_Density(self):
        # envelope_Density finds the envelope PDF of the simulated random variables  求模拟随机变量的包络PDF
        
        R = np.sqrt((np.real(self.multipathFading))**2 + (np.imag(self.multipathFading))**2)
        kde = kdf(R)
        x = np.linspace(R.min(), R.max(), 100)
        p = kde(x)
        
        return x, p
    
    def phase_Density(self):
        # phase_Density finds the phase PDF of the simulated random variables   求模拟随机变量的相位PDF
          
        R = np.angle(self.multipathFading)
        kde = kdf(R)
        x = np.linspace(R.min(), R.max(), 100)
        p = kde(x)
        
        return x, p
   



#先由  scattered_Component 计算得到平均sigma  再由generate_Gaussians得到基于平均sigma 的高斯分布，因为无线信道的多径分布规律为高斯分布
#其实 K 为莱斯因子   r_hat_2为平均小尺寸衰落幅值   phi应该是为了计算基于相位的莱斯分布（继续研究），while   r_hat_2基于幅值  nice！！！！