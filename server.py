# echo-server.py
from settings import HOST, PORT
import socket

i=1
print(socket.AF_INET)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server Listening at {HOST}:{PORT}")
    
    conn, addr = s.accept()
    
    with conn:
        print(f"Connected by {addr}")
        while True:
            
            data = conn.recv(1024)
            i += 1
            # print(i)
            if not data:
                break
            conn.sendall(data)