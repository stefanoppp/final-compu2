import sqlite3
# ARREGLAR HORA
def consulta(data):
    conexion = sqlite3.connect('connections.db')
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS connections(id_connections int, time_connection datetime not null default current_timestamp)")
    cursor.execute(f"INSERT INTO connections(id_connections) VALUES({data})")
    conexion.commit()
    conexion.close()
