
import os
import sys
import math
from ROOT import *


from array import array

def makeOffsetgraph(energy_,cell_):
    txtfile = open('data/Resolution_'+str(energy_)+'.txt','read')
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
        if a[icell] == cell_:
            energy.append(float(b[icell]))
            resolution.append(float(c[icell]))
    gr = TGraph(len(energy), energy, resolution)
    print (len(a),"  ", energy, "  ",resolution)
    return gr

def makeRMSgraph(energy_,cell_):
    txtfile = open('data/Resolution_'+str(energy_)+'.txt','read')
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
    

    amp =  array( 'd' )
    rms= array( 'd' )
    gr1=TGraph()
    #gr=[]
    for icell in range(len(a)):
        if a[icell] == cell_:
            amp.append(float(b[icell]))
            rms.append(float(d[icell]))
    gr1 = TGraph(len(amp), amp, rms)
    print (len(amp),"  ", amp, "  ",rms)
    return gr1


rootfile = TFile('ResolutionPlot.root','recreate')
energylist = [20,32,50,100,150,200,250]
for ienergy in range( len(energylist)):
    for icell in range(17,23):
        mg = makeOffsetgraph(str(ienergy),str(icell))
        histoname ='AmpcutVsOffset_cell_'+str(icell)+'_energy_'+str(ienergy)
        mg.SetNameTitle(histoname,histoname)

        mg1 = makeRMSgraph(str(ienergy),str(icell))
        histoname1 ='AmpcutVsRMS_cell_'+str(icell)+'_energy_'+str(ienergy)
        mg1.SetNameTitle(histoname1,histoname1)
        
        rootfile.cd()
        mg.Write()
        mg1.Write()
   


