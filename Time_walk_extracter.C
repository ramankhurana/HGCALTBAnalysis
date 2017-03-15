void SaveGraphs(  TString energy = "250", TString X0){

  TString filename = "histogramsOffSetExtraction/electrons_"+energy+"_GeV_"+X0+".root";
  cout << filename <<std::endl;
  TString dirname = "histogramsPDF/Dir_TimeWalk_"+energy;
  gSystem->Exec("mkdir "+dirname);
  
  TString fileout = "histogramsRootFile/Timewalk_Extracter_"+energy+"_GeV_"+X0+".root";
  TFile *fout = new TFile(fileout,"recreate");
  TFile *f1 = new TFile(filename,"open");
  f1->cd();
  TString cellnumber,cellnumber__, histoname;
  TString nameofhisto,histo2D;
  double range_min, range_max,x;
  int binmax;
  double par[3];

  TCanvas *c1 = new TCanvas ("c1","c1", 700, 500);
  TF1 *fgaus;

  TH3F *h4;
  TH1D *projectionh;
  //TDCx Vs time

  const int RCell = 15;
  double width[RCell], cell[RCell],mean[RCell];
  int j ;
  int startbin, endbin divison;
  histo2D = "h3_amp_time_cell_";
  h4 = (TH3F*) f1->Get(histo2D);
  h4->Draw();
  ofstream ftext;
  TString plottname = "data/offset_and_timewalk_E_"+energy+"_GeV_"+X0+".txt";
  ftext.open(plottname);
  for(int cellN = 1; cellN <=7; cellN++){
    startbin = 16+cellN;
    cellnumber.Form("%d",startbin);
    j =0 ;
    int gap_ = 0;
    bool isbin_ = false;
    int binnumber_ = 0;
    for (int i = 0 ; i <= 95; i ++ ){
      isbin_ = false;
      if( i < 40 && (i%4 ==0)){ gap_ = i+4; 
	projectionh = h4->ProjectionY("projectionh",i+1,gap_,cellN,cellN);
	isbin_ = true;
      }
      if ( i >=40 && (i%10 ==0) && i < 80){ gap_ = i+10;
	projectionh = h4->ProjectionY("projectionh",i+1,gap_,cellN,cellN);
	isbin_ = true;
      }
      if ( i == 95){
	projectionh = h4->ProjectionY("projectionh",80,i,cellN,cellN);
	isbin_ = true;
      }
      
      if (!isbin_)  continue; 
      binnumber_= (i+1 +gap_)/2;
      cout << " j " <<j << "   " <<binnumber_*0.05 <<std::endl;     
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
      cell[j]= binnumber_*0.005;
      ftext<<    cellnumber  << " " << binnumber_*0.005 <<" " <<mean[j]<<" "<<width[j]<<std::endl;
      //      cout << cell[j]  <<"   " <<width[j] <<std::endl;
      j++;
      c1->cd();
      gStyle->SetOptFit(1111111); 
      projectionh->Draw();
      cellnumber__.Form("%d",i);
      nameofhisto = histo2D+"_Cell_"+cellnumber+"_Amp_"+cellnumber__;
      c1->SaveAs(dirname+"/"+nameofhisto+".pdf");
    }
    
    TGraph* gr = new TGraph(15,cell,width);
    c1->cd();
    gr->Draw("AC*");
    gr->SetNameTitle("Resolution_"+cellnumber,"Resolution_"+cellnumber);
    gr->GetXaxis()->SetTitle("Cell ");
    gr->GetYaxis()->SetTitle("Resolution");
    
    c1->SaveAs(dirname+"/resolutionVscell_"+cellnumber+".pdf");
    fout->cd();  
    gr->Write();  

    TGraph* grmean = new TGraph(15,cell,mean);
    c1->cd();
    grmean->Draw("AC*");
    grmean->SetNameTitle("MeanValue_"+cellnumber,"MeanValue_"+cellnumber);
    grmean->GetXaxis()->SetTitle("Cell ");
    grmean->GetYaxis()->SetTitle("Mean");
    
    c1->SaveAs(dirname+"/MeanValue_"+cellnumber+".pdf");
    fout->cd();  
    grmean->Write();
  }
    

}

void Time_walk_extracter(){
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

  std::vector<TString> X0;
  X0.clear();
  X0.push_back("5_7_X0");
  X0.push_back("10_X0");
  
  for (int ix0 = 0; ix0 < 2; ix0++){
    for (int ie = 0; ie < (int) energyList.size(); ie++){
      TString energy_ = energyList[ie];
      SaveGraphs(energy_, X0[ix0]);
      //resol = SaveGraphs(energy_);
    }
  }
  
  //std::cout<<" resol = "<<resol[0]<<" "<<resol[1]<<" "<<resol[2]<<std::endl;
}
