import socket
import threading
import uuid
import cv2
import argparse
from multiprocessing import Process,Pipe

def main(args):
    HEADER=64
    PORT=args.x
    DISCONNECT_MESSAGE=args.y
    FORMAT=args.z
    ADDR = ('::1', PORT)

    server = socket.create_server(ADDR, family=socket.AF_INET6,dualstack_ipv6=True)
    
    from back_propagation import Back_Propagation

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

    from querys import consulta

    semaphore=threading.BoundedSemaphore(1)

    parent_conn, child_conn = Pipe()
  
    def handle_client(conn,addr,access):

        connected=True
        print(f"Nuevo cliente conectado. Direccion {addr}")
        
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
               
                child_conn.send(f"(SERVER MESSAGE). Usted dijo {msg}. El resultado es: {resultado}".encode(FORMAT))
                server_msj = parent_conn.recv()
                conn.send(server_msj)

        
    def start_server():
        print("Servidor escuchando...")

        server.listen()
        while True:
            conn, addr=server.accept()
            access=semaphore.acquire(blocking=False)
            thread=threading.Thread(target=handle_client,args=(conn,addr,access))
            thread.start()

    start_server()
    
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=5050,help='Numero de puerto')
parser.add_argument('--y',type=str,default='quit',help='Mensaje de desconexion')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)
