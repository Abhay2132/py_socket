import socket
import selectors
import types
import threading


from settings import HOST, PORT

class SocketManager:

    killThread:bool = False
    sock=False
    def __init__(self, onData) -> types.NoneType:
        self.onData = onData
        self.sel = selectors.DefaultSelector()
        
        # first try to connect as client 
        # if server not found
        # then be a server

        print("Trying to connect as a client")
        
        server_addr = (HOST, PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.data = types.SimpleNamespace(
            outb=b"",
        )
        self.sel.register(self.sock, events, data=self.data)

        self.thread = threading.Thread(target=clientEventLoop, args=(self.sel, self))
        self.thread.start()
        
    def onClientFail(self):
        # now make a server
        print("Starting server")
        self.killThread = True
        try:
            self.thread.join()
        except Exception as e:
            print(e)

        # making new socket
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((HOST,PORT))
        self.lsock.listen()
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        self.thread = threading.Thread(target=server_event_loop, args=(self,))
        self.thread.start()
    
    def sendData(self, data=None, target=None):
        if bool(data):
            self.data.outb += str.encode(data)
            return
        
        if self.sock and self.data.outb :
            count = self.sock.send(self.data.outb)
            self.data.outb = self.data.outb[count:]
        pass

def clientEventLoop(sel:selectors.DefaultSelector, sm:SocketManager):
    try:
        while not sm.killThread:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    client_service_connection(key, mask, sm)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except Exception as e:
        print("ERROR : HEHE")
        print(e)
    finally:
        sel.unregister(key.fileobj)
        key.fileobj.close()
        sm.onClientFail()
        
def client_service_connection(key, mask, sm:SocketManager):
    sock = key.fileobj
    data = key.data
    # print(repr(data))   
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        recv_data and sm.onData(recv_data)
    if mask & selectors.EVENT_WRITE:
        # sock.send(b"1")
        sm.sendData()


def server_event_loop(sm:SocketManager):
    print("RUNNING SERVER EVENT LOOP")
    try:
        while True:
            events = sm.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj, sm)
                else:
                    service_connection(key, mask, sm)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    except ConnectionResetError:
        print("Client Disconnected")
    finally:
        sm.sel.unregister(key.fileobj)
        key.fileobj.close()
        sm.onClientFail()

def accept_wrapper(sock, sm:SocketManager):
    conn, addr = sock.accept()  # Should be ready to read
    sm.conn = conn
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    sm.data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sm.sel.register(conn, events, data=sm.data)

def service_connection(key, mask, sm:SocketManager):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        handleData(b"server received : "+recv_data)
        if recv_data:
            data.outb += recv_data

        else:
            pass
            # print(f"Closing connection to {data.addr}")
            # sm.sel.unregister(sock)
            # sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sm.sendData(input(">>> "))
            # print(f"Echoing {data.outb!r} to {data.addr}")
            # sent = sock.send(data.outb)  # Should be ready to write
            # data.outb = data.outb[sent:]


import time
def handleData(data):
    time.sleep(0.5)
    print(data)

if __name__ == "__main__":
    sm = SocketManager(handleData)

    while True:
        try:
            sm.sendData(input(">> "))
        except KeyboardInterrupt:
            sm.killThread = True


