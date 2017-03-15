void SaveGraphs(  TString energy = "250",TString radiation_length = "_GeV_5_7_X0"){
  TString filename = "histogramsRootFile/electrons_"+energy+radiation_length+".root";
  cout << filename <<std::endl;
  TString dirname = "Dir_"+energy+radiation_length;
  gSystem->Exec("mkdir "+dirname);
  
  TString fileout = "Output_"+energy+radiation_length+".root";
  TFile *fout = new TFile(fileout,"recreate");
  TFile *f1 = new TFile(filename,"open");
  f1->cd();
  TString cellnumber, histoname ,ampval;
  TString histo2D;
  double range_min, range_max,x;
  int binmax;
  double par[3];
  double width[7], cell[7], peakvalue[7];
  double width_corr[7], cell_corr[7], peakvalue_corr[7];
  TCanvas *c1 = new TCanvas ("c1","c1", 700, 500);
  TF1 *fgaus;
  

  //TDCx Vs TDCy
  for (int iamp=0; iamp<1; iamp++){
    for (int j=17; j<=23; j++){
      cellnumber.Form("%d",j);
      ampval.Form("%d",iamp);
      
      histo2D = "TDCxVsTDCy_withAmpCut_"+cellnumber+"_Amp_"+ampval;
      std::cout<<" histo2D = "<<histo2D<<std::endl;
      TH2F *h4 = (TH2F*) f1->Get(histo2D);
      
      c1->cd();
      /*      h4->GetXaxis()->SetTitle("TDCx");
      h4->GetYaxis()->SetTitle("TDCy");
      h4->GetXAxis()->SetRangeUser();*/
      h4->Draw("colz");
      c1->SaveAs(dirname+"/"+histo2D+".pdf");
      
    }
  }

  //TDCx Vs time
  for (int iamp=0; iamp<1; iamp++){
    for (int j=17; j<=23; j++){
      cellnumber.Form("%d",j);
      ampval.Form("%d",iamp);
      
      histo2D = "h2_TDCx_vs_time_"+cellnumber+"_Amp_"+ampval;
      TH2F *h4 = (TH2F*) f1->Get(histo2D);
      c1->cd();
      h4->GetXaxis()->SetTitle("TDCx");
      h4->GetYaxis()->SetTitle("time");
      h4->Draw("colz");
      c1->SaveAs(dirname+"/"+histo2D+".pdf");
      
    }
  }

  //TDCy Vs time
  for (int iamp=0; iamp<1; iamp++){
    for (int j=17; j<=23; j++){
      cellnumber.Form("%d",j);
      ampval.Form("%d",iamp);
      
      histo2D = "h2_TDCy_vs_time_"+cellnumber+"_Amp_"+ampval;
      TH2F *h4 = (TH2F*) f1->Get(histo2D);
      c1->cd();
      h4->GetXaxis()->SetTitle("TDCy");
      h4->GetYaxis()->SetTitle("time");
      h4->Draw("colz");
      c1->SaveAs(dirname+"/"+histo2D+".pdf");
    }
  }


  //TDCx Vs amp
  for (int iamp=0; iamp<1; iamp++){
    for (int j=17; j<=23; j++){
      cellnumber.Form("%d",j);
      ampval.Form("%d",iamp);

      histo2D = "h2_TDCx_vs_amp_"+cellnumber+"_Amp_"+ampval;
      TH2F *h4 = (TH2F*) f1->Get(histo2D);
      c1->cd();
      h4->GetXaxis()->SetTitle("TDCx");
      h4->GetYaxis()->SetTitle("amp");
      h4->Draw("colz");
      c1->SaveAs(dirname+"/"+histo2D+".pdf");
    } 
  }


  //TDCx Vs amp
  for (int iamp=0; iamp<1; iamp++){
    for (int j=17; j<=23; j++){
      cellnumber.Form("%d",j);
      ampval.Form("%d",iamp);
      histo2D = "h2_TDCy_vs_amp_"+cellnumber+"_Amp_"+ampval;
      std::cout<<" histo2D = "<<histo2D<<std::endl;
      TH2F *h4 = (TH2F*) f1->Get(histo2D);
      c1->cd();
      h4->GetXaxis()->SetTitle("TDCy");
      h4->GetYaxis()->SetTitle("amp");
      h4->Draw("colz");
      c1->SaveAs(dirname+"/"+histo2D+".pdf");
      std::cout<<" histo saved for"<<histo2D<<std::endl;
    } 
  }

  /*
  for (int iamp=0; iamp<1; iamp++){
    ampval.Form("%d",iamp);
    histo2D = "TDCmap"+cellnumber+"_Amp_"+ampval;
    TH2F *h4 = (TH2F*) f1->Get(histo2D);
    c1->cd();
    h4->GetXaxis()->SetTitle("TDCx");
    h4->GetYaxis()->SetTitle("TDCy");
    //h4->SetOptStat(000000);
    h4->Draw("colz");
    c1->SaveAs(dirname+"/"+histo2D+".pdf");
    
    gStyle->SetOptStat(111111);
    gROOT->ForceStyle(); 
  }

  */
  //Total Time resolution
  ofstream ftext;
  ftext.open("Resolution_TimeCorrected"+radiation_length+".txt",std::fstream::app);
  /*
  for (int iamp=0; iamp<1; iamp++){
    par[0] =  par[1]= par[2] = 0;
    ampval.Form("%d",iamp);
    histoname = "h_Totaltime_Amp_" + ampval ;
    cout << histoname <<std::endl;
    TH1F *h2 = (TH1F*) f1->Get(histoname);
        
    binmax = h2->GetMaximumBin();
    x = h2->GetXaxis()->GetBinCenter(binmax);  
    range_min = x - (2*h2->GetRMS());
    range_max = x + (2*h2->GetRMS());
    fgaus = new TF1("fgaus","gaus",range_min,range_max);
    h2->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
    h2->Fit("fgaus","R");
    fgaus->GetParameters(&par[0]);
    c1->cd();
    gStyle->SetOptFit(1111111); 
    h2->Draw();
    c1->SaveAs(dirname+"/"+histoname+".pdf");
    ftext<< 100<<" " << energy <<" "<<ampval<< " "<<par[2]<<std::endl;
    // Quad
    histoname = "h_Totaltime_Quad_Amp_"+ampval;
    TH1F *h2 = (TH1F*) f1->Get(histoname);
    
    binmax = h2->GetMaximumBin();
    x = h2->GetXaxis()->GetBinCenter(binmax);  
    range_min = x - (2*h2->GetRMS());
    range_max = x + (2*h2->GetRMS());
    
    fgaus = new TF1("fgaus","gaus",range_min,range_max);
    h2->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
    h2->Fit("fgaus","R");
    c1->cd();
    gStyle->SetOptFit(1111111); 
    h2->Draw();
    c1->SaveAs(dirname+"/"+histoname+".pdf");
    
    // Log

    histoname = "h_Totaltime_Log_Amp_"+ampval;
    TH1F *h2 = (TH1F*) f1->Get(histoname);
    
    binmax = h2->GetMaximumBin();
    x = h2->GetXaxis()->GetBinCenter(binmax);  
    range_min = x - (2*h2->GetRMS());
    range_max = x + (2*h2->GetRMS());
    
    fgaus = new TF1("fgaus","gaus",range_min,range_max);
    h2->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
    h2->Fit("fgaus","R");
    c1->cd();
    gStyle->SetOptFit(1111111); 
    h2->Draw();
    c1->SaveAs(dirname+"/"+histoname+".pdf");
  }
  */
  

  for (int iamp=0; iamp<1; iamp++){
    for ( int i = 17; i <= 23; i++){
      ampval.Form("%d",iamp);
      
      par[0] =  par[1]= par[2] = 0;
      cellnumber.Form("%d",i);
      histoname = "TimePlot_"+cellnumber+"_Amp_" + ampval;
      TH1F *h2 = (TH1F*) f1->Get(histoname);
      
      binmax = h2->GetMaximumBin();
      x = h2->GetXaxis()->GetBinCenter(binmax);  
      range_min = x - (2*h2->GetRMS());
      range_max = x + (2*h2->GetRMS());
      
      fgaus = new TF1("fgaus","gaus",range_min,range_max);
      h2->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
      h2->Fit("fgaus","R");
      fgaus->GetParameters(&par[0]);
      cell[i-17] = i ;
      width[i-17] = par[2];
      peakvalue[i-17]= par[1];
      c1->cd();
      gStyle->SetOptFit(1111111); 
      h2->Draw();
      
      c1->SaveAs(dirname+"/"+histoname+".pdf");
    }
    ofstream ftext1;
    ftext1.open("Resolution_Time"+radiation_length+".txt",std::fstream::app);
    
    int n = 7;
    TGraph* gr = new TGraph(n,cell,width);
    c1->cd();
    gr->Draw("AC*");
    gr->GetXaxis()->SetTitle("Cell Number");
    gr->GetYaxis()->SetTitle("Resolution");
    gr->SetNameTitle("resolutionVsCell_Amp_" + ampval , "resolutionVsCell_Amp_" + ampval);
    c1->SaveAs(dirname+"/resolutionVsCell_Amp_" + ampval+".pdf");
    fout->cd();  
    gr->Write();  
    
    for (int i=0; i<=6; i++){
      ftext1<<    cell[i]  << " " << energy <<" "<<ampval<< " "<< peakvalue[i]<<" "<<width[i]<<std::endl;

    }
  }
  

  for (int iamp=0; iamp<1; iamp++){
    
    for ( int i = 17; i <= 23; i++){
      ampval.Form("%d",iamp);
      par[0] =  par[1]= par[2] = 0;
      cellnumber.Form("%d",i);
  
      histoname = "TimeCorrected_"+cellnumber+"_Amp_" + ampval;
      
      TH1F *h2 = (TH1F*) f1->Get(histoname);
      
      binmax = h2->GetMaximumBin();
      x = h2->GetXaxis()->GetBinCenter(binmax);  
      range_min = x - (2*h2->GetRMS());
      range_max = x + (2*h2->GetRMS());
      fgaus = new TF1("fgaus","gaus",range_min,range_max);
      h2->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
      h2->Fit("fgaus","R");
      fgaus->GetParameters(&par[0]);
      cell_corr[i-17] = i ;
      width_corr[i-17] = par[2];
      peakvalue_corr[i-17] = par[1];
      c1->cd();
      gStyle->SetOptFit(1111111); 
      h2->Draw();
      c1->SaveAs(dirname+"/"+histoname+".pdf");
    }
    
    
    int n = 7;
    TGraph* gr = new TGraph(n,cell_corr,width_corr);
    c1->cd();
    gr->Draw("AC*");
    gr->GetXaxis()->SetTitle("Cell Number");
    gr->GetYaxis()->SetTitle("Resolution");
    gr->SetNameTitle("resolution_correctedVsCell_Amp_" + ampval , "resolution_correctedVsCell_Amp_" + ampval);
    c1->SaveAs(dirname+"/resolution_correctedVsCell_Amp_" + ampval+".pdf");
    c1->SaveAs(dirname+"/resolution_correctedVsCell.pdf");
    fout->cd();  
    gr->Write();  
    
    for (int i=0; i<=6; i++){
      ftext<<    cell_corr[i]  << " " << energy <<" "<<ampval<< " "<<peakvalue_corr[i]<<" "<<width_corr[i]<<std::endl;
    }
    
  }
  



  //return width_corr;
}

void FitCode(){
  //  TString radiation_length_ = "_GeV_5_7_X0";  
  TString radiation_length_ = "_GeV_10_X0";  
  gSystem->Exec("rm Resolution_TimeCorrected"+radiation_length_+".txt");
  gSystem->Exec("rm Resolution_Time"+radiation_length_+".txt");
  
  std::vector<TString> energyList;
  energyList.clear();
  energyList.push_back("20");
  energyList.push_back("32");
  energyList.push_back("50");
  energyList.push_back("100");
  energyList.push_back("150");
  energyList.push_back("200");
  energyList.push_back("250");
  //float* resol;

  for (int ie = 0; ie < (int) energyList.size(); ie++){
    TString energy_ = energyList[ie];
    SaveGraphs(energy_,radiation_length_);
    //resol = SaveGraphs(energy_);
  }
  
  //std::cout<<" resol = "<<resol[0]<<" "<<resol[1]<<" "<<resol[2]<<std::endl;
}
