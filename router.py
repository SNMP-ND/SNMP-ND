# Class representing a Router

from interface import Interface

class Router:
    sysName : str
    ospfNeighborsIPs : list
    interfaces : list

    def __init__(self, sysName):
        self.sysName = sysName
        self.ospfNeighborsIPs = []
        self.interfaces = []
    
    def __str__(self):
        return f'Router {self.sysName}: Neighbors: {self.ospfNeighborsIPs}, interfaces: {self.interfaces}'

    def setNeighbors(self, neighbors : list):
        self.ospfNeighborsIPs = neighbors
    
    def setInterfaces(self, interface : list):
        self.interfaces = interface
    