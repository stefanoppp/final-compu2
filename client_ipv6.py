import socket
import argparse
from multiprocessing import Queue
from authenticate import main_log_process

def main(args):
    users_queue=Queue()
    passwords_queue=Queue()
    
    def login():
        user=input("Usuario: ")
        passw=input("Clave: ")

        users_queue.put(user)
        passwords_queue.put(passw)
    
        log=main_log_process(users_queue.get(),passwords_queue.get())
        return log
    
    access=login()  

    if access:
        print("Logeo exitoso!")
        HEADER=64
        PORT=args.x
        FORMAT=args.z
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
    else:
        print("Acceso denegado")
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--x',type=int,default=8080,help='Numero de puerto')
    parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
    args=parser.parse_args()
    main(args)
