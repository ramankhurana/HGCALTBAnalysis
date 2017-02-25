class calibrationReader:
    
    filename=''
    mean=0.0
    sigma=0.0
    def __init__(self, calibrationfile):
        self.filename = calibrationfile
        

    def CalibationFactor(self, icell, iamp):
        calib = open( self.filename, 'r')
        lineList=[]
        for iline in calib:
            lineList =  (iline.rstrip()).split(' ')
            if ( (lineList[0] == str(icell)) & (lineList[1] == str(iamp)) ):
                self.mean  = lineList[2]
                self.sigma = lineList[3]
        return [self.mean,self.sigma]

'''
if __name__ == "__main__":
    calb = calibrationReader('data/Resolution.txt')
    print calb.CalibationFactor(21,0.05)



'''
