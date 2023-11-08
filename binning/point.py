class Point():
    def __init__(self, id, energy, theta, phi, scatter, path):
        self.id = id
        self.energy = energy
        self.theta = theta
        self.phi = phi
        self.scatter = scatter
        self.path = path
    
    def getEventID(self):
        return self.id
    
    def getEnergy(self):
        return self.energy
    
    def getTheta(self):
        return self.theta
    
    def getPhi(self):
        return self.phi
    
    def getScatterAngle(self):
        return self.scatter
    
    def getPathLength(self):
        return self.path
