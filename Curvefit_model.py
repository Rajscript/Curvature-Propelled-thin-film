# importing modules  
import os 
import sys 
import re
import pandas as pd
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from scipy.optimize import curve_fit
#This code takes the total energy obtained from the simulation model and fit an exponential function (aexp(bx)+c) to it, where x is the displacement of the floating film from the center(x=0). After finding the optimized parameters we can rescale the total energy for further data analyis. We scale it by using the energy function at x=0 (a+b). Thus scale energy is: dU= U-(a+b). 

class data_cleaning:
 def __init__(self, Vol, meshLength, sr, stretch):     
       data = pd.read_csv("Stretching_"+str(stretch)+"-Vol_"+str(Vol)+".csv") #reading the csv file obtain from the data extraction script
       x=data['Disp']
       dU=data['Total(stretching)']
       #scaled_dU=dU/gamma
       csvfile='Curve_fitMesh-' + str(meshLength) + 'Radius'+ str(sr)+'Vol-' + str(Vol)+'stretching'+str(stretch)+'.csv'  #saves the csv file with the cleaned rescaled data.
       plt.scatter(x,dU, label='mesh'+str(meshLength)) #plots the total energy vs displacement

  #define the function to fit our data
       def func(x, a0,a1,a2):     
           return a0*np.exp(x*a1)+a2
       popt, pcov =curve_fit(func, x, dU, p0=[0.000123, 3.1,  55.3005]) #optimized curve fitting through scipy library with a guess
       print(popt)
       x_model= np.linspace(0,3.2,1000)
       y_model= func(x_model, popt[0], popt[1], popt[2])
       plt.plot(x_model, y_model, label='fit: a=%5.3e, b=%5.3f, c=%5.3f' % tuple(popt)) #plotting the optimized curve fit over our data  
       plt.ylim(99.155, 99.16)
       plt.ylabel('dU')
       plt.xlabel('x')
       x=np.asarray(x)
       total=np.asarray(dU)
       total=total-(popt[0]+popt[2])                   #rescaling the energy by substracting value of the model at displacement 0 (a+c) (from aexp(bx)+c) from the total energy 
       arr1inds = x.argsort()
       x=x[arr1inds[::1]]
       total = total[arr1inds[::1]]
       np.savetxt(csvfile, np.column_stack((x, total)), fmt='%0.14f', delimiter=',', header='x,total', comments='') #saving the rescaled total energy along with the displacement
       plt.legend()
       plt.tight_layout()
       plt.savefig('exponentialfit.png')                     
       plt.show()
i=1
Vol = 26.97        # volume or pressure of drop
if len(sys.argv) > i :
    Vol, i = float(sys.argv[i]), i+1

meshLength = 0.2        # mesh refinement on sheet
if len(sys.argv) > i :
    meshLength, i = float(sys.argv[i]), i+1

sr=0.0 #sheet radius
if len(sys.argv) > i :
    sr, i = float(sys.argv[i]), i+1
stretch=0.0 #stretching modulus
if len(sys.argv) > i :
    stretch, i = int(sys.argv[i]), i+1
data_cleaning(Vol, meshLength, sr, stretch)
