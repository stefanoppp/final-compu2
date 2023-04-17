import socket
import threading
import uuid
import cv2
import argparse
import multiprocessing
def main(args):
    # instanciamos server y red neuronal
    HEADER=64
    PORT=args.x
    DISCONNECT_MESSAGE=args.y
    FORMAT=args.z
    
    SERVER=socket.gethostbyname(socket.gethostname())
    ADDR=(SERVER,PORT)

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server.bind(ADDR)
    from back_propagation import Back_Propagation

    fotos=['P1-1.jpg',
        'P2-1.jpg',
        'P1-2.jpg',
        'P2-2.jpg'
        ]

    salidas=[1,0,1,0]

    pixeles_fotos=[]
    # Obtenemos los pixeles de las imagenes
    for foto in fotos:
        image = cv2.imread(foto)
        auxiliar=[]
        for alto in image:
            for ancho in alto:
                auxiliar.append(ancho[0])
        auxiliar.append(1)
        pixeles_fotos.append(auxiliar)

    back=Back_Propagation(pixeles_fotos,salidas)
    neuronas=back.main()
    # creamos proceso que escribe la bd, el cual accede al lock primero
    from querys import consulta
    semaphore=threading.BoundedSemaphore(1)

    lock=multiprocessing.Lock()

    def handle_client(conn,addr,access):
        # Se crea el hilo y se queda esperando que los otros liberen el semaphore para recibir respuesta por parte del servidor
        connected=True
        print(f"Nuevo cliente conectado. Direccion {addr}")
        
        id_con=uuid.uuid1().int
        id_con=id_con/1000000
        lock.acquire()
        consulta(id_con)
        lock.release()

        while connected:
            msg_length=conn.recv(HEADER).decode(FORMAT)

            if msg_length:
                msg_length=int(msg_length)
                msg=conn.recv(msg_length).decode(FORMAT)
                # La diferencia es que un if libera el semaforo porque accedio, el otro no
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
        server.listen()
        while True:
            conn, addr=server.accept()
            access=semaphore.acquire(blocking=False)
            thread=threading.Thread(target=handle_client,args=(conn,addr,access))
            thread.start()

    p=multiprocessing.Process(target=start_server)
    p.start()
    p.join()
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=5050,help='Numero de puerto')
parser.add_argument('--y',type=str,default='quit',help='Mensaje de desconexion')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)