import socket
import threading
import uuid
import cv2
import argparse
def main(args):
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

    def handle_client(conn,addr):
        connected=True
        print(f"Nuevo cliente conectado. Direccion {addr}")
        id_con=uuid.uuid1().int
        from querys import consulta
        consulta(id_con)
        # ---------------------------------------
        while connected:
            msg_length=conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                
                msg_length=int(msg_length)
                msg=conn.recv(msg_length).decode(FORMAT)
                if msg==DISCONNECT_MESSAGE:
                    connected=False
                # imprimo en la consola del server
                print(f"Usuario {addr} dice {msg}")
                
                resultado=back.foto(msg,neuronas,pixeles_fotos=[])
                # imprimo en la consola del client
                conn.send(f"(SERVER MESSAGE). Usted dijo {msg}. El resultado es: {resultado}".encode(FORMAT))
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
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=5050,help='Numero de puerto')
parser.add_argument('--y',type=str,default='quit',help='Mensaje de desconexion')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()
main(args)