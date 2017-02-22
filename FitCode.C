void SaveGraphs(  TString energy = "250"){

  

  TString filename = "electrons_"+energy+"_GeV_5_7_X0.root";
  cout << filename <<std::endl;
  TString dirname = "Dir_"+energy;
  gSystem->Exec("mkdir "+dirname);
  
  TString fileout = "Output_"+energy+".root";
  TFile *fout = new TFile(fileout,"recreate");
  TFile *f1 = new TFile(filename,"open");
  f1->cd();
  TString cellnumber, histoname;
  TString histo2D;
  double range_min, range_max,x;
  int binmax;
  double par[3];
  double width[7], cell[7];
  double width_corr[7], cell_corr[7];
  TCanvas *c1 = new TCanvas ("c1","c1", 700, 500);
  TF1 *fgaus;
  

  //TDCx Vs TDCy
  for (int j=17; j<=23; j++){
    cellnumber.Form("%d",j);
    histo2D = "TDCxVsTDCy_withAmpCut_"+cellnumber;
    TH2F *h4 = (TH2F*) f1->Get(histo2D);
    c1->cd();
    h4->GetXaxis()->SetTitle("TDCx");
    h4->GetYaxis()->SetTitle("TDCy");
    //    h4->SetOptStat(0);

    h4->Draw("colz");
    c1->SaveAs(dirname+"/"+histo2D+".pdf");

  }

  //TDCx Vs time
  for (int j=17; j<=23; j++){
    cellnumber.Form("%d",j);
    histo2D = "h2_TDCx_vs_time_"+cellnumber;
    TH2F *h4 = (TH2F*) f1->Get(histo2D);
    c1->cd();
    h4->GetXaxis()->SetTitle("TDCx");
    h4->GetYaxis()->SetTitle("time");
    h4->Draw("colz");
    c1->SaveAs(dirname+"/"+histo2D+".pdf");

  }

  //TDCy Vs time
  for (int j=17; j<=23; j++){
    cellnumber.Form("%d",j);
    histo2D = "h2_TDCy_vs_time_"+cellnumber;
    TH2F *h4 = (TH2F*) f1->Get(histo2D);
    c1->cd();
    h4->GetXaxis()->SetTitle("TDCy");
    h4->GetYaxis()->SetTitle("time");
    h4->Draw("colz");
    c1->SaveAs(dirname+"/"+histo2D+".pdf");

  }


  //TDCx Vs amp
  for (int j=17; j<=23; j++){
    cellnumber.Form("%d",j);
    histo2D = "h2_TDCx_vs_amp_"+cellnumber;
    TH2F *h4 = (TH2F*) f1->Get(histo2D);
    c1->cd();
    h4->GetXaxis()->SetTitle("TDCx");
    h4->GetYaxis()->SetTitle("amp");
    h4->Draw("colz");
    c1->SaveAs(dirname+"/"+histo2D+".pdf");

  }


  //TDCx Vs amp
  for (int j=17; j<=23; j++){
    cellnumber.Form("%d",j);
    histo2D = "h2_TDCy_vs_amp_"+cellnumber;
    TH2F *h4 = (TH2F*) f1->Get(histo2D);
    c1->cd();
    h4->GetXaxis()->SetTitle("TDCy");
    h4->GetYaxis()->SetTitle("amp");
    h4->Draw("colz");
    c1->SaveAs(dirname+"/"+histo2D+".pdf");

  }




  TH2F *h4 = (TH2F*) f1->Get("TDCmap_");
  c1->cd();
  h4->GetXaxis()->SetTitle("TDCx");
  h4->GetYaxis()->SetTitle("TDCy");
  //h4->SetOptStat(000000);
  h4->Draw("colz");
  c1->SaveAs(dirname+"/TDCMap_.pdf");

  gStyle->SetOptStat(111111);
  gROOT->ForceStyle(); 



  //Total Time resolution
    histoname = "h_Totaltime";
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

    // Quad
    histoname = "h_Totaltime_Quad";
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

    histoname = "h_Totaltime_Log";
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
  

  for ( int i = 17; i <= 23; i++){
    par[0] =  par[1]= par[2] = 0;
    cellnumber.Form("%d",i);
    histoname = "TimePlot_"+cellnumber;
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
    c1->cd();
    gStyle->SetOptFit(1111111); 
    h2->Draw();
        
    c1->SaveAs(dirname+"/"+histoname+".pdf");
  }

  

  for ( int i = 17; i <= 23; i++){
    par[0] =  par[1]= par[2] = 0;
    cellnumber.Form("%d",i);
    histoname = "TimeCorrected_"+cellnumber;
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
    c1->cd();
    gStyle->SetOptFit(1111111); 
    h2->Draw();
    c1->SaveAs(dirname+"/"+histoname+".pdf");
  }

  int n = 7;
  TGraph* gr = new TGraph(n,cell,width);
  c1->cd();
  gr->Draw("AC*");
  gr->GetXaxis()->SetTitle("Cell Number");
  gr->GetYaxis()->SetTitle("Resolution");
  
  c1->SaveAs(dirname+"/resolutionVsCell.pdf");
  fout->cd();  
  gr->Write();  

  TGraph* gr = new TGraph(n,cell_corr,width_corr);
  c1->cd();
  gr->Draw("AC*");
  gr->GetXaxis()->SetTitle("Cell Number");
  gr->GetYaxis()->SetTitle("Resolution");
  c1->SaveAs(dirname+"/resolution_correctedVsCell.pdf");
  fout->cd();  
  gr->Write();  


  ofstream ftext;
  ftext.open("Resolution.txt");
  for (int i=0; i<=6; i++){
    ftext<<    cell_corr[i]  << " " << energy <<" "<<width_corr[i]<<std::endl;
  }

  //return width_corr;
}

void FitCode(){
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
    SaveGraphs(energy_);
    //resol = SaveGraphs(energy_);
  }
  
  //std::cout<<" resol = "<<resol[0]<<" "<<resol[1]<<" "<<resol[2]<<std::endl;
}
