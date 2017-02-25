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


def StripRootFileName(filepath):
    striped_path = filepath.split('/')
    print striped_path
    nparts = len(striped_path)
    return striped_path[nparts-1]

    
## generic code starts here
def makeTChain():
    timingTree = TChain(treeName)
    infile = open(textfilename)
    for ifile in infile:
        timingTree.Add(ifile.rstrip())
        outputfilename = StripRootFileName(ifile.rstrip())
    return timingTree


