import os
import socket
import threading
from rsa_t import *
from aes_des import *


# Function to handle client connections
def handle_client(client_socket, client_address, key, isAES):
    n = client_socket.recv(1024)
    e = client_socket.recv(1024)
    pub = (int(n.decode()), int(e.decode()))
    #print("Public Key Received")
    enc_key = encrypt(key, pub)
    client_socket.send(enc_key)
    #print("Private Key Sent")
    client_socket.send(encrypt(isAES, pub))
    #print("AES Key Sent")
    print(f"Tried {client_address}")

    try:
        while True:
            message = client_socket.recv(4096)
            if not message:
                break
            # Broadcast message to all clients
            broadcast(message, client_socket)
    except Exception as e:
        #print(f"Error: {e}")
        pass
    finally:
        client_socket.close()
        print("User Disconnected")

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except Exception as e:
                #print(f"Error broadcasting message: {e}")
                # If there's an error broadcasting, assume client disconnected
                client_socket.close()
                del clients[client_socket]
                print("Client Disconnected")

def mssgEnc_INIT():
    type = input("Select an Encryption Type: (1) AES or (2) DES: ")
    if type == "1":
        isAES = True
    elif type == "2":
        isAES = False
    else: 
        print("Invalid input.")
        return mssgEnc_INIT()

    passphrase = input("Enter a passphrase: ")
    
    if " " in passphrase or not passphrase.isascii():
        print("Invalid input.")
        return mssgEnc_INIT()
    else:
        aes_des = AES_DES(isAES)
        key = AES_DES.generate_key(passphrase, os.urandom(16), key_length=32)  
    return key, isAES

# Main code
if __name__ == "__main__":
    # Initialize server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    
    server.listen(5)
    print("Server is listening...")

    clients = {}  # To store connected clients
    key, isAES = mssgEnc_INIT()
    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, key, isAES))
            client_thread.start()
            clients[client_socket] = client_address
    except KeyboardInterrupt:
        print("Shutting down server...")
        for client_socket in clients:
            client_socket.close()
        server.close()