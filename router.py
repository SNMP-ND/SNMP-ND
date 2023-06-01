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
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Router):
            return self.sysName == __value.sysName
        return False

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
    
    def getInterfacesIP(self):
        interfacesIP = []
        for interface in self.interfaces:
            interfacesIP.append(interface.getIP())
        return interfacesIP
    