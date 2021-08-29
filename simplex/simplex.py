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
variables_de_decision = 0
ecuacion = []
filas,columnas,saliente,entrante,pivote = 0,0,0,0,-1


"""Parsea los datos del archivo txt, y crea una tabla"""
def crear_tabla(lista_lineas):
    i,j=0,0
    global columnas, filas, variables_de_decision
    linea = list(lista_lineas[0].split(','))
    variables_de_decision = int(linea[2])
    filas = int(linea[3]) + 1
    columnas = int(linea[2]) + int(linea[3]) + 1
    tabla = np.zeros((filas, columnas))
    lista_lineas.pop(0)
    while i < len(lista_lineas):
        linea = list(lista_lineas[i].split(','))
        """Aqui lee la U, diferente al resto puesto q hay q cambiar los signos
            además los guardo en variables globales para luego dar el resultado final"""
        if i == 0:
            for j in range(len(linea)):
                tabla[i,j]=int(linea[j])*-1
                ecuacion.append(int(linea[j]))
        else:
            """parseo el resto de lineas"""
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

"""Verifica que hayan negativos en la fila U"""
def prueba_optimalidad(tabla):
    if (min(tabla[0]) < 0):
        return False
    else:
        return True

"""Calculo la fila entrante, la saliente, el pivote y los asigno a globales"""
def entrante_saliente_pivote(tabla):
    global entrante,saliente,pivote
    """Entrante el menor de la fila U"""
    entrante = np.argmin(tabla[0])
    contador=0
    resutado,resultado_anterior=0,0
    """Para el saliente hacer calculos de LD/Entrante"""
    for filas in tabla[1:]:
        contador += 1
        if filas[entrante] != 0:
            resultado = filas[columnas - 1] / filas[entrante]
            if (resultado >= 0 and resultado_anterior == 0):
                pivote = filas[entrante]
                saliente = contador
                resultado_anterior = resultado
            elif(resultado >= 0 and resultado < resultado_anterior):
                pivote = filas[entrante]
                saliente = contador
                resultado_anterior = resultado

"""Aplico la formula de gaous jordan para cada fila excepto la nueva fila."""
def gaus_jordan(tabla):
    i=0
    for filas in tabla:
        if i != saliente:
            """Formula Gaus jordan"""
            tabla[i] = filas-((tabla[i,entrante])*(tabla[saliente]))
        i+=1
    return tabla

"""Calcula la U, le paso una lista con una tupla de (Entrante,Saliente)
y la recorro en busca de las variables de decisión, de atras hacia adelante
por aquello que hayan más iteraciones de lo normal, luego multiplico 
mi ecuación original * resultado de tablas"""
def calcular_u(posiciones_finales,tabla):
    global variables_de_decision,columnas
    respuesta = np.array([])
    while(variables_de_decision >= 0):
        largo = len(posiciones_finales)-1
        while largo >=0:
            if(posiciones_finales[largo][0] == variables_de_decision-1):
                respuesta = np.append(respuesta,(tabla[posiciones_finales[largo][1],columnas-1]))
                break
            largo-=1
        variables_de_decision -=1
    respuesta = np.flip(respuesta)
    U = sum(ecuacion*respuesta)
    return U

"""Desde aqui llamo a todas las operaciones para el simplex"""
def operaciones_tabulares():
    global entrante, saliente, pivote
    tabla = crear_tabla(lista_lineas)
    optimo = prueba_optimalidad(tabla)
    posiciones_finales = []
    print("\nTabla inicial: ")
    print(tabla)
    while(optimo!=True):
        entrante,saliente,pivote=0,0,-1
        entrante_saliente_pivote(tabla)
        posiciones_finales.append([entrante,saliente])
        print("\nEntrante: ", entrante, "\n", "Saliente: ", saliente, "\n", "Pivote: ", pivote)
        print("\n")
        tabla[saliente]= tabla[saliente] / pivote
        tabla=gaus_jordan(tabla)
        print(tabla)
        optimo = prueba_optimalidad(tabla)
    if(optimo):
        print("U max = ",calcular_u(posiciones_finales,tabla))

operaciones_tabulares()
