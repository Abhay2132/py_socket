# multiconn-server.py

import sys
import socket
import selectors
from m_utils import accept_wrapper, service_connection
sel = selectors.DefaultSelector()
from settings import HOST, PORT
# host, port = sys.argv[1], int(sys.argv[2])
host, port = (HOST, PORT)

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# EVENT LOOP``
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(sel, key.fileobj)
            else:
                service_connection(sel, key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

# starting event loop
