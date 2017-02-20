class cellInfo:
    ''' A class to store all information related to the HGCAL cell. 
    This consist of:
    - tdc (x,y) coordinates
    - raw timing 
    - corrected timing 
    - calibrated timing 
    - amplitude
    - integral
    - 
    '''
    icell = -99
    tdcx = -999.
    tdcy = -999.
    time_ = -999.
    time_correct_ = -999.
    time_calibrate_ = -999.
    amplitude = -999.
    integral = -999.
    isneighbour = False
    def __init__(self):
        self.tdcx = -999.


    
    def Print(self):
        print(self.icell, self.tdcx, self.tdcy, self.time_, self.time_correct_, self.time_calibrate_, self.amplitude, self.integral)
        
