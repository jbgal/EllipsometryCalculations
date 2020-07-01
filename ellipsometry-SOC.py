import os.path
import sys
import statistics
from numpy import *
from pylab import *
from scipy import polyfit, linspace, polyval, sqrt, stats, randn
#from numarray import *
import math
import matplotlib.pyplot as plt

#This usage is here to make sure that the dimension file - containing at the very least the sample's height, path length, and width - is included. 
def usage():
    print( "\n Usage: ellc.py -- MAKE SURE TO HAVE 'dim' FILE (h, pl, w [, angle, G, abs])")
    sys.exit(1)

#If the dimension file is not present, give the usage error
while 'dim' not in os.listdir('.'):
    usage()

#Grab the relevant dimensions from the 'dim' file
dimen = open('dim')
di = []
for line in dimen:
    k = line.split(" ")
    di.append(k)
pl = float(di[1][1])
width = float(di[2][1])


#Convert the dimensions from mm to m
plm = pl/1000
aream = plm*width/1000

#Go through all of the subdirectories, find the .DAT files containing data, and pull the info
#If a file name is 10p2.dat, then the [Delta] of the sample was captured using the ellipsometer when the strain gage reading was at 10.2 [[lbs, kg]]. The lab had two strain gages, so whether it was lbs or kg would depend on which one was used. 
#pressures = []
pressures2 = []
#delta = []
Delta2 = []
for root, dirs, files in os.walk('.'):
    if len(dirs) == 0:
        if root != './n':
            N = len(files)
            press1 = []
            for j in range(N):
                if files[j].endswith('.dat'):
                    press1.append(files[j])
            M = len(press1)
            counter = 0
            pressh = []
            datah = []
            for j in range(M):
                direc = press1[j]
                name = direc.strip(".dat")
                name = name.replace("p", ".")
                #This pulls the strain gage reading from the file name
                #pressures.append(float(name))
                pressh.append(float(name))
                filename = open(os.path.join(root,direc))
                o = []
                for line in filename:
                    k = line.split("\t")
                    o.append(k)
                data1 = o[4::3]
                data2 = []
                #This pulls the delta for each wavelength from the .dat file
                for k in range(len(data1)):
                    data2.append(float(data1[k][4]))
                #This makes sure that the data doesn't jump for example from 355 degrees to 5 degrees (i.e. loop around) which is mathematically correct but computationally problematic.
                data3 = data2[::-1]
                TOP = 150
                for val in range(len(data3)): 
                    if data3[val] > TOP:
                        data3[val] = data3[val] - 360
                #Note that there are 492 wavelengths captured by the .dat file
                for k in range(491):
                    if (data3[k]) > (TOP-60) and (data3[k+1]) < (TOP-300):
                        data3[k+1] = data3[k+1] + 360
                    elif data3[k] < (TOP-300) and (data3[k+1]) > (TOP-60):
                        (data3[k+1]) = (data3[k+1])-360
                data = data3[::-1]
#                delta.append(data)
                datah.append(data)
            Deltah = transpose(datah)
            Delta2.append(Deltah)
            pressures2.append(pressh)

#Delta = transpose(delta)

#If the strain gage reading is in kg, use the following calculation to convert from kg to N
t = float(-1/aream*9.81*10**(-12))
#If the strain gage reading is in lbs, use the following calculation to convert from lbs to N
#t = float(-1*0.45359237/aream*9.81*10**(-12))

#strain = [float(x)*t for x in pressures]

strain2 = []
for dat in pressures2:
    strain2h = []
    for j in range(len(dat)):
        strain2h.append(float(dat[j]*t))
    strain2.append(strain2h)

wavelength = []
for i in range(492):
    wavelength.append(float(data1[i][1]))


for i in range(len(strain2)):
    plt.plot(strain2[i], Delta2[i][235], 'o', label= "Set " + str(i+1))
plt.xlabel('strain')
plt.ylabel('delta')
plt.legend(ncol=1, loc=1)
plt.show()


C = []
for i in range(len(strain2)):
    Ch = []
    for j in range(len(wavelength)):
        slope, intercept, r_value, p_value, std_err = stats.linregress(strain2[i], Delta2[i][j])
        c = slope*float(wavelength[j])*10**(-9)/(2*180*plm)
        #err = std_err*float(wavelength[j])*10**(-9)/(2*180*plm)
        Ch.append(c)
    C.append(Ch)

Cavg = []
Cerr = []
cplus = []
cminus = []
for j in range(len(wavelength)):
    ch = []
    for i in range(len(strain2)):
        ch.append(C[i][j])
    chavg = statistics.mean(ch)
    cherr = statistics.stdev(ch)
    Cavg.append(chavg)
    Cerr.append(cherr)
    cplus.append(chavg + cherr)
    cminus.append(chavg - cherr)


#Write the output to a file
(fpath, fname) = os.path.split(os.getcwd())
f = open(fname, "w")
newdata = []
newdata.append("wavelength(nm)" + " " + "C avg(B)" + " " + "stdev(B)"  +  "\n")
for i in range(len(wavelength)):
    newdata.append(str(wavelength[i]) + " " + str(Cavg[i]) + " " + str(Cerr[i]) + "\n")
f.writelines(newdata)

#plot the data
plt.xlabel('Wavelength (nm)')
plt.ylabel('Stress-optic coefficient (B)')
plt.plot(wavelength, Cavg, label=fname)
plt.plot(wavelength, cplus, 'y')
plt.plot(wavelength, cminus, 'y')
plt.axhline(0, color="black")
#axis([200, 1000, -1, 1])
plt.xticks(np.arange(200, 1050, 100))
plt.legend(ncol=1, loc=1)
plt.show()


#plt.plot(x,y)
#plt.xticks(np.arange(min(x), max(x)+1, 1.0))
#plt.show()

