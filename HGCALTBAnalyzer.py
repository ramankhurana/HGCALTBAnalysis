#!/usr/bin/env python                                                                                                                                                               
#### 
## Changes 
# - interchange TDCX and TDCy
# - add calibration 
# - add histo for lineartime45 - lineartime45[16]
# - add histo for linear 60 - gauspeak [16] 
##  
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

## Some Fixed parameters
## can be made configurable later on, once code is stable 
debug_ = False
treeName = 't1065'
textfilename = 'inputrootfiles.txt'
outputfilename = ''

calibration={'17':10.12,
             '18':10.3,
             '19':10.05,
             '20':10.15,
             '21':10.11,
             '22':10.01,
             '23':10.18}


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


def defineHistograms(postfix="_"):
    TDCmap = TH2F('TDCmap'+postfix,'TDCmap'+postfix,40,-20,20, 40,-20,20)
    allhisto = {'TDCmap':TDCmap}
    
    h_TDCxVsTDCy_withoutAmpCut = TH2F('TDCxVsTDCy_withoutAmpCut','TDCxVsTDCy_withoutAmpCut',100,-30,30,100,-30,30)
    allhisto ['TDCmapNoAmpCut'] = h_TDCxVsTDCy_withoutAmpCut

    h_TDCxVsTDCy_withAmpCut=[]
    h_Timeplot=[]
    h_TimeCorrected=[]
    for icell in range(17,24):
        cellnumber = str(icell)
        
        h_TDCxVsTDCy_withAmpCut.append ( TH2F("TDCxVsTDCy_withAmpCut_"+cellnumber,"TDCxVsTDCy_withAmpCut_"+cellnumber,100,-30,30,100,-30,30) )
        allhisto ['TDCmapWithAmpCut_'+cellnumber] = h_TDCxVsTDCy_withAmpCut[icell-17]
        
        h_Timeplot.append( TH1F("TimePlot_"+cellnumber,"TimePlot_"+cellnumber,100,9.5,10.5) )
        allhisto ['time_'+cellnumber] = h_Timeplot[icell-17]
        
        h_TimeCorrected.append( TH1F('TimeCorrected_'+cellnumber, 'TimeCorrected_'+cellnumber, 100,-0.5,0.5) )
        allhisto ['timecorrected_'+cellnumber] = h_TimeCorrected[icell-17]
        
    return allhisto
    
def analyze(timingTree, allhisto_):
    NEntries = timingTree.GetEntries()
    if debug_: print "NEntries = ",NEntries
    for ievent in range(NEntries):
        if ievent%1 ==0: print ievent
        timingTree.GetEntry(ievent)
        tt_event                        = timingTree.__getattr__('event') # UInt_t
        tt_ngroups                      = timingTree.__getattr__('ngroups') # UInt_t
        tt_nsamples                     = timingTree.__getattr__('nsamples') # UInt_t
        tt_nchannels                    = timingTree.__getattr__('nchannels') # UInt_t
        tt_tc                           = timingTree.__getattr__('tc') # UShort_t[4]
        tt_b_c                          = timingTree.__getattr__('b_c') # UShort_t[36864]
        tt_raw                          = timingTree.__getattr__('raw') # Short_t [36][1024]
        tt_t                            = timingTree.__getattr__('t') # Int_t[36864]
        tt_channel                      = timingTree.__getattr__('channel') # Short_t[36][1024]
        tt_channelCorrected             = timingTree.__getattr__('channelCorrected') # Short_t[36][1024]
        tt_t0                           = timingTree.__getattr__('t0') # Int_t [1024]
        tt_time                         = timingTree.__getattr__('time') # Float_t[4][1024]
        tt_xmin                         = timingTree.__getattr__('xmin') # Float_t[36]
    # the amplitude in channels i
        tt_amp                          = timingTree.__getattr__('amp') # Float_t[36]
        tt_base                         = timingTree.__getattr__('base') # Float_t[36]
        tt_int                         = timingTree.__getattr__('int') # Float_t[36]
        tt_intfull                      = timingTree.__getattr__('intfull') # Float_t[36]
        tt_risetime                     = timingTree.__getattr__('risetime') # Float_t[36]
    # the time from a gaus fit
        tt_gauspeak                     = timingTree.__getattr__('gauspeak') # Float_t[36]
        tt_linearTime0                  = timingTree.__getattr__('linearTime0') # Float_t[36]
        tt_linearTime15                 = timingTree.__getattr__('linearTime15') # Float_t[36]
        tt_linearTime30                 = timingTree.__getattr__('linearTime30') # Float_t[36]
    # the time from a linear fit for the rising edge
        tt_linearTime45                 = timingTree.__getattr__('linearTime45') # Float_t[36]
        tt_linearTime60                 = timingTree.__getattr__('linearTime60') # Float_t[36]
        
        ## interchanging the X and Y becuase these are stored wrong in the previous step. 
        tt_TDCx                         = timingTree.__getattr__('TDCy') # Float_t
        tt_TDCy                         = timingTree.__getattr__('TDCx') # Float_t
        
        
        
        allhisto_['TDCmap'].Fill(tt_TDCx,tt_TDCy)


        if ( (abs(tt_TDCx) > 30.) ):  continue
        if ( (abs(tt_TDCy) > 30.) ):  continue
        
        allhisto_['TDCmapNoAmpCut'].Fill(tt_TDCx,tt_TDCy)

        tt_linearTime45_corrected = CorrectTiming(list(tt_linearTime45), list(tt_gauspeak))
                
        
                
        '''for iele in range(len(tt_amp_sensitive)):
            print (tt_amp_sensitive[iele], tt_linearTime45_sensitive[iele])
        '''
    
        
        # fill TDC map and timing information for each cell. 
        info_ring1 = []
        for icell in range(17,24):
            cellnumber = str(icell)
            if ( (abs(tt_TDCx)<30.) & (abs(tt_TDCy)<30.) & (tt_amp[icell] > 0.1) & (tt_amp[icell] <0.48) ):
                allhisto_['TDCmapWithAmpCut_'+cellnumber].Fill(tt_TDCx,tt_TDCy)
                
                time_ = tt_linearTime45_corrected[icell] 
                time_calibrated = time_ - calibration[str(icell)]
                
                # fill timing information in a given range
                if ( (time_ < 10.5) & (time_ >9.5)):                     allhisto_['time_'+cellnumber].Fill(time_)
                
                # fill the corrected timing info
                allhisto_['timecorrected_'+cellnumber].Fill(time_calibrated)
                ci = cellInfo()
                ci.icell = icell
                ci.tdcx = tt_TDCx
                ci.tdcy = tt_TDCy
                ci.time_ = tt_linearTime45[icell]
                ci.time_correct_ = time_
                ci.time_calibrate_ = time_calibrated
                ci.amplitude = tt_amp[icell]
                ci.integral = tt_int[icell]
                
                if debug_: ci.Print()
                #info_ring[str(icell)] = []
                info_ring1.append(ci)
        
        #if debug_:
                

        sorted_ring1 = sorted(info_ring1, key=operator.attrgetter('amplitude'))
        sorted_ring1.reverse()
        
        ''' alternate method to sort the python list
        info_ring1.sort(key=operator.attrgetter('amplitude'))
        '''
        
        print 'size of list before cleaning is ', len(sorted_ring1)
        ## write following part of code into a function 
        nhbr = neighbours()
        if len(sorted_ring1) > 1:
            centercell = sorted_ring1[0].icell
            sorted_ring1[0].isneighbour = True
            for icell in range(1,len(sorted_ring1)):
                print 'icell inside loop',sorted_ring1[icell].icell
                sorted_ring1[icell].isneighbour = nhbr.isNeighbour(centercell, sorted_ring1[icell].icell)
                if (nhbr.isNeighbour(centercell, sorted_ring1[icell].icell)):
                    print (sorted_ring1[icell].icell, 'is neighbour of center cell ', centercell)
                else: 
                    #sorted_ring1.pop(icell)
                    print (sorted_ring1[icell].icell, 'is **NOT** neighbour of center cell ', centercell)
        
        ## write upto this into a function 
        filtered_ring1=[]
        for icell in range(len(sorted_ring1)):
            if sorted_ring1[icell].isneighbour == True: 
                filtered_ring1.append(sorted_ring1[icell])

        print 'size of list after cleaning is ', len(filtered_ring1)
        


        
        if debug_: print [tt_event, tt_ngroups, tt_nsamples, tt_nchannels, tt_tc[0], tt_amp[0], tt_base[0], tt_gauspeak[0], tt_linearTime45[0], tt_TDCx, tt_TDCy ]
    return allhisto_

def WriteHistograms(allhistoFilled_):
    print allhistoFilled_
    outfile_ = TFile(outputfilename,'RECREATE')
    outfile_.cd()
    for k in allhistoFilled_.keys():
        allhistoFilled_[k].Write()
        
    outfile_.Close()
    return ;

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

''' remove a given element from the list, provided by the variable 'index' '''
def removeElement(a,index):
    a = a[:index] + a[index+1 :]
    return a 


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
## Main of the code. 
if __name__ == "__main__":
    

    infile = open(textfilename)
    ## make one rootfile for each input file. 
    ## TChain should be inside loop becuase sequence has to run on each rootfile and give one output rootfile instead of one big rootfile. 
    for ifile in infile:
        timingTree_ = TChain(treeName)
        timingTree_.Add(ifile.rstrip())
        outputfilename = StripRootFileName(ifile.rstrip())
            #timingTree_ = makeTChain()
        allhisto_  = defineHistograms()
        allhistoFilled_  = analyze(timingTree_, allhisto_)
        WriteHistograms(allhistoFilled_)
    
