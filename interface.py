# Class representing an Interface

class Interface:
    index : int
    description : str
    status : str
    speed : int
    ip : str

    def __init__(self, index, description, status, speed, ip):
        self.index = index
        self.description = description
        self.status = status
        self.speed = speed
        self.ip = ip

    def __str__(self):
        return f'Interface {self.index}: {self.description}, {self.status}, {self.speed}, {self.ip}'
    