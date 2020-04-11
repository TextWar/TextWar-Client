import json
from textwar import sender

"""
    The Packet for client,all dataPackets must impl it
    
    author: magiclu550 
"""

class Packet:

    def __init__(self,type,action):
        self.type = type
        self.data = {'type':type,'action':action}

    def add(self,key,value):
        """add the value for json"""
        self.data[key] = value

    def dump(self):
        """get json object"""
        json.dumps(self.data)

    def compile(self):
        self.register()
        sender.get_format(self.dump())
    def register(self):
        """overwrite it"""
        pass


"""
    The packet type is player
"""
class PlayerPacket(Packet):

    def __init__(self,action):
        super().__init__("player",action)


"""
    the type is player,the action is about player joining    
"""
class PlayerJoinPacket(PlayerPacket):
    def __init__(self,action,name,password,rad):
        super().__init__(action)
        self.name = name
        self.password = password
        self.rad = rad
        self.action = action

    def register(self):
        self.add("name",self.name)
        self.add("password",self.password)
        self.add("rad",self.rad)

class PlayerRegisterPacket(PlayerJoinPacket):

    def __init__(self,name,password,rad):
        super().__init__("register",name,password,rad)
        self.name = name
        self.password = password
        self.rad = rad

class PlayerLoginPacket(PlayerJoinPacket):

    def __init__(self,name,password,rad):
        super().__init__("login",name,password,rad)
        self.name = name
        self.password = password
        self.rad = rad

