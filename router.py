# Class representing a Router

class Router:
    sysName : str
    ospfNeighbors : list
    interfaces : list

    def __init__(self, sysName):
        self.sysName = sysName
        self.ospfNeighbors = []
        self.interfaces = []
    
    def __str__(self):
        return f'Router {self.sysName}: Neighbors: {self.ospfNeighbors}, interfaces: {self.interfaces}'

    # Setters
    def setNeighbors(self, neighbors : list):
        self.ospfNeighbors = neighbors
    
    def setInterfaces(self, interface : list):
        self.interfaces = interface
    

    # Getters
    def getSysName(self):
        return self.sysName
    
    def getNeighbors(self):
        return self.ospfNeighbors
    
    def getInterfaces(self):
        return self.interfaces
    