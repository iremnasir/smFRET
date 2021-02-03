import numpy as np
from pylab import *
from sys import argv
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import csv
from scipy.optimize import curve_fit
name = argv[1] # name of .dat file

namelist = argv[1:]

def EFRET(name):
	#read tsv data with the argument taken from user
	data_file = np.loadtxt(name, delimiter='\t')
	raw = data_file[:,:]

	#calculate the average of each column - background
	#IMPORTANT!! THIS DEPENDS ON HOW APDS ARE HOOKED
	avgc1 = np.mean((raw[:,0]), dtype=float) #F3 acceptor
	avgc2 = np.mean((raw[:,1]), dtype = float) #F2 donor
	avgc3 = np.mean((raw[:,2]), dtype = float) #F1 donor #2

	print avgc1 #acceptor
	print avgc2 #donor1
	print avgc3 #donor2

	#Columns are subject to change. Depends on how you hook the APDs
	Donor_raw = raw[:,1]
	Acceptor_raw = raw[:,0]
	Donor2_raw = raw[:,2]

	#This is for time stamp purposes
	index_nr = len(Donor_raw)
	index_array = np.arange(index_nr)

	#plot raw trace - Very heavy
	#f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
	#ax1.plot(index_array, Donor_raw)
	#ax2.plot(index_array, Acceptor_raw)
	#ax3.plot(index_array, Coincident_raw)
	#plt.show()

	#calculate how long the data is collected

	Time = 0.5*(len(Donor_raw)-1)
	print Time

	#Subtract bg - Subject to change depending on how APDs are hooked
	D = (Donor_raw - avgc2)
	A = Acceptor_raw - avgc1
	D2 = Donor2_raw - avgc3

	#Optional - Save it
	#np.savetxt('backg.txt', (Donor, Acceptor), "%.2f", delimiter='\t') #test

	#Define Leakage & Direct Excitation
	#l1= 0.06#   #C to D
	l2=	0.07# #D to A
	#l3=	0.0#C to A
	#d1=	0.015##C to D
	d2=	0.01##D to A
	#d3=	0.0#C to A


	#Total Donor for Beam Splitter Case
	DonTot = D + D2
	#Intensity Definition 
	# *****Two color*****
	I_D = DonTot/(1-l2)
	I_A = (A - (l2 * A) - (l2 * DonTot) - (d2 * DonTot))/ (1 +d2 - (l2*d2) - l2)

	Tot1 = I_D+I_A
	#Lower Thresholding for E
	TFRET = 40
	U = 250

	#For 2 color only
	I_Dt = I_D[np.logical_and(Tot1>TFRET, Tot1<U)]
	I_At = I_A[np.logical_and(Tot1>TFRET, Tot1<U)]

	print np.mean(I_Dt)
	print np.mean(I_At)


	# FRET Efficiency
	E = I_At / (I_Dt + I_At)
	print len(E)
	
	#Saving E
	np.savetxt('EFRET.txt', E, '%.2f', delimiter='\t')
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# plt.scatter(I_Dtt, I_Ctt)
	# plt.savefig("/Users/iremnasir/Google Drive/DenizLabData/Coincidence Trials/160809/Scatter_A8_2_200pM_dichr5.pdf", dpi=600)
	# 
	# # #Coincidence
	#S = I_Ctt / (I_Dtt+I_Ctt+I_Att)
	#np.savetxt('Coincidence.txt', S, '%.2f', delimiter='\t')
	#print E
	# # 

	#Plotting stuff. Not necessary to do it here. Refer to bimodal.py
	#f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)

	
	#ax2.hist(S, 42, normed = False, color = 'blue', alpha = 0.5)
	
	# 
	# 
	#2D histogram plotting
	#fig = plt.figure()
	#ax = fig.add_subplot(111)
	#plt.hist2d(E, S, bins = 30, range = [[-.025, 1.025], [-.025, 1.025]])#norm=LogNorm()
	# 
	# # 
	# plt.xlim(-0.025, 1.025)
	# plt.ylim(-0.025, 1.025)
	# cb = plt.colorbar()
	# cb.set_label('Number of Events')
	# ax.set_xlabel('$E_{FRET}$')
	# ax.set_ylabel('Coincidence')
	# # # 
	# # # #Saving
	#plt.savefig(name+"2D_hist.pdf", dpi=600)
	# # 
	# # #Show
	return E
	
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_color_cycle(['red', 'orange', 'yellow', 'green', 'blue', 'navy', 'purple'])
for name in namelist:
	E = EFRET(name)
	np.savetxt(name+'EFRET.txt', E, '%.2f', delimiter='\t')
	ax.hist(E, 42, normed = False, range = (-0.025, 1.025),  alpha = 0.8, label = name)
	plt.xlim(-0.05, 1.05)
	plt.ylim(0, 2000)
	plt.savefig(name+"E.pdf", dpi=600)
plt.legend()
plt.show()
# # #Saving
