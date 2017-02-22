import os
import sys
import math
from ROOT import *

txtfile = open('Resolution.txt','read')

a=[]
b=[]
c=[]

for line in txtfile:
    
    stripline_ = line.rstrip()
    a_,b_,c_ = stripline_.split()
    a.append(a_)
    b.append(b_)
    c.append(c_)

    

from array import array
def makeresolutiongraph(cell_):
    energy =  array( 'd' )
    resolution= array( 'd' )
    for icell in range(len(a)):
        if a[icell] == cell_: 
            energy.append(float(b[icell]))
            resolution.append(float(c[icell]))
    gr = TGraph(len(a), energy, resolution)
    return gr

gr1 = makeresolutiongraph('17')
c = TCanvas()
gr1.Draw()
c.SaveAs("test.pdf")
