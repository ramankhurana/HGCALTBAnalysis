class calibrationReader:
    
    filename=''
    mean=0.0
    sigma=0.0
    def __init__(self, calibrationfile):
        self.filename = calibrationfile
        

        
    def findampBin(self, iamp):
        amplitudeBins_=[[0.00,0.02], [0.02,0.04], [0.04, 0.06], [0.06, 0.08], [0.08, 0.1], [0.1, 0.12], [0.12, 0.14], [0.14, 0.16], [0.16, 0.18], [0.18, 0.20], [0.20, 0.25], [0.25, 0.30], [0.30, 0.35], [0.35, 0.40], [0.40, 0.48]]
        amplitudeCut_=[0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.225, 0.275, 0.325, 0.375, 0.44]
        
        ampbin = 0.0 
        j = 0
        for iampbin in amplitudeBins_:
            amplow = iampbin[0]
            amphi =  iampbin[1]
            iampcut = amplitudeCut_[j]
            
            j  = j +1 
            if (iamp > amplow) & (iamp < amphi):
                ampbin = iampcut 
                break; 
        return ampbin
    
    def CalibationFactor(self, icell, iamp):
        iampbin = self.findampBin(iamp)
        calib = open( self.filename, 'r')
        lineList=[]
        for iline in calib:
            lineList =  (iline.rstrip()).split(' ')
            if ( (lineList[0] == str(icell)) & (lineList[1] == str(iampbin)) ):
                self.mean  = lineList[2]
                self.sigma = lineList[3]
        return [self.mean,self.sigma]

'''
if __name__ == "__main__":
    calb = calibrationReader('data/Resolution.txt')
    print calb.CalibationFactor(21,0.05)



'''
