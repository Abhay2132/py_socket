from Socket import ClientSocket
from ui import APP
from settings import PORT, getWIFI

addr = (getWIFI(), PORT)
class Client(APP):
    clientSocket = None

    def __init__(self):
        super().__init__("CLIENT", "Client")
        print(f"Connecting to {addr}")
        self.clientSocket = ClientSocket(addr)
        self.clientSocket.connect()
        self.clientSocket.on("data", self.receiveMessage)
    
    def postMessage(self):
        for message in self.pendingMessages:
            self.clientSocket.send(bytes(message, encoding='utf-8'))
        self.pendingMessages.clear()
    
    def receiveMessage(self, args):
        print(args)
        text = args[0]
        message = text.decode("utf-8")
        return super().receiveMessage(message, "SERVER")


if __name__ == "__main__":
    client = Client()
    client.show()

