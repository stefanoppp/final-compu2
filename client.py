import socket
import argparse
def main(args):
    HEADER=64
    PORT=args.x
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
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=5051,help='Numero de puerto')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)