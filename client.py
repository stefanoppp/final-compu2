import socket
import argparse
def main(args):
    HEADER=64
    PORT=args.x
    FORMAT=args.z
    
    # SERVER=socket.gethostbyname(socket.gethostname())
    ADDR=('::1',PORT)
    CONNECTED=True
    client=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    client.connect(ADDR)
  
    while CONNECTED:
        msg=input("Nombre de foto: ")    
        message=msg.encode(FORMAT)
        msg_length=len(message)
        send_length=str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER-len(send_length))
        client.send(send_length)
        client.send(message)
        server_msj=client.recv(2048).decode(FORMAT)
        if server_msj=='Disconnect capacity':
            print("Usted ha sido desconectado por exceso de demanda")
            client.close()
            break
        if server_msj=='Disconnect':
            print('Hasta luego!')
            client.close()
            break
        print(server_msj)

        
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=5050,help='Numero de puerto')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)