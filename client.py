import socket
import threading

# Function to receive messages from server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

# Main code
if __name__ == "__main__":
    username = input("Enter your username: ")
    
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    
    # Start receiving messages from server in a separate thread
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    
    # Continuously send messages to server
    while True:
        message = input()
        client_socket.send(f"{username}: {message}".encode())
