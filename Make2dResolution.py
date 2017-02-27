
import os
import sys
import math
from ROOT import *

txtfile = open('data/Resolution_250.txt','read')

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
    #gr=[]
    for icell in range(len(a)):
        if a[icell] == cell_:
            energy.append(float(b[icell]))
            resolution.append(float(c[icell]))
        print (len(a),"  ", energy, "  ",resolution)
    gr = TGraph(len(energy), energy, resolution)
    return gr

#from array import array
#def makeresolutiongraph(cell_):
#    energy1 =  array( 'd' )
#    resolution1= array( 'd' )
#    gr1=TGraph()
#    for icell in range(len(a)):
#        if a[icell] == cell_:
#            energy1.append(float(b[icell]))
#            resolution1.append(float(d[icell]))
#            print (len(a),"  ", energy1, "  ",resolution1)
#        gr1 = TGraph(len(energy1), energy1, resolution1)
#    return gr1



rootfile =TFile('ResolutionPlot.root','recreate')
for icell in range(17,19):
    mg = makewidthgraph(str(icell))
    #histoname ='AmpcutVsOffset_cell_'+str(icell)
    #mg.SetNameTitle(histoname,histoname)

 #   mg1 = makeresolutiongraph(str(icell))
 #   histoname1 ='AmpcutVsRMS_cell_'+str(icell)
 #   mg1.SetNameTitle(histoname1,histoname1)

    #rootfile.cd()
    #mg.Write()
 #   mg1.Write()
   


