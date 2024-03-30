from Socket import ServerSocket
from ui import APP
from settings import HOST, PORT

addr = (HOST, PORT)

class Server(APP):

    def __init__(self):
        super().__init__("SERVER", "Server")
        self.serverSocket = ServerSocket(addr)
        self.serverSocket.start()
        self.serverSocket.on("new-connection", self.onClient)
        self.serverSocket.on("data", self.receiveMessage)
    
    def onClient(self, clientID):
        print(f"new client : {clientID}")
    
    def postMessage(self): # broadcast message to all clients
        for i,message in enumerate(self.pendingMessages):
            for client in self.serverSocket.clients:
                self.serverSocket.broadcast(bytes(message, 'utf-8'))
            self.pendingMessages.pop(i)
    
    def receiveMessage(self, args):
        message = args[0]
        message = message.decode("utf-8")
        return super().receiveMessage(message, "USER")

if __name__ == "__main__":
    server = Server()
    server.show()