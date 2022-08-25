# importing modules  
import os 
import sys 
import re
import numpy as np



class energy_data_extraction:
 def __init__(self, Vol, meshLength, sr):
     
      self.Vol=Vol
      self.meshLength=meshLength
      self.sr=sr
      filepaths  = [os.path.join(sys.path[0], name) for name in os.listdir(sys.path[0])] #creating file paths to access all directories containg the energy file.
      mylines=[]
      file_list=[]
      energyfile= 'EnergyMesh-' + str(meshLength) + 'Vol-' + str(Vol) + '.txt'
      energyfilerefine='EnergyMesh-' + str(meshLength) + 'Radius' + str(sr) + 'Vol-' + str(Vol) + '-refine.txt'
      filename='10000sessile_4.19_4.19_v_0.342_'+ str(Vol) + '_' + str(meshLength) + '_sheet_True_'
      print(filename)
        
      f = open(energyfile, "w+")
      fref=open(energyfilerefine, "wt")
      delete_list=["energy", "quantity","1. ", "5. ", "7. ", "stretch", "default_area", "gravity_quant", filename , "-max__6e3-relax_1-", "_se_.log" ] #to clean the data from unnecessary strings.
      lines_to_read = [3, 11, 18]                         #lines containg the energy data
      i=0
      myFile=[]
      for path in filepaths:                              #running for loop through each of the filepath directing to unique directories 
          if path.endswith("energy.log"):                 #only choosing the files that ends with 'energy.log'
             f.write(os.path.basename(path))              
             file_list.append(os.path.basename(path))     #writing the file names in an array called 'file_list'
             f.write("\n")
             i=i+1
             print(path)
             a_file= open(path, 'rt')  
          for position, line in enumerate(a_file):        
             if position in lines_to_read:                # finding the lines containing the desired energies
               mylines.append(line)                       # adding those lines
               f.write(line)
               print(line)  
      print(file_list) 
      f=open(energyfile, "rt")                            
      for line in f:
       for word in delete_list:
           line=line.replace(word, "")
       fref.write(line)          
       res=re.findall("relax_1-(\d+)_se_energy.log", line)
       if not res: 
          continue
       print(res[0])
       fref.write(res[0])                                 #writing the final refined energy results from all directories in this text file

 def energy_csv(self):
     Vol=self.Vol
     meshLength=self.meshLength
     sr=self.sr
     myFile=[]
     disp=[]
     stretch=[]
     surface=[]
     grav=[]
     energyfilerefine='EnergyMesh-' + str(meshLength) + 'Radius'+ str(sr) +'Vol-' + str(Vol) + '-refine.txt'    
     csvfile= 'Stretching_6191-Vol_' + str(Vol) + '.csv'    
     myFile= open( energyfilerefine , "r" ).readlines()
     f = open(csvfile, "w+")
     #print(myFile)
     length=len(myFile)/4 
     for x in range(0, int(length)):
       x=x*4
       disp.append(float(myFile[x].split('d')[0]))
       stretch.append(float(myFile[x+1]))
       surface.append(float(myFile[x+2]))
       grav.append(float(myFile[x+3]))

     disp=np.asarray(disp)
     stretch=np.asarray(stretch)
     surface=np.asarray(surface)
     grav=np.asarray(grav)
     total_stretch=surface+grav+stretch
     total=surface+grav
     #print(total)
     d=np.argmin(disp)
     total_stretch_change=total_stretch-total_stretch[d]     #adding the three energies relevant to our system
     total_change=total-total[d]
     #surface=surface-surface[d]
     #grav=grav-grav[d]
     #energycollapse=total/(pow(Vol,gamma)*pow(sr, delta))
     arr1inds = disp.argsort()              
     disp=disp[arr1inds[::1]]               #sorting displacement in ascending order 
     surface = surface[arr1inds[::1]]       #sorting all the energies with respect to the displacement
     grav = grav[arr1inds[::1]]
     stretch = stretch[arr1inds[::1]]
     total_stretch = total[arr1inds[::1]]
     total = total[arr1inds[::1]]
     np.savetxt(csvfile, np.column_stack((disp, surface, grav, stretch, total_stretch, total)), fmt='%0.14f', delimiter=',', header="Disp, Surface, Grav,  Stretching, Total(stretching), Total", comments='') #comments='' is to remove the hashtag from before the header
i=1
Vol = 26.97        # input volume or pressure of drop
if len(sys.argv) > i :
    Vol, i = float(sys.argv[i]), i+1

meshLength = 0.2        # input mesh refinement on sheet
if len(sys.argv) > i :
    meshLength, i = float(sys.argv[i]), i+1

sr = 1.0        # input sheet radius
if len(sys.argv) > i :
    sr, i = float(sys.argv[i]), i+1
    
p1=energy_data_extraction(Vol, meshLength, sr)
p1.energy_csv()
