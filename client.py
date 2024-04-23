import socket
import threading
from rsa_t import *
from aes_des import *

def setup_server(username, rsa_bit_len):
    try:
        # Connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 5555))

        pub, priv = genKeys(rsa_bit_len)
        n, e = pub
        #print("Sending rsa keys...")
        client_socket.send(str(n).encode())
        client_socket.send(str(e).encode())
        global key
        key = bytes(decrypt(client_socket.recv(4096), priv))
        isAES = bool(decrypt(client_socket.recv(1024), priv))
        global aes_des 
        aes_des = AES_DES(isAES)
        print(len(key))
        # Start receiving messages from server in a separate thread
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, aes_des, key))
        receive_thread.start()

        # Continuously send messages to server
        print("Begin Messaging...")
        while True:
            message = input()
            if message.strip():  # Check if message is not empty or contains only whitespaces
                message = f"{username}: {message}"
                encrypted_message = aes_des.encrypt_m(message, key)
                client_socket.send(encrypted_message)
            else:
                print("Error: Message cannot be empty.")

    except Exception as e:
        #print(f"Error: {e}")
        pass

def receive_messages(client_socket, aes_des, key):
    try:
        while True:
            _message = client_socket.recv(4096)
            if not _message:
                break
            # Decrypt message
            decrypted_message = aes_des.decrypt_m(_message, key)
            print(decrypted_message.decode('utf-8'))
    except Exception as e:
        #print(f"Error: {e}")
        pass
    finally:
        client_socket.close()


# Main code
if __name__ == "__main__":
    rsa_bit_len = int(input("Enter RSA bit length (1024, 2048, 4096): "))
    username = input("Enter your username: ")
    setup_server(username, rsa_bit_len)
