from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, AddressOf, gROOT, TH2F
import ROOT as ROOT
import os
import sys, optparse
from array import array
import math
import numpy as numpy_
import operator
from cellInfo import *
from neighbours import *


''' remove a given element from the list, provided by the variable 'index' '''
def removeElement(a,index):
    a = a[:index] + a[index+1 :]
    return a 



def beamEnergy(filename):
    nameList = (filename.rstrip()).split('/')
    name_ = nameList[-1]
    rootfilenameList = name_.split('_')
    energy = rootfilenameList[1]
    return energy



def RadiationLength(filename):
    nameList = (filename.rstrip()).split('/')
    name_ = nameList[-1]
    rootfilenameList = name_.split('_')
    x0 = str(rootfilenameList[3]) + '.' + str(rootfilenameList[4])
    return x0


print 'energy=', beamEnergy('eos/cms/store/user/khurana/HGCAL/TBNov2016/RECO/analysis/electrons_20_GeV_5_7_X0.root')
print 'x0=', RadiationLength('eos/cms/store/user/khurana/HGCAL/TBNov2016/RECO/analysis/electrons_20_GeV_5_7_X0.root')
    
