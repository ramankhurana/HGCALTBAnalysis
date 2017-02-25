import os
import sys
import math
from ROOT import *

txtfile = open('Resolution.txt','read')

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
    

from array import array
def makewidthgraph(cell_):
    energy =  array( 'd' )
    resolution= array( 'd' )
    gr=TGraph()
    for icell in range(len(a)):
        if a[icell] == cell_:
            energy.append(float(b[icell]))
            resolution.append(float(c[icell]))
            print (len(a),"  ", energy, "  ",resolution)
        gr = TGraph(len(energy), energy, resolution)
    return gr

from array import array
def makeresolutiongraph(cell_):
    energy =  array( 'd' )
    resolution= array( 'd' )
    gr1=TGraph()
    for icell in range(len(a)):
        if a[icell] == cell_:
            energy.append(float(b[icell]))
            resolution.append(float(d[icell]))
            print (len(a),"  ", energy, "  ",resolution)
        gr1 = TGraph(len(energy), energy, resolution)
    return gr1



rootfile =TFile('ResolutionPlot.root','recreate')
for icell in range(17,24):
    mg = makewidthgraph(str(icell))
    histoname ='AmpcutVsOffset_cell_'+str(icell)
    mg.SetNameTitle(histoname,histoname)

    mg1 = makeresolutiongraph(str(icell))
    histoname1 ='AmpcutVsRMS_cell_'+str(icell)
    mg1.SetNameTitle(histoname1,histoname1)

    rootfile.cd()
    mg.Write()
    mg1.Write()
   


