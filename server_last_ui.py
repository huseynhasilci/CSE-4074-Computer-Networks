import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []


nicknames = []

# broadcast
def broadcast(message):
    for client in clients:
        print(client.send(message))
        #print(client.__get__)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}")
            broadcast(message)
            if message == "request":
                print("Requested")
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
# receive
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode(FORMAT))

        clients.append(client)
        nickname = client.recv(1024)
        nicknames.append(nickname)

        print(f"Nickname ot the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode(FORMAT))
        client.send("Connected to the server".encode(FORMAT))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
# handle

print("Server Running...")
receive()