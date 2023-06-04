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
    
    def getMask(self):
        return self.mask
    
    def isLinkedWith(self, interface: 'Interface') -> bool:
        # First check if the interfaces are up
        if (self.status != 'up' or interface.getStatus() != 'up'):
            return False
        # Then check if they are in the same subnet
        if (self.mask != interface.getMask()):
            return False
        # Finally, check if they are in the same network depending on the mask
        ip1 = self.ip.split('.')
        ip2 = interface.getIP().split('.')
        # Check if the IPs are valid
        if (len(ip1) != 4 or len(ip2) != 4):
            return False
        mask = self.mask.split('.')
        for i in range(0, 4):
            if (int(ip1[i]) & int(mask[i]) != int(ip2[i]) & int(mask[i])):
                return False
        return True
    