void SaveGraphs(  TString energy = "250", TString radiation_length ="_GeV_5_7_X0"){
  TString filename = "histogramsRootFile_1/electrons_"+energy+radiation_length+".root";
  cout << filename <<std::endl;
  TString dirname = "DirCombine_ncellscom"+energy+radiation_length;
  gSystem->Exec("mkdir "+dirname);
  
  TString fileout = "OutputCombine_ncellscom"+energy+radiation_length+".root";
  TFile *fout = new TFile(fileout,"recreate");
  TFile *f1 = new TFile(filename,"open");
  f1->cd();
  TString cellnumber, histoname ,ampval;
  TString histo2D;
  double range_min, range_max,x;
  int binmax;
  double par[3];
  double width[7], cell[7];
  double width_corr[7], cell_corr[7];
  TCanvas *c1 = new TCanvas ("c1","c1", 700, 500);
  TF1 *fgaus;
  
  TString ncellscom ;
  //Total Time resolution
  ofstream ftext;
    ftext.open("CombineResolution_DifferentAmplitude_ncellscom"+radiation_length+".txt",std::fstream::app);
  for (int j =1; j<=7; j++){
    ncellscom.Form("%d",j);
    for (int iamp=0; iamp<=90; iamp=iamp+5){
      par[0] =  par[1]= par[2] = 0;
      ampval.Form("%d",iamp);
      if(j==1){
	histoname = "h_Totaltime_Amp_0_AmpTh_" + ampval ;}
      else if( j>1){
	histoname = "h_Totaltime_Amp_0_AmpTh_" + ampval+"_"+ncellscom ;}
      // h_Totaltime_Amp_0_AmpTh_55_2, _3, _4, _5, _6, _7
      TH1F *h2 = (TH1F*) f1->Get(histoname);
      
      binmax = h2->GetMaximumBin();
      x = h2->GetXaxis()->GetBinCenter(binmax);  
      h2->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
      fgaus = new TF1("fgaus","gaus",range_min,range_max);
      cout << "RMS + "<< h2->GetRMS() <<std::endl;
      range_min = x - (1*h2->GetRMS());
      range_max = x + (1*h2->GetRMS());
      
      h2->Fit("fgaus","R");
      fgaus->GetParameters(&par[0]);
      c1->cd();
      gStyle->SetOptFit(1111111); 
      h2->Draw();
      c1->SaveAs(dirname+"/"+histoname+".pdf");
      ftext<<ncellscom<<" "<< energy <<" "<<iamp<< " "<<par[1]<<" "<<par[2]<<std::endl;
    }
  }
}

void Fitting_CombineRes(){
  //TString radiation_length_ = "_GeV_5_7_X0";
  TString radiation_length_ = "_GeV_10_X0";
  gSystem->Exec("rm CombineResolution_DifferentAmplitude_ncellscom"+radiation_length_+".txt");
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
  }
  
}
