# Class representing an Interface

class Interface:
    index : int
    description : str
    status : str
    speed : int
    ip : str
    mask : str

    def __init__(self, index, description, status, speed, ip, mask):
        self.index = index
        self.description = description
        self.status = status
        self.speed = speed
        self.ip = ip
        self.mask = mask

    def __str__(self):
        return f'Interface {self.index}: {self.description}, {self.status}, {self.speed}, {self.ip}, {self.mask}'
    
    # Getters
    def getIndex(self):
        return self.index
    
    def getDescription(self):
        return self.description
    
    def getStatus(self) -> str:
        return self.status
    
    def getSpeed(self):
        return self.speed
    
    def getIP(self):
        return self.ip
    