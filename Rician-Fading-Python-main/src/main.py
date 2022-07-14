# -*- coding: utf-8 -*-
"""
@author: Jonathan Browning   https://github.com/Jonathan-Browning/Rician-Fading-Python
"""
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import time
from Class.rice import Rice
from tkinter import messagebox
import os

def draw_envelope(data):
    plotname = "envelope_plot.png"
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure(1)
    plt.xlabel(r"$r$", fontsize=18)
    plt.ylabel(r"$f_{R}(r)$", fontsize=18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18) 
    plt.xlim((0, 6))
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.tick_params(direction='in')
    plt.plot(data.r, data.envelopeProbability, "k", label='Theoretical')  
    plt.plot(data.xdataEnv[1:len(data.xdataEnv):2], data.ydataEnv[1:len(data.ydataEnv):2], "k.", label='Simulation') 
    leg = plt.legend(fontsize=15)
    leg.get_frame().set_edgecolor('k')
    plt.savefig(plotname)
    plt.close(1)
    return plotname

def draw_phase(s):
    plotname = "phase_plot.png"
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure(1)
    plt.xlabel(r'$\theta$', fontsize=18)
    plt.ylabel(r'$f_{\Theta}(\theta)$', fontsize=18)
    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
                [r'$-\pi$',r'$-\pi/2$',r'$0$',r'$\pi/2$',r'$\pi$'],
                fontsize = 18)
    plt.yticks(fontsize = 18) 
    plt.xlim((-np.pi, np.pi))
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.tick_params(direction='in')    
    plt.plot(s.theta, s.phaseProbability, "k", label='Theoretical')  
    plt.plot(s.xdataPh[1:len(s.xdataPh):2], s.ydataPh[1:len(s.ydataPh):2], "k.", label='Simulation')  
    leg = plt.legend(fontsize=15)
    leg.get_frame().set_edgecolor('k')
    plt.savefig(plotname)
    plt.close(1)
    return plotname
    
def main():   
        
    # Setting up window layout
    layout = [[sg.Text(r'Please enter K, \hat{r}^2 and \phi', font='Helvetica 18')],      
          [sg.Text("K:", size=(8, 1), font='Helvetica 18'), sg.Input(key='-K', size=(5, 1), font='Helvetica 18')],      
          [sg.Text(r"\hat{r}^2:", size=(8, 1), font='Helvetica 18'), sg.Input(key=r'-\hat{r}^2', size=(5, 1), font='Helvetica 18')],      
          [sg.Text("\phi:", size=(8, 1), font='Helvetica 18'), sg.Input(key=r'-\phi', size=(5, 1), font='Helvetica 18')],      
          [sg.Button('Calculate', font='Helvetica 18'), sg.Exit(font='Helvetica 18')],
          [sg.Text("Time (s):", size=(8, 1), font='Helvetica 18'), sg.Txt('', size=(8,1), key='output')],
          [sg.Image(key='-Image1')],
          [sg.Image(key='-Image2')]]
        
    window = sg.Window("The Rician fading model", layout, finalize=True, font='Helvetica 18')

    # The Event Loop                 
    while True:
        # Reading user inputs
        event, values = window.read() 
        
        # Close if the exist button is pressed or the X
        if event in (sg.WIN_CLOSED, 'Exit'):
            break      
        
        # Rice class instance which calculates everything and time the exeuction
        start = time.time()
        try:
            s = Rice(values['-K'], values['-\hat{r}^2'], values['-\phi'])
        except Exception as e:  # displays the error message and will force the program to close
            messagebox.showerror("Error", e)
            continue
        end = time.time()
        
        # update the execution time
        exeTime = round(end - start, 4) # Roudn to 4 decimal places
        window['output'].update(exeTime)  # Display the execution time 
        
        # drawing the figures
        imageFileName1 = draw_envelope(s)
        window.Element('-Image1').Update(imageFileName1)
        os.remove(imageFileName1) # need to remove the image file again
        
        imageFileName2 = draw_phase(s)
        window.Element('-Image2').Update(imageFileName2)
        os.remove(imageFileName2) # need to remove the image file again

    window.close()
    
if __name__ == "__main__":
    main()