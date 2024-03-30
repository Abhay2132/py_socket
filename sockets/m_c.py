import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
import threading

a=True
host,port = ("localhost", 5002)
# client conn

csel = DefaultSelector()
csoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csoc.setblocking(False)
csoc.connect_ex((host,port))
events = EVENT_WRITE | EVENT_READ
csel.register(csoc, events, data={"inb":b"", "outb":str.encode(input(">> "))})

# this function runs in a thread
def client_event_loop(csel:DefaultSelector):
    global a
    try:
        while True:
            events = csel.select(timeout=None)
            for key, mask in events:
                sock = key.fileobj
                # print(sock is csoc)
                data = key.data
                if mask & EVENT_READ:
                    if a:print("READ"); a=False
                    recv_data = sock.recv(1024)  # Should be ready to read
                    if recv_data:
                        print(f"<< {recv_data!r}")
                        data["inb"] += recv_data
                if mask & EVENT_WRITE:
                    if a:
                        print("Write")
                        a=False

                    if not data['outb']:
                        data['outb'] = str.encode(input(">> "))
                    if data['outb']:
                        sent = sock.send(data['outb'])  # Should be ready to write
                        data['outb'] = data['outb'][sent:]
        pass
    except KeyboardInterrupt:
        print("exiting (client) by keyboard interrupt")
    except Exception as e:
        print("Exiting (client): " , e)
    finally:
        csel.close()


#starting client event loop

cthread = threading.Thread(target=client_event_loop, args=(csel,))
cthread.start()