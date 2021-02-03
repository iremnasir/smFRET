import numpy as np
from pylab import *
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.mlab as mlab
from lmfit import Model


#Script for simulating shot noise based histograms. 
#Idea taken from Deniz et.al. PNAS 1999
#The emissions of both fluoropohores (Ia and Id) exhibit Poisson distributions,
#with mean values that depend on the excitation intensity and the photophysical
#characteristics of the dyes. For these low signals, the relative fluctuations,
#equal to the inverse of the square root of the mean value, play a 
#significant role. This results in fluctuations in the ratio E = Ia/(Ia + Id), 
#which put an intrinsic limit on the separation resolution that can be achieved by using 
#this approach. To evaluate this limit, a simple model was used in which both emission 
#channels Ia and Id are described by Poisson variables. 

#Their mean values are ES and (1-E)S, respectively, where E is the mean transfer 
#efficiency and S is the sum of the signals in both channels. 
#In practice, the shot noise is calculated for S taken equal to the threshold T. 
#Because only signals above this threshold are processed, 
#they have a smaller relative shot noise, and this places an upper bound on the 
#calculated values. 


#function form
def shotnoise(E,S):
	Ia_m = E*S #distribution mean for acceptor E= fret eff. S = tot # of photons
	Id_m = (1-E)*S #distribution mean for donor
	I_a = np.random.poisson(Ia_m, 1000) #create number of data (second arg) of poisson 
	#dist centered at first arg
	I_d = np.random.poisson(Id_m, 1000)
	Ia = np.array(I_a,dtype = float) #convert them to arrays. otherwise division spits zeros
	Id = np.array(I_d,dtype = float)
	sum = Ia+Id
	return np.divide(Ia, sum) #def of FRET efficiency

#define values
E1 =0.38
S1=50
E2=.40
S2=50
Esim1 = shotnoise(E1,S1)
np.savetxt('FRET.txt', Esim1, "%.2f")
Esim2 = shotnoise(E2,S2)

# 
# #plot
plt.hist(Esim1, 42, normed = True, color = 'green', alpha = .5, label = str(S1) +'photons')
plt.hist(Esim2, 42, normed = True, color = 'blue', alpha = 0.5, label = str(S2) +'photons')
plt.legend()
plt.xlabel('$E_{FRET}$')
plt.ylabel('Normalized Probability')
plt.xlim(0,1)
plt.show()


