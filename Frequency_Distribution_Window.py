import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess
import pickle

# Error messages vector
error_messages = [
    "NetworkManager",
    "kernel",
    "All",
]

conn = sqlite3.connect('Linuxtrbl.db')
c = conn.cursor()

# Función para mostrar la gráfica
def mostrar_grafica():
    # Realizar la consulta para contar los registros agrupados por el campo 'error'
    c.execute("SELECT error, COUNT(*) FROM errors GROUP BY error")

    # Obtener los resultados de la consulta
    results = c.fetchall()

    # Guardar los datos en un archivo usando pickle
    with open("data.pkl", "wb") as file:
        pickle.dump(results, file)

    # Ejecutar el programa Graficas.py
    subprocess.Popen(["python", "Graficas.py"])


def contar_registros():
    # Limpiamos el Treeview antes de cargar nuevos datos
    tree_calculate.delete(*tree_calculate.get_children())

    # Realizamos la consulta para contar los registros agrupados por el campo 'error'
    c.execute("SELECT error, COUNT(*) FROM errors GROUP BY error")

    # Obtenemos los resultados de la consulta
    results = c.fetchall()

    # Insertamos los nuevos datos en el Treeview
    for result in results:
        tree_calculate.insert("", "end", values=result)


# Función para cargar datos en el Treeview desde la tabla "errors"

def cargar_datos():
    # Obtenemos el valor seleccionado del ComboBox
    selected_error = combo.get()

    # Si se selecciona "All", mostramos todos los registros
    if selected_error == "All":
        c.execute("SELECT * FROM errors")
    else:
        # Realizamos el SELECT con la cláusula WHERE para obtener los registros correspondientes
        c.execute("SELECT * FROM errors WHERE error=?", (selected_error,))

    datos = c.fetchall()

    # Limpiamos el Treeview antes de cargar nuevos datos
    tree.delete(*tree.get_children())

    # Insertamos los nuevos datos en el Treeview
    for dato in datos:
        tree.insert("", "end", values=dato)

    # Actualizamos la etiqueta con el total de registros
    total_registros.set(len(datos))

def agregar_dato():
    dato = entry.get()
    if dato:
        combo['values'] = (*combo['values'], dato)
        entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Agregar datos al ComboBox")

# Crear el primer LabelFrame "Seleccionar"
frame_seleccionar = ttk.LabelFrame(root, text="Seleccionar")
frame_seleccionar.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Crear el ComboBox dentro del primer LabelFrame
combo = ttk.Combobox(frame_seleccionar, values=error_messages, width=30)
combo.grid(row=0, column=0, padx=10, pady=10)

# Crear el TextBox dentro del primer LabelFrame
entry = ttk.Entry(frame_seleccionar, width=30)
entry.grid(row=0, column=1, padx=10, pady=10)

# Crear el botón para agregar datos al ComboBox dentro del primer LabelFrame
button_agregar = ttk.Button(frame_seleccionar, text="Agregar", command=agregar_dato)
button_agregar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Crear el segundo LabelFrame "Mensajes de Error"
frame_mensajes_error = ttk.LabelFrame(root, text="Mensajes de Error")
frame_mensajes_error.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Agregar etiqueta para mostrar la descripción "Total de Registros.-"
label_total_registros_desc = ttk.Label(frame_mensajes_error, text="Total de Registros.-")
label_total_registros_desc.grid(row=0, column=0, padx=5, pady=5)

# Variable para almacenar el total de registros y mostrar en la etiqueta
total_registros = tk.StringVar()
total_registros.set("0")  # Inicialmente, no hay registros
label_total_registros = ttk.Label(frame_mensajes_error, textvariable=total_registros)
label_total_registros.grid(row=0, column=1, padx=5, pady=5)


# Crear el Treeview dentro del segundo LabelFrame
tree = ttk.Treeview(frame_mensajes_error, columns=("ID", "error", "message", "currdate"), show="headings", height=5)
tree.heading("ID", text="ID")
tree.heading("error", text="error")
tree.heading("message", text="message")
tree.heading("currdate", text="currdate")
tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Crear el Scrollbar vertical y asociarlo al Treeview
vsb = ttk.Scrollbar(frame_mensajes_error, orient="vertical", command=tree.yview)
vsb.grid(row=1, column=2, sticky="ns")
tree.configure(yscrollcommand=vsb.set)

# Crear el Scrollbar horizontal y asociarlo al Treeview
hsb = ttk.Scrollbar(frame_mensajes_error, orient="horizontal", command=tree.xview)
hsb.grid(row=2, column=0, columnspan=2, sticky="ew")
tree.configure(xscrollcommand=hsb.set)



# Crear el botón para cargar datos al Treeview desde la tabla "errors" dentro del segundo LabelFrame
button_cargar = ttk.Button(frame_mensajes_error, text="Cargar Datos", command=cargar_datos)
button_cargar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)  # Modificar el grid para colocarlo debajo del Scrollbar horizontal



# Crear el tercer LabelFrame "Calcular"
frame_calcular = ttk.LabelFrame(root, text="Calcular")
frame_calcular.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Crear el Treeview dentro del tercer LabelFrame con las columnas "Error" y "Cantidad"
tree_calculate = ttk.Treeview(frame_calcular, columns=("Error", "Cantidad"), show="headings", height=5)
tree_calculate.heading("Error", text="Error")
tree_calculate.heading("Cantidad", text="Cantidad")
tree_calculate.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Crear el botón para calcular y cargar los datos al Treeview
button_calcular = ttk.Button(frame_calcular, text="Calcular", command=contar_registros)
button_calcular.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Crear el botón para mostrar la gráfica dentro del tercer LabelFrame
button_grafica = ttk.Button(frame_calcular, text="Grafica", command=mostrar_grafica)
button_grafica.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()
