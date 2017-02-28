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

##
## User code 
##
from cellInfo import *
from neighbours import *
from HGCALTBUtils import *  ## HGCAL related functions 
from Utils import * ## ROOT related utinities 
from pythonUtils import * ## python related utilities 
from HistoUtils import * ## Histogram related utilities 
from calibrationReader import * 


usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed

parser.add_option("-i", "--inputfile", dest="inputfile")
parser.add_option("-o", "--inputOffsetfile", dest="inputOffsetfile")

parser.add_option("-e", "--extractOffsetMode", action="store_true",  dest="extractOffsetMode")
parser.add_option("-a", "--applyOffsetMode",   action="store_true",  dest="applyOffsetMode")

(options, args) = parser.parse_args()


## Some Fixed parameters
## can be made configurable later on, once code is stable 
debug_ = False
treeName = 't1065'
textfilename = 'inputrootfiles.txt'
outputfilename = ''

##
## This part of code will get the calibration constants. 
##
'''calibration={'17':0.0,
             '18':0.0,
             '19':0.0,
             '20':0.0,
             '21':0.0,
             '22':0.0,
             '23':0.0}
'''
calibration={'17':10.12,
             '18':10.3,
             '19':10.05,
             '20':10.15,
             '21':10.11,
             '22':10.01,
             '23':10.18}


amplitudeCut=[0.05, 0.1, 0.15, 0.2, 0.25]
##
## Analyse function: This will call all other functions needed and manage them. 
##   
def analyze(timingTree, allhisto_, ampCutIndex, calib):
    NEntries = timingTree.GetEntries()
    if debug_: print "NEntries = ",NEntries
    for ievent in range(NEntries):
        if ievent%1 ==100: print ievent
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
            if ( (abs(tt_TDCx)<30.) & (abs(tt_TDCy)<30.) & (tt_amp[icell] > amplitudeCut[ampCutIndex]) & (tt_amp[icell] <0.48) ):
                allhisto_['TDCmapWithAmpCut_'+cellnumber].Fill(tt_TDCx,tt_TDCy)
                
                time_ = tt_linearTime45_corrected[icell] 
                
                #print ('-------------------------------',cellnumber, str(amplitudeCut[ampCutIndex]))
                if debug_: print ('-------------------------------',cellnumber, ampCutIndex)
                offsetList    = (calib.CalibationFactor(cellnumber, str(amplitudeCut[ampCutIndex]) ))
                if debug_: print "offset list", offsetList
                
                ## correct for offset 
                if debug_:  print "offset =============================================== ", offsetList[0]
                time_calibrated = time_ - float(offsetList[0])
                
                ## fill timing information in a given range
                allhisto_['time_'+cellnumber].Fill(time_)
                
                ## fill the corrected timing info
                allhisto_['timecorrected_'+cellnumber].Fill(time_calibrated)
                
                allhisto_['timeOffsetcorrected_'+cellnumber].Fill(tt_linearTime45[icell] + float(offsetList[0]))
                
                
                
                ## 2D histograms 
                allhisto_['h2_TDCy_vs_amp_'+cellnumber].Fill(tt_TDCy, tt_amp[icell])
                allhisto_['h2_TDCx_vs_amp_'+cellnumber].Fill(tt_TDCx, tt_amp[icell])
                
                allhisto_['h2_TDCx_vs_time_'+cellnumber].Fill(tt_TDCx, time_calibrated)
                allhisto_['h2_TDCy_vs_time_'+cellnumber].Fill(tt_TDCy, time_calibrated)
                
                allhisto_['h2_amp_vs_time_'+cellnumber].Fill(tt_amp[icell], time_)
                
                allhisto_['amp_time_cell_'].Fill(tt_amp[icell], time_, icell)
                
                ci                          = cellInfo()
                ci.icell                    = icell
                ci.tdcx                     = tt_TDCx
                ci.tdcy                     = tt_TDCy
                ci.time_                    = tt_linearTime45[icell]
                ci.timeGaussPeak            = tt_gauspeak[16]
                ci.time_correct_            = time_
                ci.time_calibrate_          = time_calibrated
                ci.offset_                  = float(offsetList[0])
                ci.time_offsetCorrected_    = tt_linearTime45[icell] + float(offsetList[0])
                ci.amplitude_               = tt_amp[icell]
                ci.integral_                = tt_int[icell]
                
                
                if debug_: ci.Print()
                #info_ring[str(icell)] = []
                info_ring1.append(ci)
        
                
        ## sort the ring and reverse it. 
        sorted_ring1 = sorted(info_ring1, key=operator.attrgetter('amplitude_'))
        sorted_ring1.reverse()
        
        ''' alternate method to sort the python list
        info_ring1.sort(key=operator.attrgetter('amplitude'))
        '''
        
        ##print 'size of list before cleaning is ', len(sorted_ring1)
        
        ## set the flags about the neighbours for each cell in the event 
        sorted_ring1 = SetNeighbourFlag(sorted_ring1)
        
        ## remove the cells which are not neighbour 
        filtered_ring1 = FilterRing(sorted_ring1)
        
        ##print 'size of list after cleaning is ', len(filtered_ring1)
        
        ## calculate linear energy weighted time 
        totalT = LinearEnergyWeightedTime(filtered_ring1)
        if (len(filtered_ring1)>1): allhisto_['Totaltime'].Fill(totalT)

        ## calculate the quadrature weighted time 
        totalT = QuadratureEnergyWeightedTime(filtered_ring1)
        if (len(filtered_ring1)>1): allhisto_['Totaltime_Quad'].Fill(totalT)

        ## calculate the log energy weighted time 
        totalT = LogEnergyWeightedTime(filtered_ring1)
        if (len(filtered_ring1)>1): allhisto_['Totaltime_Log'].Fill(totalT)

        
        if debug_: print [tt_event, tt_ngroups, tt_nsamples, tt_nchannels, tt_tc[0], tt_amp[0], tt_base[0], tt_gauspeak[0], tt_linearTime45[0], tt_TDCx, tt_TDCy ]
    return allhisto_




## Main of the code. 
if __name__ == "__main__":
    

    infile = open(textfilename)
    ## make one rootfile for each input file. 
    ## TChain should be inside loop becuase sequence has to run on each rootfile and give one output rootfile instead of one big rootfile. 
    for ifile in infile:
        E  = beamEnergy(ifile)
        x0 = RadiationLength(ifile)
        calibrationtextfile = 'data/Resolution_'+E+'.txt'
        calib = calibrationReader(calibrationtextfile)
                
        timingTree_ = TChain(treeName)
        timingTree_.Add(ifile.rstrip())
        outputfilename = StripRootFileName(ifile.rstrip())
        
        ## Run in extracting mode 
        if options.extractOffsetMode: 
            allhisto_  = defineHistograms()
            allhistoFilled_  = analyze(timingTree_, allhisto_,0, calib)
            WriteHistograms(allhistoFilled_, outputfilename,"RECREATE","histogramsOffSetExtraction")

        ## Run in applying the offset mode 
        if options.applyOffsetMode: 
            for iamp in range(len(amplitudeCut)):
                allhisto_  = defineHistograms('_Amp_'+str(iamp))
                allhistoFilled_  = analyze(timingTree_, allhisto_,iamp, calib)
                if iamp==0:
                    WriteHistograms(allhistoFilled_, outputfilename,"RECREATE","histogramsRootFile")
                else:
                    WriteHistograms(allhistoFilled_, outputfilename,"UPDATE","histogramsRootFile")


