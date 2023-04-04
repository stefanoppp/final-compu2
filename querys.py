import sqlite3
import datetime
import pytz

def consulta(data):

    timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    hora_actual = datetime.datetime.now(timezone)
    hora_formateada = hora_actual.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    conexion = sqlite3.connect('connections.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conexiones (
                        id_con INTEGER,
                        hora_actual TEXT
                    )''')

    cursor.execute("INSERT INTO conexiones (id_con, hora_actual) VALUES (?, ?)", (data, hora_formateada))
    conexion.commit()
    conexion.close()
