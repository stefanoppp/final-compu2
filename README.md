# final-compu2

  Este trabajo consiste en que clientes preguntan quien es la persona de la foto y el server debe contestar acertadamente. Implementará una arquitectura cliente-servior para así, poder implementar sockets. Luego, para implementar mecanismos de I/O, cada conexión cliente-servidor será un thread distinto, esperando el input por parte del cliente para devolver un output. Ese input sera un argumento para que el server sepa que devolver. Previamente a eso, el servidor paralelizará la tarea de entrenar la red para que luego, este abierto a nuevas conexiones. Los datos de las nuevas conexiones y horarios de las mismas serán almacenadas en una base de datos. Las direcciones que se manejarán serán IPV6 e IPV4. Para manejar la concurrencia de clientes se implementará un semáforo al cual los clientes podrán acceder y salir.

  Como tecnologías secundarias, se implementó cv2, Sqlite, datetime, pytz y uuid
