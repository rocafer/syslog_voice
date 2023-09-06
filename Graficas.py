import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
import pickle

# Definir la función para graficar los datos
def graficar_datos(datos):
    # Obtener las categorías y cantidades de datos
    categorias = [dato[0] for dato in datos]
    cantidades = [dato[1] for dato in datos]

    # Crear la gráfica de barras
    plt.bar(categorias, cantidades)

    # Añadir etiquetas
    plt.xlabel('Error')
    plt.ylabel('Cantidad')
    plt.title('Gráfica de Errores')

    # Mostrar la gráfica
    plt.show()

# Cargar los datos desde el archivo usando pickle y llamar a la función para graficar
with open("data.pkl", "rb") as file:
    datos = pickle.load(file)
    graficar_datos(datos)
