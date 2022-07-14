# Rician-Fading-Python

The Rician fading model implemented in python. Plots the theoretical and simulated, envelope and phase porbability density functions (PDFs)

The Rician fading model describes the small-scale fading ocurring between and transmitter and receiver antenna pair, where a scattered and dominant signal components exist.
A special case of this model is Rayleigh fading, when only a scattered signal component exists. This is represented by K = 0.

This project uses PySimpleGUI, numpy, scipy, matplotlib and tkinter.

This project was developed on a windows OS, using Spyder IDE with Python 3.8. All the dependencies where installed by anaconda.

The input K accepts values in the range 0 to 50.
The input \hat{r}^{2} accepts values in the range 0.5 to 2.5.
The input \phi accepts values in the range -pi to pi.

Runing main.py to start the GUI displays:
  
![ScreenShot](https://raw.github.com/Jonathan-Browning/Rician-Fading-Python/main/docs/Initial_window.png)

Entering values for the Rician K factor, the root mean sqaure of the signal \hat{r}(the input is the squared value), and \phi the phase parameter:

![ScreenShot](https://raw.github.com/Jonathan-Browning/Rician-Fading-Python/main/docs/Enter_inputs.png)

The theoretical evenlope PDF and phase PDFs are plotted to compare with the simulation and gives the execution time for the theoretical calculations and simulations together:

![ScreenShot](https://raw.github.com/Jonathan-Browning/Rician-Fading-Python/main/docs/Result.png)
