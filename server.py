import socket
import threading


# cabecera de los mensajes que seran enviados en bytes
HEADER=64
PORT=5050
FORMAT='utf-8'
DISCONNECT_MESSAGE="quit"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# creamos server
server.bind(ADDR)

# metodo para manejar las comunicaciones entre cliente y servidor. Se ejecuta
# una vez por cada cliente
def handle_client(conn,addr):
    connected=True
    print(f"Nuevo cliente conectado. Direccion {addr}")
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MESSAGE:
                connected=False
            print(f"Usuario {addr} dice {msg}")
    conn.close()    
    
def start():
    print("Servidor escuchando...")
    server.listen()
    while True:
        # cuando hay una nueva conexin, creamos un thread con la funcion handle client
        conn, addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        
start()