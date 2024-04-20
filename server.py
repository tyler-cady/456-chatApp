import socket
import threading
from rsa_t import *

# Function to handle client connections
def handle_client(client_socket, client_address):
    n = client_socket.recv(1024)
    e = client_socket.recv(1024)
    pub = (int(n.decode()), int(e.decode()))
    print("keys recieved")    
    print(f"Connected {client_address}")
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(message, client_socket)
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()
        del clients[client_socket]
        print("User Disconnected")
        broadcast("User Disconnected")
        

# Function to broadcast messages to all clients
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode())

# Main code
if __name__ == "__main__":
    # Initialize server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server is listening...")

    clients = {}  # To store connected clients

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            clients[client_socket] = client_address
    except KeyboardInterrupt:
        print("Shutting down server...")
        for client_socket in clients:
            client_socket.close()
        server.close()
