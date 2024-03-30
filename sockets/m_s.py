import types 
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
import threading
import os

host,port = ("localhost", 5002)
sel = DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host,port))
lsock.listen()
print("server listening at", (host,port))
sel.register(lsock, EVENT_READ, data=None)

clients = list()
ci=1

killThred:bool = False
def server_event_loop(sel):
    try:
        global ci
        print("server event_loop started")
        while not killThred:
            events = sel.select(timeout=None)
            for key,mask in events:
                if key.data is None:
                    # add new client
                    soc = key.fileobj
                    conn, addr = soc.accept()
                    clients.append(conn)
                    sel.register(conn, EVENT_READ | EVENT_WRITE, data={"addr":addr, "outb": b"", "inb":b"", "cid": ci})
                    ci+=1
                else :
                    # read / write clients
                    soc = key.fileobj
                    data = key.data

                    if mask & EVENT_READ:
                        recv = soc.recv(1024)
                        if recv:
                            data["inb"] += recv
                            data["outb"] += recv
                            print(f"recv {data['addr']}: "+recv.decode("utf-8"))
                            print(f"clients : {len(clients)}")
                        
                    if mask & EVENT_WRITE:
                        sent = 0
                        if data["outb"]:
                            sent = soc.send(data["outb"])
                        data['outb'] = data['outb'][sent:]
    except KeyboardInterrupt:
        print("Exiting by Keyboard Interrupt")
    except Exception as e:
        print("Exiting : ", e)
    finally:
        sel.close()

# starting event loop in a thead
        
thread = threading.Thread(target=server_event_loop, args=(sel,))
thread.start()
