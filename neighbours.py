class neighbours:
    
    def __init__(self):
        ''' do nothing '''
        

    def isNeighbour17(self, icell):
        isneighbour = False
        if (icell == 18) | (icell == 19) | (icell == 20) | (icell == 21) | (icell == 22) | (icell == 23) :
            isneighbour = True
        return isneighbour
    
    def isNeighbour18(self, icell):
        isneighbour = False
        if (icell == 17) | (icell == 19) | (icell == 23) :
            isneighbour = True
        return isneighbour

    def isNeighbour19(self, icell):
        isneighbour = False
        if (icell == 17) | (icell == 18) | (icell == 20) :
            isneighbour = True
        return isneighbour

    def isNeighbour20(self, icell):
        isneighbour = False
        if (icell == 17) | (icell == 19) | (icell == 21) :
            isneighbour = True
        return isneighbour

        
    def isNeighbour21(self, icell):
        isneighbour = False
        if (icell == 17) | (icell == 20) | (icell == 22) :
            isneighbour = True
        return isneighbour

    def isNeighbour22(self, icell):
        isneighbour = False
        if (icell == 17) | (icell == 21) | (icell == 23) :
            isneighbour = True
        return isneighbour
    
    def isNeighbour23(self, icell):
        isneighbour = False
        if (icell == 17) | (icell == 18) | (icell == 22) :
            isneighbour = True
        return isneighbour
    
    def isNeighbour(self, icenter, icell):
        isneighbour = False
        if icenter == 17:
            isneighbour = self.isNeighbour17(icell)
        elif icenter == 18:
            isneighbour = self.isNeighbour18(icell)
        elif icenter == 19:
            isneighbour = self.isNeighbour19(icell)
        elif icenter == 20:
            isneighbour = self.isNeighbour20(icell)
        elif icenter == 21:
            isneighbour = self.isNeighbour21(icell)
        elif icenter == 22:
            isneighbour = self.isNeighbour22(icell)
        elif icenter == 23:
            isneighbour = self.isNeighbour23(icell)
        else: isneighbour = False
        return isneighbour

            
            
