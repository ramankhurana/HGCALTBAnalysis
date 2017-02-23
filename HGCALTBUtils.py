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


''' Remove cell numbers where we don't have the timing sensitive detector '''
def makesensitivelist(fullList):
    toremove = [24, 16, 13, 12, 11, 10, 9, 8, 4, 3, 2, 1, 0]
    for iele in toremove: 
        fullList = removeElement(fullList,iele)
    return fullList

''' correct the timing of each cell
by subtracting the PhoteK time. 
Each group of cells have different Photek. 
'''
def CorrectTiming(fullList, (tt_gauspeak)):
    fullList[5] = -(fullList[5] - tt_gauspeak[0])
    fullList[6] = -(fullList[6] - tt_gauspeak[0])
    fullList[7] = -(fullList[7] - tt_gauspeak[0])
    
    fullList[14] = (fullList[14] - tt_gauspeak[8])
    fullList[15] = (fullList[15] - tt_gauspeak[8])
    
    for iele in range(17,24):
        fullList[iele] = -(fullList[iele] - tt_gauspeak[16])

    for iele in range(25,32):
        fullList[iele] = -(fullList[iele] - tt_gauspeak[24])
        
    return fullList


''' Calibrated timing information 
The corrected time is then calibrated so that the mean time for each cell from group 3 is at zero. 
This is done only for group three, for other groups one may need to change the code a bit. 
'''
def CalibratedTiming(fullList):
    
    for iele in range(17,24):
        #print iele
        fullList[iele] = fullList[iele] - calibration[str(iele)]
        #print (iele,fullList[iele], calibration[str(iele)])
        #print fullList[iele]
    return fullList


def SetNeighbourFlag(sorted_ring1):
    nhbr = neighbours()
    
    if len(sorted_ring1) ==1: sorted_ring1[0].isneighbour_  = True
    if len(sorted_ring1) > 1:
        centercell = sorted_ring1[0].icell
        sorted_ring1[0].isneighbour_ = True
        for icell in range(1,len(sorted_ring1)):
            print 'icell inside loop',sorted_ring1[icell].icell
            sorted_ring1[icell].isneighbour_ = bool(nhbr.isNeighbour(centercell, sorted_ring1[icell].icell))
            if (nhbr.isNeighbour(centercell, sorted_ring1[icell].icell)):
                print (sorted_ring1[icell].icell, 'is neighbour of center cell ', centercell)
            else: 
                print (sorted_ring1[icell].icell, 'is **NOT** neighbour of center cell ', centercell)
    return sorted_ring1

def FilterRing(sorted_ring1):
    ## write upto this into a function 
    filtered_ring1=[]
    for icell in range(len(sorted_ring1)):
        if sorted_ring1[icell].isneighbour_ == True: 
            filtered_ring1.append(sorted_ring1[icell])
            
    ## after filtering         
    print 'size of list after cleaning is ', len(filtered_ring1)
    return filtered_ring1 


def LinearEnergyWeightedTime(filtered_ring1):
    sum1_ = 0.0
    sum2_ = 0.0
    totalT = 0.0
    for icell in range(len(filtered_ring1)):
        iamp = filtered_ring1[icell].amplitude_
        itime = filtered_ring1[icell].time_calibrate_
        product1_ = iamp * (itime)
        sum1_  =  sum1_ + product1_
        sum2_ = sum2_ + iamp
    ## end of for loop
    if len(filtered_ring1) > 0: totalT = sum1_ / sum2_
    else:  totalT = -99. 
    print 'totalT = ', totalT
    return totalT


def QuadratureEnergyWeightedTime(filtered_ring1):
    sum1_ = 0.0
    sum2_ = 0.0
    totalT = 0.0
    for icell in range(len(filtered_ring1)):
        iamp = filtered_ring1[icell].amplitude_
        itime = filtered_ring1[icell].time_calibrate_
        product1_ = iamp*iamp * (itime)
        sum1_  =  sum1_ + product1_
        sum2_ = sum2_ + (iamp*iamp)
    ## end of for loop
    if len(filtered_ring1) > 0: totalT = sum1_ / sum2_
    else:  totalT = -99. 
    print 'totalT = ', totalT
    return totalT


from math import log10
def LogEnergyWeightedTime(filtered_ring1):
    sum1_ = 0.0
    sum2_ = 0.0
    totalT = 0.0
    
    deno = 0.0 
    for icell in range(len(filtered_ring1)): deno = deno + filtered_ring1[icell].amplitude_
    
    for icell in range(len(filtered_ring1)):
        iamp = filtered_ring1[icell].amplitude_
        itime = filtered_ring1[icell].time_calibrate_
        weight_ = log10(10*iamp / deno)
        sum1_ = sum1_ + (weight_ * itime)
        sum2_ = sum2_ + weight_
    ## end of for loop
    if (len(filtered_ring1) > 0) & (sum2_ > 0.0): totalT = sum1_ / sum2_
    else:  totalT = -99. 
    print 'totalT = ', totalT
    return totalT

