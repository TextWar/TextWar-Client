from textwar.parser import Client

class ClientNetwork:

    def start(self,ip,port):
        self.client = Client(ip,port)
        self.client.start("")

    def send(self):
        self.client.out()
