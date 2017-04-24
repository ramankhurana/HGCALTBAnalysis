# In this at the end of filevector I am putting the dirname
# so loop over n-1 files and n will give the name of the output dir.

# In legend also the n element will give the name for the ratio plot y axis label.
#edited by Monika Mittal 
#Script for ratio plot 
#import sys
#sys.argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)

#import ROOT
from ROOT import TFile, TH1F, gDirectory, TCanvas, TPad, TProfile,TGraph, TGraphAsymmErrors
from ROOT import TH1D, TH1, TH1I
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from ROOT import TLegend
from ROOT import TMath
from ROOT import TPaveText
from ROOT import TLatex

import os
colors=[3,4,5,6,7,8,9,1,2,11,41,46,30,12,28,20,32]
markerStyle=[23,24,22,20,21,25,26,27,28,29,20,21,22,23]            
linestyle=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

def DrawOverlap(fileVec, histVec, titleVec,legendtext,pngname,logstatus=[0,0],xRange=[-99999,99999,1]):

    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    gStyle.SetTitleOffset(1.1,"Y");
    gStyle.SetTitleOffset(0.9,"X");
    gStyle.SetLineWidth(3)
    gStyle.SetFrameLineWidth(3); 

    i=0

    histList_=[]
    histList=[]
    histList1=[]
    maximum=[]
    
    ## Legend    
    leg = TLegend(0.4, 0.70, 0.939, 0.89)#,NULL,"brNDC");
    legendtitle = legendtext[-1]
    leg.SetHeader(legendtitle)
    leg.SetBorderSize(0)
    leg.SetNColumns(2)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(22)
    leg.SetTextSize(0.045)
     
    c = TCanvas("c1", "c1",0,0,500,500)
    #c.SetBottomMargin(0.15)
    #c.SetLeftMargin(0.15)
    #c.SetLogy(0)
    #c.SetLogx(0)
    c1_2 = TPad("c1_2","newpad",0.04,0.05,1,0.994)
    c1_2.Draw()

    
    print ("you have provided "+str(len(fileVec))+" files and "+str(len(histVec))+" histograms to make a overlapping plot" )
    print "opening rootfiles"
    c.cd()
    #c1_2.SetBottomMargin(0.13)
    c1_2.SetLogy(logstatus[1])
    c1_2.SetLogx(logstatus[0])
    
    
    c1_2.cd()
    ii=0    
    inputfile={}
    print str(fileVec[(len(fileVec)-1)])

    for ifile_ in range(len(fileVec)):
        print ("opening file  "+fileVec[ifile_])
        inputfile[ifile_] = TFile( fileVec[ifile_] )
        print "fetching histograms"
        for ihisto_ in range(len(histVec)):
            print ("printing histo "+str(histVec[ihisto_]))
            histo = inputfile[ifile_].Get(histVec[ihisto_])
            #status_ = type(histo) is TGraphAsymmErrors
            histList.append(histo)
            # for ratio plot as they should nt be normalize 
            histList1.append(histo)
            print histList[ii].Integral()
            #histList[ii].Rebin(xRange[2])
            type_obj = type(histList[ii])
            if (type_obj is TH1D) or (type_obj is TH1F) or (type_obj is TH1) or (type_obj is TH1I) :
                histList[ii].Rebin(1)
                histList[ii].Scale(1.0/histList[ii].Integral())
                maximum.append(histList[ii].GetMaximum())
                maximum.sort()
            ii=ii+1

    print histList
    for ih in range(len(histList)):
        tt = type(histList[ih])
#        print "graph_status =" ,(tt is TGraphAsymmErrors)
#        print "hist status =", (tt is TH1D) or (tt is TH1F)
        if ih == 0 :      
            if (tt is TGraphAsymmErrors) | (tt is TGraph) : 
                histList[ih].Draw("A3P")
            if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
                histList[ih].Draw("HIST")   
        if ih > 0 :
            #histList[ih].SetLineWidth(2)
            if (tt is TGraphAsymmErrors) | (tt is TGraph) : 
                histList[ih].Draw("3P same")
            if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
                histList[ih].Draw("HISTsame")   

        if (tt is TGraphAsymmErrors) | (tt is TGraph) :
           # histList[ih].SetMaximum(0.06) 
           # histList[ih].SetMinimum(0.02) 

#            histList[ih].SetMaximum(maximum+0.3) 
            histList[ih].SetMinimum(0.02) 
            histList[ih].SetMarkerColor(colors[ih])
            histList[ih].SetLineColor(colors[ih])
            histList[ih].SetLineWidth(3)
            histList[ih].SetLineStyle(linestyle[ih])
            
            histList[ih].SetMarkerStyle(markerStyle[ih])
            histList[ih].SetMarkerSize(1)
            leg.AddEntry(histList[ih],legendtext[ih],"P")
        if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
            histList[ih].SetLineStyle(linestyle[ih])
            histList[ih].SetLineColor(colors[ih])
            histList[ih].SetLineWidth(3)
            histList[ih].SetMaximum(maximum[0]+0.3) 
            histList[ih].SetMinimum(0) 
            leg.AddEntry(histList[ih],legendtext[ih],"L")
        histList[ih].GetYaxis().SetTitle(titleVec[1])
        histList[ih].GetYaxis().SetTitleSize(0.045)
        histList[ih].GetYaxis().SetTitleOffset(1.1000998)
        histList[ih].GetYaxis().SetTitleFont(22)
        histList[ih].GetYaxis().SetLabelFont(22)
        histList[ih].GetYaxis().SetLabelSize(.045)
        histList[ih].GetXaxis().SetRangeUser(xRange[0],xRange[1])
        histList[ih].GetXaxis().SetLabelSize(0.0000);
        histList[ih].GetXaxis().SetTitle(titleVec[0])
        histList[ih].GetXaxis().SetLabelSize(0.052)
        histList[ih].GetXaxis().SetTitleSize(0.052)
        histList[ih].GetXaxis().SetTitleOffset(1.04)
        histList[ih].GetXaxis().SetTitleFont(22)
        histList[ih].GetXaxis().SetTickLength(0.07)
        histList[ih].GetXaxis().SetLabelFont(22)
        histList[ih].GetYaxis().SetLabelFont(22) 
# histList[ih].GetXaxis().SetNdivisions(508)
#

        i=i+1
    pt = TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(22)
    pt.SetTextSize(0.046)
    text = pt.AddText(0.05,0.5,"CMS Preliminary")
    #text = pt.AddText(0.5,0.5,"12.9 fb^{-1} (13 TeV)")
#    text = pt.AddText(0.8,0.5," (13 TeV)")
 #   text = pt.AddText(0.65,0.5," AK8")
    pt.Draw()
   
    

#    t2a = TPaveText(0.0877181,0.81,0.9580537,0.89,"brNDC")
#    t2a.SetBorderSize(0)
#    t2a.SetFillStyle(0)
#    t2a.SetTextSize(0.040) 
#    t2a.SetTextAlign(12)
#    t2a.SetTextFont(62)
#    histolabel1= str(fileVec[(len(fileVec)-1)])
#    text1 = t2a.AddText(0.06,0.5,"CMS Internal") 
#    t2a.Draw()
    leg.Draw()
#
#    c.cd()
    outputdirname = 'HGCAL/'
    histname=outputdirname+pngname 
    c.SaveAs(histname+'.png')
    c.SaveAs(histname+'.pdf')
#    outputname = 'cp  -r '+ outputdirname +' /afs/hep.wisc.edu/home/khurana/public_html/'
#    os.system(outputname) 




print "calling the plotter"

radiationlength = ['5_7', '10']

for rl in radiationlength: 
    print rl
    files1 = ['ResPlot_new_GeV_'+rl+'_X0.root']
    plotname= ['EnergyVsWidth_cell_17','EnergyVsWidth_cell_18','EnergyVsWidth_cell_19','EnergyVsWidth_cell_20','EnergyVsWidth_cell_21','EnergyVsWidth_cell_22','EnergyVsWidth_cell_23','EnergyVsWidth_amp_0_1','EnergyVsWidth_amp_5_1']
    legend=['17','18','19','20','21','22','23','combo_1','combo_2', 'comparison']
    DrawOverlap(files1,plotname,["Energy","Resolution"],legend,'EnergyVsWidth_cell_Combine_GeV_'+rl+'_X0',[0,0],) 
    
    #files1 = ['ResPlot_new_GeV_'+rl+'_X0.root']
    plotname1= ['EnergyVsWidth_amp_0_1','EnergyVsWidth_amp_5_1','EnergyVsWidth_amp_15_1','EnergyVsWidth_amp_25_1','EnergyVsWidth_amp_70_1']
    legend=['0','5','15','25','70', 'amp. th.']
    DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_ForVariousAmplCut_GeV_'+rl+'_X0',[0,0],) 
    
    
    plotname1= ['EnergyVsWidth_amp_0_2','EnergyVsWidth_amp_0_3','EnergyVsWidth_amp_0_4','EnergyVsWidth_amp_0_5','EnergyVsWidth_amp_0_6','EnergyVsWidth_amp_0_7']
    legend=['2','3','4','5','6','7','ncells']
    DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_GeV_'+rl+'_X0_ncellscom_amplcut_0_',[0,0],) 
    
    plotname1= ['EnergyVsWidth_amp_5_2','EnergyVsWidth_amp_5_3','EnergyVsWidth_amp_5_4','EnergyVsWidth_amp_5_5','EnergyVsWidth_amp_5_6','EnergyVsWidth_amp_5_7']
    legend=['2','3','4','5','6','7','ncells']
    DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_GeV_'+rl+'_X0_ncellscom_amplcut_5_',[0,0],) 
    
    plotname1= ['EnergyVsWidth_amp_15_2','EnergyVsWidth_amp_15_3','EnergyVsWidth_amp_15_4','EnergyVsWidth_amp_15_5','EnergyVsWidth_amp_15_6','EnergyVsWidth_amp_15_7']
    legend=['2','3','4','5','6','7','ncells']
    DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_GeV_'+rl+'_X0_ncellscom_amplcut_15_',[0,0],) 
    
    plotname1= ['EnergyVsWidth_amp_25_2','EnergyVsWidth_amp_25_3','EnergyVsWidth_amp_25_4','EnergyVsWidth_amp_25_5','EnergyVsWidth_amp_25_6','EnergyVsWidth_amp_25_7']
    legend=['2','3','4','5','6','7','ncells']
    DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_GeV_'+rl+'_X0_ncellscom_amplcut_25_',[0,0],) 
    
    
    plotname1= ['EnergyVsWidth_amp_5_2','EnergyVsWidth_amp_5_3','EnergyVsWidth_amp_70_4','EnergyVsWidth_amp_70_5','EnergyVsWidth_amp_70_6','EnergyVsWidth_amp_70_7']
    legend=['2','3','4','5','6','7','ncells']
    DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_GeV_'+rl+'_X0_ncellscom_amplcut_70_',[0,0],) 
    


'''
files = ['ResPlot_new_GeV_10_X0.root']
plotname= ['EnergyVsWidth_cell_17','EnergyVsWidth_cell_18','EnergyVsWidth_cell_19','EnergyVsWidth_cell_20','EnergyVsWidth_cell_21','EnergyVsWidth_cell_22','EnergyVsWidth_cell_23','EnergyVsWidth_amp_70_1','EnergyVsWidth_amp_5_1']
legend=['17','18','19','20','21','22','23','combo_1','combo_2']
DrawOverlap(files,plotname,["Energy","Resolution"],legend,'EnergyVsWidth_cell_Combine_GeV_10_X0',[0,0],) 

files1 = ['ResPlot_new_GeV_10_X0.root']
plotname1= ['EnergyVsWidth_amp_0_1','EnergyVsWidth_amp_5_1','EnergyVsWidth_amp_15_1','EnergyVsWidth_amp_25_1','EnergyVsWidth_amp_70_1']
legend=['0','5','15','25','70']
DrawOverlap(files1,plotname1,["Energy","Resolution"],legend,'EnergyVsWidth_Combine_ForVariousAmplCut_GeV_10_X0',[0,0],) 
'''
