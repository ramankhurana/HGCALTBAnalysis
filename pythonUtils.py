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

