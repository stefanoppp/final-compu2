import socket
import argparse

def main(args):
    HEADER=64
    PORT=args.x
    DISCONNECT_MESSAGE=args.y
    FORMAT=args.z
    
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
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=5050,help='Numero de puerto')
parser.add_argument('--y',type=str,default='quit',help='Mensaje de desconexion')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)