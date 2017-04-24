
import os
import sys
import math
from ROOT import *


from array import array

def makeOffsetgraph(cell_,textfilename,ncells ='-999'):

    txtfile = open(textfilename,'read')
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    for line in txtfile:
    
        stripline_ = line.rstrip()
        a_,b_,c_,d_,e_ = stripline_.split()
        a.append(a_)
        b.append(b_)
        c.append(c_)
        d.append(d_)
        e.append(e_)
    

    energy =  array( 'f' )
    resolution= array( 'f' )
    gr=TGraph()
    #gr=[]
    for icell in range(len(a)):
        if (a[icell] == cell_) & (ncells == str(-999)):
            print (" i am loop not correct") 
            energy.append(float(b[icell]))
            resolution.append(float(e[icell]))
        if (a[icell] == ncells) & (c[icell] == cell_):
            print (" i am in correct loop")
            energy.append(float(b[icell]))
            resolution.append(float(e[icell]))
    print ( energy,resolution)                        
    print (len(energy),"  ", energy, "  ",resolution, " ", len(resolution))
    gr = TGraph(len(energy), energy, resolution)

    return gr

#radiation_length='_GeV_5_7_X0'
radiation_length='_GeV_10_X0'
rootfile = TFile('ResPlot_new'+radiation_length+'.root','recreate')
energylist = [20,32,50,100,150,200,250]
amplist = [0,5,15,25,70]



itxtfile = 'Resolution_TimeCorrected'+radiation_length+'.txt'
ctxtfile= 'CombineResolution_DifferentAmplitude_ncellscom'+radiation_length+'.txt'

for icell in range(17,24):
    mg = makeOffsetgraph(str(icell),str(itxtfile))
    histoname ='EnergyVsWidth_cell_'+str(icell)
    mg.SetNameTitle(histoname,histoname)
    mg.Write()

for iamp in range( len(amplist)):
    for incells in range(1,8):
        mg1 = makeOffsetgraph(str(amplist[iamp]),str(ctxtfile),str(incells))
        histoname ='EnergyVsWidth_amp_'+str(amplist[iamp])+'_'+str(incells)
        mg1.SetNameTitle(histoname,histoname)
        rootfile.cd()
        mg1.Write()


   


