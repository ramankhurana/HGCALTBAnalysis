from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, AddressOf, gROOT, TH2F, TH3F
import ROOT as ROOT
import os
import sys, optparse
from array import array
import math
import numpy as numpy_
import operator
from cellInfo import *
from neighbours import *
import config

def defineHistograms(postfix="_"):
    TDCmap = TH2F('TDCmap'+postfix,'TDCmap'+postfix,40,-20,20, 40,-20,20)
    allhisto = {'TDCmap':TDCmap}
    
    h_TDCxVsTDCy_withoutAmpCut = TH2F('TDCxVsTDCy_withoutAmpCut'+postfix,'TDCxVsTDCy_withoutAmpCut',100,-30,30,100,-30,30)
    allhisto ['TDCmapNoAmpCut'] = h_TDCxVsTDCy_withoutAmpCut
    
    for iampTh in config.relativeAmpThreshold_:
        ampThStr = '_AmpTh_'+str(int(iampTh*100))
        
        h_Totaltime = TH1F('h_Totaltime'+postfix+ampThStr,'h_Totaltime', 400, -2, 2)
        allhisto['Totaltime'+ampThStr] = h_Totaltime
        
        h_NPads = TH1F('h_NPads'+postfix+ampThStr, 'h_NPads', 20, 1,21)
        allhisto['h_NPads'+ampThStr] = h_NPads 
        
        for ipad in [2,3,4,5,6,7]:
            ipad_ = str(ipad)
            h_Totaltime_NPads = TH1F('h_Totaltime'+postfix+ampThStr+ipad_,'h_Totaltime', 400, -2, 2)
            #print 'Totaltime'+ampThStr+'_'+ipad_
            allhisto['Totaltime'+ampThStr+'_'+ipad_] = h_Totaltime_NPads
        
    h_Totaltime_Quad = TH1F('h_Totaltime_Quad'+postfix,'h_Totaltime_Quad', 400, -2, 2.)
    allhisto['Totaltime_Quad'] = h_Totaltime_Quad

    h_Totaltime_Log = TH1F('h_Totaltime_Log'+postfix,'h_Totaltime_Log', 400, -2, 2.)
    allhisto['Totaltime_Log'] = h_Totaltime_Log

    h3_amp_time_cell = TH3F('h3_amp_time_cell'+postfix, 'h3_amp_time_cell', 120, 0.0, 0.6, 200, 9.0, 11.0 , 7, 17, 24)
    allhisto['amp_time_cell_'] = h3_amp_time_cell
    
    h_TDCxVsTDCy_withAmpCut=[]
    h_Timeplot=[]
    h_TimeCorrected=[]
    h2_TDCx_vs_amp=[]
    h2_TDCy_vs_amp=[]
    h2_TDCx_vs_time=[]
    h2_TDCy_vs_time=[]
    h2_amp_vs_time=[]    
    h_TimeOffsetCorrected=[]
    for icell in range(17,24):
        cellnumber = str(icell)
        
        h_TDCxVsTDCy_withAmpCut.append ( TH2F("TDCxVsTDCy_withAmpCut_"+cellnumber+postfix,"TDCxVsTDCy_withAmpCut_"+cellnumber,100,-30,30,100,-30,30) )
        allhisto ['TDCmapWithAmpCut_'+cellnumber] = h_TDCxVsTDCy_withAmpCut[icell-17]
        
        h_Timeplot.append( TH1F("TimePlot_"+cellnumber+postfix,"TimePlot_"+cellnumber,100,9.5,10.5) )
        allhisto ['time_'+cellnumber] = h_Timeplot[icell-17]
        
        h_TimeCorrected.append( TH1F('TimeCorrected_'+cellnumber+postfix, 'TimeCorrected_'+cellnumber, 100,-0.5,0.5) )
        allhisto ['timecorrected_'+cellnumber] = h_TimeCorrected[icell-17]

        h_TimeOffsetCorrected.append( TH1F('TimeOffsetCorrected_'+cellnumber+postfix, 'TimeOffsetCorrected_'+cellnumber, 200,10,30) )
        allhisto ['timeOffsetcorrected_'+cellnumber] = h_TimeOffsetCorrected[icell-17]
        
        h2_TDCx_vs_amp.append( TH2F ('h2_TDCx_vs_amp_'+cellnumber+postfix, 'h2_TDCx_vs_amp_'+cellnumber, 120, -30.0, 30.0, 100, 0.0, 1.0 ) )
        h2_TDCy_vs_amp.append( TH2F ('h2_TDCy_vs_amp_'+cellnumber+postfix, 'h2_TDCy_vs_amp_'+cellnumber, 120, -30.0, 30.0, 100, 0.0, 1.0 ) )
        
        h2_TDCx_vs_time.append( TH2F ('h2_TDCx_vs_time_'+cellnumber+postfix, 'h2_TDCx_vs_time_'+cellnumber, 120, -30.0, 30.0, 200, -1.0, 1.0 ) )
        h2_TDCy_vs_time.append( TH2F ('h2_TDCy_vs_time_'+cellnumber+postfix, 'h2_TDCy_vs_time_'+cellnumber, 120, -30.0, 30.0, 200, -1.0, 1.0 ) )
        
        h2_amp_vs_time.append( TH2F ('h2_amp_vs_time_'+cellnumber+postfix, 'h2_amp_vs_time_'+cellnumber, 120, 0.0, 0.6, 200, 9.0, 11.0 ) )
        

        allhisto['h2_TDCx_vs_amp_'+cellnumber] = h2_TDCx_vs_amp[icell-17]
        allhisto['h2_TDCy_vs_amp_'+cellnumber] = h2_TDCy_vs_amp[icell-17]
        
        allhisto['h2_TDCx_vs_time_'+cellnumber] = h2_TDCx_vs_time[icell-17]
        allhisto['h2_TDCy_vs_time_'+cellnumber] = h2_TDCy_vs_time[icell-17]
        
        allhisto['h2_amp_vs_time_'+cellnumber] = h2_amp_vs_time[icell-17]
        
        
    return allhisto






def WriteHistograms(allhistoFilled_, outputfilename,mode, dirname):
    print allhistoFilled_
    outfile_ = TFile(dirname+'/'+outputfilename,mode)
    #outfile_ = TFile('/tmp/khurana/'+outputfilename,mode)
    outfile_.cd()
    for k in allhistoFilled_.keys():
        allhistoFilled_[k].Write()
        
    outfile_.Close()
    return ;

