set CFG_FILE="HGCALTBAnalyzer.py"
set OUTPUT_FILE="electrons_100_GeV_5_7_X0.root"
set TOP="$PWD"

#cd /afs/cern.ch/work/k/khurana/HGCALTB/CMSSW_7_1_5/src/HGCALTBAnalysis/

cd $TOP
eval `scramv1 runtime -sh`
/afs/cern.ch/work/k/khurana/HGCALTB/CMSSW_7_1_5/src/HGCALTBAnalysis/HGCALTBAnalyzer.py -e
#$TOP/$CFG_FILE -e
xrdcp /tmp/khurana/$OUTPUT_FILE root://eoscms//eos/cms//store/user/khurana/$OUTPUT_FILE

