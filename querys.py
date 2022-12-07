import sqlite3
import uuid
def consulta(data):
    conexion = sqlite3.connect('connections.db')
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS connections (id_connections varchar(100))")
    cursor.execute(f"INSERT INTO connections VALUES ({data})" )
    conexion.commit()
    conexion.close()