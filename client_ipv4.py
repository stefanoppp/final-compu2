import socket
import argparse
from authenticate import main_log_process

def main(args):
    def login():
        user=input("Usuario: ")
        passw=input("Clave: ")
        log=main_log_process(user,passw)
        return log
    
    access=login()  

    if access:
        print("Logeo exitoso!")
        HEADER=64
        PORT=args.x
        FORMAT=args.z
        SERVER=socket.gethostbyname(socket.gethostname())
        ADDR=(SERVER,PORT)
        CONNECTED=True
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(ADDR)
        while CONNECTED:
            
            def send(msg):
                message=msg.encode(FORMAT)
                msg_length=len(message)
                send_length=str(msg_length).encode(FORMAT)
                send_length += b' '*(HEADER-len(send_length))
                client.send(send_length)
                client.send(message)
                server_msj=client.recv(2048).decode(FORMAT)
                return server_msj
            
            if True:
                msg=input("Nombre de foto: ")

                server_msj=send(msg)

                if server_msj=='Disconnect capacity':
                    print("Usted ha sido desconectado por exceso de demanda")
                    client.close()
                    break
                if server_msj=='Disconnect':
                    print('Hasta luego!')
                    client.close()
                    break
                
                print(server_msj)
    else:
        print("Acceso denegado")

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--x',type=int,default=5051,help='Numero de puerto')
    parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
    args=parser.parse_args()
    main(args)