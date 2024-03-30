import socket

# Define the host and port on which the server will listen
HOST = '192.168.137.1'
PORT = 8080

# Define a simple HTTP response
RESPONSE = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
<title>Simple Web Server</title>
</head>
<body>
<h1>Hello, World!</h1>
<p>This is a simple web server implemented in Python using sockets.</p>
</body>
</html>
"""

def run_server():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        # Listen for incoming connections
        server_socket.listen()

        print(f"Server listening on {HOST}:{PORT}")

        while True:
            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            with client_socket:
                # Receive data from the client
                request = client_socket.recv(1024).decode('utf-8')
                print(f"Received request:\n{request}")

                # Send the HTTP response to the client
                client_socket.sendall(RESPONSE.encode('utf-8'))

                print("Response sent")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("Exiting KEYBOARD INTERRUPT")
        import  sys
        sys.exit(1)
