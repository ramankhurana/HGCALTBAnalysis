t1065->Draw("linearTime45[0]:linearTime45[8]","linearTime45[0]>0 && linearTime45[8]>0")
t1065->Draw("TDCx:TDCy","fabs(TDCx)<50 && fabs(TDCy)<50","colz")
t1065->Draw("linearTime45[17]-linearTime45[16]", "linearTime45[17]>0 && linearTime45[17]<40 && amp[17]>0.02 && abs(linearTime45[17]-linearTime45[16]) <20 ","colz")
