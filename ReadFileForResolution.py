import os
import sys
import math
from ROOT import *


from array import array

def makeOffsetgraph(cell_,amplitude_):
    txtfile = open('Resolution_TimeCorrected.txt','read')
    a=[]
    b=[]
    c=[]
    d=[]
    for line in txtfile:
    
        stripline_ = line.rstrip()
        a_,b_,c_,d_ = stripline_.split()
        a.append(a_)
        b.append(b_)
        c.append(c_)
        d.append(d_)
    

    energy =  array( 'd' )
    resolution= array( 'd' )
    gr=TGraph()
    #gr=[]
    for icell in range(len(a)):
#        print ( cell_ ,"  ", amplitude_)    
        if ((a[icell] == cell_) & (c[icell] == amplitude_) & (float(b[icell]) > 35.0)):
            energy.append(float(b[icell]))
            resolution.append(float(d[icell]))
    gr = TGraph(len(energy), energy, resolution)
    print (len(energy),"  ", energy, "  ",resolution)
    return gr


rootfile = TFile('OutputrootFileResolution_withamplitude.root','recreate')
energylist = [20,32.50,100,150,200,250]
amplitudelist = [0,1,2,3,4]
celllist=[17,18,19,20,21,22,23,100]
for icelll in range(len(celllist)):
#for icelll in range(17,23):
    for iamp in range( len(amplitudelist)):
        print 
        mg = makeOffsetgraph(str(celllist[icelll]),str(iamp))
        histoname ='Resolution_cell_'+str(celllist[icelll])+'_amp_'+str(iamp)
        mg.SetNameTitle(histoname,histoname)

        rootfile.cd()
        mg.Write()

   


