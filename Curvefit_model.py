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
"""
This code takes the total energy obtained from the simulation model and fit an exponential 
function (aexp(bx)+c) to it, where x is the displacement of the floating film from the center(x=0).
After finding the optimized parameters we can rescale the total energy for further data analyis. We
 scale it by using the energy function at x=0 (a+b). Thus scaled total energy is: dU= U-(a+b). 
"""
class data_cleaning:
 def __init__(self, Vol, meshLength, sr, stretch): 
       """
       Class for cleaning the raw energy data and rescale it for further analysis
       :param Vol:
             Volume of the liquid drop in our simulation model
       :type Vol: float  
       :param meshLength:
             Mesh refinement that regulates the triangulations of the surface
       :type meshLength: float
       :param sr:
             Sheet radius of the thin fim floating on the liquid interface
       :type sr: float  
       :param stretch:
             Stretching modulus of the thin film.
       : type stretch: int    
       """ 
       print(type(Vol))   
       data = pd.read_csv("Stretching_"+str(stretch)+"-Vol_"+str(Vol)+".csv") #reading the csv file obtain from the data extraction script
       x=data['Disp']
       U=data['Total(stretching)']
       csvfile='Curve_fitMesh-' + str(meshLength) + 'Radius'+ str(sr)+'Vol-' + str(Vol)+'stretching'+str(stretch)+'.csv'  #saves the csv file with the cleaned rescaled data.

       #define the function to fit our data
       def func(x, a0,a1,a2):
           """
          :param x:
             Radial position of the sheet on the film
           :type x: class 'pandas.core.series.Series'  
           :param a0:
             coefficient of the exponential equation
           :type a0: class 'numpy.float64'
           :param a1:
             exponential coefficient of the curve fit
           :type a1: class 'numpy.float64'  
           :param a2:
             coefficient of the curve fit
           : type a2: class 'numpy.float64'    
           """         
           return a0*np.exp(x*a1)+a2
       popt, pcov =curve_fit(func, x, U, p0=[0.000123, 3.1,  55.3005]) #optimized curve fitting through scipy library with a guess
       print(popt)
       def plot(func, x, U, popt):
           """
           :param func:
             The exponential function   
           :type func: class 'function' 
           :param x:
             Radial position of the sheet on the film
           :type x: class 'pandas.core.series.Series'  
           :param U:
             Total energy at each position
           :type x: class 'pandas.core.series.Series'    
           :param popt:
             Optimized a0, a1, a2 values
           :type popt: class 'numpy.ndarray'  
           """  
           print(type(popt))
           fig, (ax1, ax2) = plt.subplots(2)
           ax1.scatter(x,U, label='Drop Volume: '+str(Vol)) #plots the total energy vs displacement
           ax1.set_ylim(99.155, 99.16)
           x_model= np.linspace(0,3.2,1000)
           y_model= func(x_model, popt[0], popt[1], popt[2])
           ax1.plot(x_model, y_model, 'r--', label='fit: a=%5.3e, b=%5.3f, c=%5.3f' % tuple(popt)) #plotting the optimized curve fit over our data
           ax1.set_ylabel('Energy, U')
           ax1.set_xlabel('r')
           ax1.set_title('Curve Fitting total energy function') 
           x=np.asarray(x)
           total=np.asarray(U)
           total=total-(popt[0]+popt[2])                   #rescaling the energy by substracting value of the model at displacement 0 (a+c) (from aexp(bx)+c) from the total energy 
           ax2.scatter(x, total)
           ax2.set_ylabel('Rescaled Energy, dU')
           ax2.set_xlabel('r')
           ax2.set_ylim(-0.0008, 0.004)
           arr1inds = x.argsort()
           x=x[arr1inds[::1]]
           total = total[arr1inds[::1]]
           np.savetxt(csvfile, np.column_stack((x, total)), fmt='%0.14f', delimiter=',', header='x,total', comments='') #saving the rescaled total energy along with the displacement
           ax1.legend( bbox_to_anchor=[0.5, 0.75], loc='center', ncol=1)
           fig.tight_layout()
           plt.savefig('exponentialfit.png')                     
           plt.show()
       plot(func, x, U, popt)
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
