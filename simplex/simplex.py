import numpy as np

# Es para leer consola NO QUITAR, se implentará al final.
'''
from sys import argv
script,archivo = argv
f = open(archivo, 'r')
'''
archivo = open('archivo.txt', 'r')
lista_lineas = archivo.read().split('\n')
archivo.close()

filas,columnas,saliente,entrante,pivote = 0,0,0,0,-1


def crear_tabla(lista_lineas):
    i,j=0,0
    global columnas, filas
    linea = list(lista_lineas[0].split(','))
    filas = int(linea[3]) + 1
    columnas = int(linea[2]) + int(linea[3]) + 1
    tabla = np.zeros((filas, columnas))
    lista_lineas.pop(0)
    while i < len(lista_lineas):
        linea = list(lista_lineas[i].split(','))
        if i == 0:
            for j in range(len(linea)):
                tabla[i,j]=int(linea[j])*-1
        else:
            while j < len(linea):
                if linea[j] == '<=':
                    j+=1
                    tabla[i,columnas-1]=int(linea[j])
                    tabla[i, i + 1] = 1
                else:
                    tabla[i,j]=int(linea[j])
                j+=1
        j=0
        i+=1
    return tabla

def prueba_optimalidad(tabla):
    if (min(tabla[0]) < 0):
        return False
    else:
        return True

def entrante_saliente_pivote(tabla):
    global entrante,saliente,pivote
    entrante = np.argmin(tabla[0])
    contador = 0
    for filas in tabla[1:]:
        contador +=1
        if filas[entrante] != 0:
            resultado = filas[columnas - 1] / filas[entrante]
            if (pivote == -1 and resultado >= 0):
                pivote = resultado
                saliente = contador
            elif(pivote != -1 and pivote > resultado):
                pivote = resultado
                saliente = contador



def operaciones_tabulares():
    tabla = crear_tabla(lista_lineas)
    optimo = prueba_optimalidad(tabla)
    if optimo:
        "Es optimo"
    else:
        entrante_saliente_pivote(tabla)
        print("Tabla inicial: \n")
        print(tabla)
        print("Falta gaus jordan: \n")
        tabla[saliente]= tabla[saliente] / pivote
        print(tabla)
        print("Entrante: ", entrante,"\n","Saliente: ",saliente,"\n","Pivote: ",pivote)

operaciones_tabulares()