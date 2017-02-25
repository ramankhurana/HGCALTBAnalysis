void SaveGraphs(  TString energy = "250"){

  

  TString filename = "histogramsRootFile/electrons_"+energy+"_GeV_5_7_X0.root";
  cout << filename <<std::endl;
  TString dirname = "DirResolutionPerCell_"+energy;
  gSystem->Exec("mkdir "+dirname);
  
  TString fileout = "Output_"+energy+".root";
  TFile *fout = new TFile(fileout,"recreate");
  TFile *f1 = new TFile(filename,"open");
  f1->cd();
  TString cellnumber,cellnumber__, histoname;
  TString nameofhisto,histo2D;
  double range_min, range_max,x;
  int binmax;
  double par[3];

  double width_corr[7], cell_corr[7];
  TCanvas *c1 = new TCanvas ("c1","c1", 700, 500);
  TF1 *fgaus;

  TH3F *h4;
  TH1D *projectionh;
  //TDCx Vs time

  const int RCell = 5;
  double width[RCell], cell[RCell],mean[RCell];
  int j ;
  int startbin, endbin divison;
  histo2D = "h3_amp_time_cell_";
  h4 = (TH3F*) f1->Get(histo2D);
  h4->Draw();
  ofstream ftext;
  TString plottname = "data/Resolution_"+energy+".txt";
  ftext.open(plottname);
  for(int cellN = 1; cellN <=7; cellN++){
    startbin = 16+cellN;
    cellnumber.Form("%d",startbin);
    j =0 ;
    for (int i = 10 ; i <= 50; i = i + 10 ){
      projectionh = h4->ProjectionY("projectionh",i,95,cellN,cellN);
      binmax =projectionh->GetMaximumBin();
      
      x =projectionh->GetXaxis()->GetBinCenter(binmax);  
      range_min = x - (1.5 * projectionh->GetRMS());
      range_max = x + (1.5 * projectionh->GetRMS());
      fgaus = new TF1("fgaus","gaus",range_min,range_max);
      projectionh->GetXaxis()->SetRangeUser(x-0.2,x+0.2);
      projectionh->Fit("fgaus","R");
      fgaus->GetParameters(&par[0]);
      width[j] = par[2];
      mean[j] = par[1];
      cell[j]= j;
      ftext<<    cellnumber  << " " << (j+1)*0.05 <<" " <<mean[j]<<" "<<width[j]<<std::endl;
      //      cout << cell[j]  <<"   " <<width[j] <<std::endl;
      j++;
      c1->cd();
      gStyle->SetOptFit(1111111); 
      projectionh->Draw();
      cellnumber__.Form("%d",i);
      nameofhisto = histo2D+"_Cell_"+cellnumber+"_Amp_"+cellnumber__;
      c1->SaveAs(dirname+"/"+nameofhisto+".png");
    }
    
    TGraph* gr = new TGraph(5,cell,width);
    c1->cd();
    gr->Draw("AC*");
    gr->GetXaxis()->SetTitle("Cell ");
    gr->GetYaxis()->SetTitle("Resolution");
    
    c1->SaveAs(dirname+"/resolutionVsCell_"+cellnumber+".png");
    fout->cd();  
    gr->Write();  

    TGraph* grmean = new TGraph(5,cell,mean);
    c1->cd();
    grmean->Draw("AC*");
    grmean->GetXaxis()->SetTitle("Cell ");
    grmean->GetYaxis()->SetTitle("Mean");
    
    c1->SaveAs(dirname+"/MeanValue_"+cellnumber+".png");
    fout->cd();  
    grmean->Write();
  }
    
    


}

void CodeFitCode(){
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
