import socket
HEADER=64
PORT=5050
FORMAT='utf-8'
DISCONNECT_MESSAGE="quit"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
CONNECTED=True
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

while CONNECTED:
    msg=input("Nombre de foto: ")    
    
    def send(msg):
        message=msg.encode(FORMAT)
        msg_length=len(message)
        send_length=str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER-len(send_length))
        client.send(send_length)
        client.send(message)
        server_msj=client.recv(2048).decode(FORMAT)
        print(server_msj)
    send(msg)
    if msg==DISCONNECT_MESSAGE:
        break