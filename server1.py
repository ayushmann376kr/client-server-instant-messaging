import socket
import threading

# Server information
host = '127.0.0.1'  # Localhost
port = 22865      # Port to listen on

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse

server.bind((host, port))
server.listen()

# List to keep track of connected clients
clients = []
nicknames = []

# Broadcast a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle messages from clients
def handle_client(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            broadcast(message)  # Broadcast message to all clients
        except:
            # If client disconnects, remove them from the list and notify others
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receive messages from the server (for sending to clients)
def send_messages_from_server():
    while True:
        message = input('')  # Get input from server admin
        broadcast(f'Server: {message}'.encode('utf-8'))  # Broadcast server message

# Receive new clients
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start thread for receiving client connections
print("Server is listening...")
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start thread for sending server messages
send_messages_from_server()
