import socket
import argparse
import multiprocessing

def main(args):
    HEADER=64
    PORT=args.x
    FORMAT=args.z

    ADDR=('::1',PORT)
    CONNECTED=True
    client=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    client.connect(ADDR)

    parent_conn, child_conn = multiprocessing.Pipe()

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
        parent_conn.send(server_msj)

    parent_conn.close()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--x',type=int,default=5050,help='Numero de puerto')
    parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
    args=parser.parse_args()
    main(args)
