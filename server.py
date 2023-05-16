import socket
import threading
import uuid
import cv2
import argparse
from back_propagation import Back_Propagation
from querys import consulta

def main(args):
    HEADER=64
    PORT=args.x
    DISCONNECT_MESSAGE=args.y
    FORMAT=args.z

    fotos=['P1-1.jpg',
        'P2-1.jpg',
        'P1-2.jpg',
        'P2-2.jpg'
        ]

    salidas=[1,0,1,0]

    pixeles_fotos=[]
    # -----------------Imagenes
    for foto in fotos:
        image = cv2.imread(foto)
        auxiliar=[]
        for alto in image:
            for ancho in alto:
                auxiliar.append(ancho[0])
        auxiliar.append(1)
        pixeles_fotos.append(auxiliar)
        
    # -----------------
    
    back=Back_Propagation(pixeles_fotos,salidas)
    neuronas=back.main()

    semaphore=threading.BoundedSemaphore(2)

    ADDR2 = ("", PORT)
    server_ipv6 = socket.create_server(ADDR2, family=socket.AF_INET6, dualstack_ipv6=True)

    SERVER=socket.gethostbyname(socket.gethostname())
    ADDR=(SERVER,5051)
    
    server_ipv4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server_ipv4.bind(ADDR)
    def handle_client(conn,addr,access):

        connected=True
        id_con=uuid.uuid1().int
        id_con=id_con/1000000
        
        consulta(id_con)

        while connected:

            msg_length=conn.recv(HEADER).decode(FORMAT)

            if msg_length:
                
                msg_length=int(msg_length)
                msg=conn.recv(msg_length).decode(FORMAT)
                
                if msg==DISCONNECT_MESSAGE:
                    conn.send(f"Disconnect".encode(FORMAT))
                    conn.close()
                    semaphore.release()
                    connected=False
                    break

                if access==False:
                    conn.send(f"Disconnect capacity".encode(FORMAT))
                    conn.close()
                    break
                
                print(f"Usuario {addr} dice {msg}")
                
                resultado=back.foto(msg,neuronas,pixeles_fotos=[])
               
                conn.send(f"(SERVER MESSAGE). Usted dijo {msg}. El resultado es: {resultado}".encode(FORMAT))

        
    def start_server():
        print("Servidor escuchando...")
        server_ipv4.setblocking(0)
        server_ipv6.setblocking(0)
        server_ipv4.listen()
        server_ipv6.listen()

        while True:
            try:
                conn_ipv4, addr_ipv4 = server_ipv4.accept()
                print(f"Nuevo cliente IPv4 conectado. Direccion {addr_ipv4}")
                access = semaphore.acquire(blocking=False)
                threading.Thread(target=handle_client, args=(conn_ipv4, addr_ipv4, access)).start()
            except:

                pass

            try:
                conn_ipv6, addr_ipv6 = server_ipv6.accept()
                print(f"Nuevo cliente IPv6 conectado. Direccion {addr_ipv6}")
                access = semaphore.acquire(blocking=False)
                threading.Thread(target=handle_client, args=(conn_ipv6, addr_ipv6, access)).start()

            except:
                pass


    start_server()
    
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=8080,help='Numero de puerto')
parser.add_argument('--y',type=str,default='quit',help='Mensaje de desconexion')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)
