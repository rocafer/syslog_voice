import datetime
import sqlite3
import openai
import time

from tabulate import tabulate

openai.api_key = "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"  # supply your API key however you choose

current_time = datetime.datetime.now()

conn = sqlite3.connect('Linuxtrbl.db')
c = conn.cursor()


def agrupar_registros(registro):
    # Clasificar el registro y retornar la clasificación
    palabras_clave = ['pycharm 2023.2', 'mg2500']
    valor = ' '.join(registro).lower()  # Convertir el registro completo a minúsculas

    for keyword in palabras_clave:
        if keyword in valor:
            return keyword.capitalize()  # Devolver la palabra clave con la primera letra en mayúscula

    return "Linux"  # Si no se encuentra ninguna palabra clave, se clasifica como "General"


def delete_all():
    c.execute("DELETE FROM logs")
    conn.commit()


def update_data():
    c.execute("UPDATE logs SET type='ERROR' WHERE type='fail' OR type='err' OR type='error' OR type='Fail' OR type='Err'")
    #c.execute("UPDATE logs SET type='ERROR' WHERE type='Could' OR type='could'")
    c.execute("UPDATE logs SET type='ERROR' WHERE type IN ('Could', 'could')")

    conn.commit()
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS logs (ID INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, type TEXT, message TEXT, currdate TIMESTAMP)')


def insert_data(group, log_type, message):
    current_time = datetime.datetime.now()
    c.execute("INSERT INTO logs (group_name, type, message, currdate) VALUES (?, ?, ?, ?)",
              (group, log_type, message, current_time))
    conn.commit()  # Guardar los cambios en la base de datos


def clasificar_registro(registro):
    # Clasificar el registro y retornar la clasificación
    palabras_clave = ['err', 'fail', 'error', 'warning', 'info', 'could']
    valor = ' '.join(registro).lower()  # Convertir el registro completo a minúsculas

    for keyword in palabras_clave:
        if keyword in valor:
            return keyword.capitalize()  # Devolver la palabra clave con la primera letra en mayúscula

    return "General"  # Si no se encuentra ninguna palabra clave, se clasifica como "General"

def nueva_agrupacion(registro):
    #Algoritmo Incompleto

    # Clasificar el registro y retornar la clasificación
    palabras_clave = ['err', 'fail', 'error', 'warning', 'info', 'could']
    valor = ' '.join(registro).lower()  # Convertir el registro completo a minúsculas

    # Extraer valores de fecha y tiempo de la variable valor
    partes_valor = valor.split()
    if len(partes_valor) >= 3:
        fecha_comun = partes_valor[0] + ' ' + partes_valor[1]
        tiempo_comun = partes_valor[2]

    # Crear una lista vacía para almacenar los registros
    registros = []

    for keyword2 in registro:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": "The follow line is an entry log in Linux? please tell me only yes or no, please does not put any point to the end of the anser.: " + keyword2}]
        )
        answer = response.choices[0].message.content

        # Crear un diccionario para el registro actual
        registro_actual = {'message': keyword2, 'answer': answer, 'fecha': fecha_comun, 'tiempo': tiempo_comun}

        # Agregar el registro actual a la lista de registros
        registros.append(registro_actual)
        time.sleep(240)  # Pausa de 4 minutos


    # Supongamos que deseas eliminar los registros con 'answer' igual a 'no', 'No', o 'NO'
    registros_filtrados = []

    for registro in registros:
        if registro['answer'].lower() in ['yes', 'yes.']:
            registros_filtrados.append(registro)

    #registros_filtrados quedan con los datos correctos!

    # Imprimir los registros en un formato tabular
    headers = ["Message", "Answer", "Fecha", "Tiempo"]
    table_data = []

    for registro in registros_filtrados:
        table_data.append([registro["message"], registro["answer"], registro["fecha"], registro["tiempo"]])

    # Crear la representación de la tabla como una cadena en lugar de imprimir directamente
    tabla_str = tabulate(table_data, headers=headers, tablefmt="pretty")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Tengo la siguiente tabla, tengo que seleccionar solo un registro de acuerdo al contenido de message, el contenido de message se debe acercar hacer un log entry, contesta solo el contenido de message que seleccionarías sin usar punto final en tu respuesta:\n" + tabla_str}]
    )
    answer2 = response.choices[0].message.content

    for keyword in palabras_clave:
        if keyword in valor:
            return keyword.capitalize()  # Devolver la palabra clave con la primera letra en mayúscula

    return "General"  # Si no se encuentra ninguna palabra clave, se clasifica como "General"



def mostrar_registro(registro):
    # Agregar una columna con la clasificación al registro completo
    clasificacion = clasificar_registro(registro)
    registro_con_clasificacion = [clasificacion] + registro

    agrupacion = agrupar_registros(registro)
    #registro_con_agrupacion = [clasificacion] + registro


    new_group = nueva_agrupacion(registro)

    # Imprimir los datos del registro por separado
    #for i, valor in enumerate(registro_con_clasificacion):
     #   print(f"Columna {i}:", valor)

    group = agrupacion
    tipo = clasificacion
    message = " ".join(registro)
    insert_data(group, tipo, message)



    #print("Longitud del Vector:", len(registro_con_clasificacion))
    #print("=" * 50)

def main():
    create_table()
    delete_all()
    total_lineas = 0  # Variable para contar las líneas del syslog

    try:
        # Abre el archivo syslog en modo lectura
        with open("/home/r/Documents/syslog", "r") as archivo:
            lineas = archivo.readlines()
            total_lineas = len(lineas)  # Contar el número de líneas

        for linea in lineas:
            # Hacemos el split de la línea
            datos_registro = linea.split()

            # Mostramos el registro
            mostrar_registro(datos_registro)

            # Pausa después de cada registro
            #input("Presiona Enter para continuar al siguiente registro...")

    except FileNotFoundError:
        print("El archivo syslog no se encuentra en la ruta /var/log/syslog.")
    except Exception as e:
        print("Ocurrió un error:", str(e))

    # Mostrar el total de líneas al final
    print("Total de líneas en syslog:", total_lineas)
    update_data()

if __name__ == "__main__":
    main()
