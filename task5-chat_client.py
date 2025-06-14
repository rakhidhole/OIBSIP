import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))
print("Connected to server.")

while True:
    received = client_socket.recv(1024).decode()
    print(f"Server: {received}")

    message = input("You: ")
    client_socket.send(message.encode())
    if message.lower() == 'exit':
        print("You left the chat.")
        break

client_socket.close()
