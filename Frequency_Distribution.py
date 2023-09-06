import datetime
import sqlite3
import os
import time
import subprocess
import re

#dim_lst = ['']
lista_syslog = []

# Error messages vector
error_messages = [
    "NetworkManager",
    "kernel",
]

current_time = datetime.datetime.now()

conn = sqlite3.connect('Linuxtrbl.db')
c = conn.cursor()

def delete_All():
    conn = sqlite3.connect('Linuxtrbl.db')
    c = conn.cursor()

    # Eliminamos todos los registros de la tabla 'errors'
    c.execute("DELETE FROM errors")

    conn.commit()
    c.close()
    conn.close()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS errors (ID INTEGER PRIMARY KEY AUTOINCREMENT, error TEXT, message TEXT, currdate TIMESTAMP)')

def insert_data(error_message, line):
    current_time = datetime.datetime.now()
    c.execute("INSERT INTO errors (error, message, currdate) VALUES(?, ?, ?)",
              (error_message, line, current_time))
def datos_de_error(lista_syslog):
    create_table()

    for line in lista_syslog:
        for error_message in error_messages:
            if error_message in line:
                insert_data(error_message, line)

    conn.commit()
    c.close()
    conn.close()


def contar_registros():
    conn = sqlite3.connect('Linuxtrbl.db')
    c = conn.cursor()

    # Realizamos la consulta para contar los registros agrupados por el campo 'error'
    c.execute("SELECT error, COUNT(*) FROM errors GROUP BY error")

    # Obtenemos los resultados de la consulta
    results = c.fetchall()

    # Mostramos el resultado en el formato solicitado
    #print("Resultado:")
    #for error, count in results:
     #   print(f"{error}\t\t{count}")

    c.close()
    conn.close()

def cargar_syslog(ruta_archivo):
    lista_syslog = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            lista_syslog.append(linea.strip())
    return lista_syslog

def main():
    ruta_archivo_syslog = "/var/log/syslog"
    try:
        lista_syslog = cargar_syslog(ruta_archivo_syslog)
        #print("Archivo syslog cargado correctamente en la lista.")
        # Aquí puedes realizar cualquier operación adicional con la lista de syslog
        # Por ejemplo, puedes imprimir las primeras 10 líneas del archivo:
        #print("Las primeras 10 líneas del archivo syslog:")
        #for linea in lista_syslog[:10]:
         #   print(linea)
    except FileNotFoundError:
        print("Error: El archivo syslog no fue encontrado en la ruta especificada.")
    except Exception as e:
        print("Error desconocido:", e)

    create_table()
    delete_All()
    datos_de_error(lista_syslog)
    contar_registros()

if __name__ == "__main__":
    main()