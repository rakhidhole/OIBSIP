import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

# Bind and listen
server_socket.bind((host, port))
server_socket.listen(1)
print("Server started, waiting for client...")

conn, addr = server_socket.accept()
print(f"Connected to {addr}")

while True:
    message = input("You: ")
    conn.send(message.encode())

    received = conn.recv(1024).decode()
    if received.lower() == 'exit':
        print("Client left the chat.")
        break
    print(f"Client: {received}")

conn.close()
