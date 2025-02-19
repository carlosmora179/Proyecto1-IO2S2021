import numpy as np
import sys
"""Variables globales del programa"""
salida = ""
lista_lineas = None
variables_de_decision = 0
ecuacion = []
filas,columnas,saliente,entrante,pivote = 0,0,0,0,-1
degenerada = False
tipo = 0
columnaActual = 0
dos_fases = []
"""
Funcion:
Parsea los datos del archivo txt, y crea una tabla

Parametros:
1- lista_lineas

Salida:
Tabla inicial del metodo
"""
"""
corregir problema con la variables de holgura comenzar una columna +1
"""

def dimenciones_tabla(lista_lineas):
    global columnas, filas, variables_de_decision, tipo,columnaActual,dos_fases
    linea = list(lista_lineas[0].split(','))
    tipo = 1 if linea[1] == "max" else(2 if linea[1] == "min" else 0)
    variables_de_decision = int(linea[2])
    filas = int(linea[3]) + 1
    columnas = int(linea[2]) + int(linea[3]) + 1
    columnaActual = int(linea[2])
    i,j,=0,0
    columna_adicional=0
    variables_negativas = []
    while i < len(lista_lineas):
        linea = list(lista_lineas[i].split(','))
        while j < len(linea):
            if (linea[j] == '=>'):
                columna_adicional+=1
                variables_negativas.append(i)
                dos_fases.append(i)
            elif(linea[j] == '='):
                dos_fases.append(i)
            elif (linea[j] == '<='):
                dos_fases.append(0)
            j += 1
        j=0
        i+=1
    columnas=columnas+columna_adicional
    tabla = np.zeros((filas, columnas))
    i=columnas
    while len(variables_negativas) != 0:
        tabla[variables_negativas.pop(len(variables_negativas)-1)-1,i-2]=-1
        i -=1


    return tabla

def crear_tabla_GranM(lista_lineas):
    i,j=0,0
    global columnas, filas, variables_de_decision,tipo
    linea = list(lista_lineas[0].split(','))
    variables_de_decision = int(linea[2])
    tipo = 1 if linea[1] == "max" else(2 if linea[1] == "min" else 0)
    
    filas = int(linea[3]) + 1
    columnas = int(linea[2]) + int(linea[3]) + 1
    columnaActual = int(linea[2])
    artfclContador = 1
    tabla = np.zeros((filas, columnas))
    lista_lineas.pop(0)
    while i < len(lista_lineas):
        linea = list(lista_lineas[i].split(','))
        """Aqui lee la U, diferente al resto puesto q hay q cambiar los signos
            además los guardo en variables globales para luego dar el resultado final"""
        if i == 0:
            for j in range(len(linea)):
                if (tipo == 1):

                    tabla[i,j]=float(linea[j])*-1
                else:
                    tabla[i,j]=float(linea[j])
                ecuacion.append(float(linea[j]))
        else:
            """parseo el resto de lineas"""
            while j < len(linea):
                if linea[j] == '<=':
                    j+=1
                    tabla[i,columnas-1]=float(linea[j])
                    tabla[i, columnaActual] = 1
                    columnaActual +=1
                elif linea[j] == '=':
                    j+=1
                    tabla[i,columnas-1]=float(linea[j])
                    tabla[i, columnaActual+artfclContador] = 1
                    if (tipo == 1):
                        tabla[0, columnaActual+artfclContador] = 1000000
                    else:
                        tabla[0, columnaActual+artfclContador] = -1000000
                    artfclContador += 1
                    columnaActual +=1
                elif linea[j] == '>=':
                    j+=1
                    tabla[i,columnas-1]=float(linea[j])
                    tabla[i, columnaActual] = -1
                    tabla[i, columnaActual+artfclContador] = 1
                    if (tipo == 1):
                        tabla[0, columnaActual+artfclContador] = 1000000
                    else:
                        tabla[0, columnaActual+artfclContador] = -1000000
                    artfclContador += 1
                    columnaActual +=1


                else:
                    
                    tabla[i,j]=float(linea[j])
                    
                j+=1
        j=0
        i+=1

    
    return tabla


def crear_tabla(lista_lineas):
    global columnas, filas, variables_de_decision, tipo_problema, columnaActual
    i,j=0,0
    tabla = dimenciones_tabla(lista_lineas)
    lista_lineas.pop(0)
    while i < len(lista_lineas):
        linea = list(lista_lineas[i].split(','))
        """Aqui lee la U, diferente al resto puesto q hay q cambiar los signos
            además los guardo en variables globales para luego dar el resultado final"""
        if i == 0:
            for j in range(len(linea)):
                tabla[i,j]=float(linea[j])*-1
                ecuacion.append(float(linea[j]))
        else:
            """parseo el resto de lineas"""
            while j < len(linea):
                if linea[j] == '<=' or linea[j] == '=' or linea[j] == '=>':
                    j+=1
                    tabla[i,columnas-1]=float(linea[j])
                    tabla[i, columnaActual] = 1
                    columnaActual +=1
                else:
                    tabla[i,j]=float(linea[j])
                    
                j+=1
        j=0
        i+=1

    return tabla


"""
Funcion:
Verifica que hayan negativos en la fila U para probar la optimalidad

Parametros:
1- tabla

Salida:
True si la solucion es optima o False de lo contrrario
"""
def prueba_optimalidad(tabla):
    if( tipo == 1):

        if (min(tabla[0]) < 0):
            return False
        else:
            return True
    if(tipo == 2):
        if (max(tabla[0]) > 0):
            return False
        else:
            return True
"""
Funcion:
Se encarga de verificar si existen posibles multiples soluciones
en el problema

Parametros:
1- tabla
2-posiciones_finales

Salida:
True si existen multiples soluciones para el problema False de lo contrario
"""
def multiples_soluciones(tabla,posiciones_finales):
    
    revisado = False
    for f in range(len(tabla[0])):
        if(tabla[0][f] == 0):
            for c in range(len(posiciones_finales)):
                
                if (f == posiciones_finales[c][0]):
                    
                    revisado =  False
                    break
                else:

                    revisado = True
                    
        if (revisado):
            return revisado
    
    return revisado
"""
Funcion:
Se encarga de obtener el indice de la siguiente variable que 
puede entrar al metodo cuando hay soluciones multiples

Parametros:
1- tabla
2-posiciones_finales

Salida:
Numero entero que es el indice de la columna a entrar
"""
def multiples_soluciones__obtener_indice(tabla,posiciones_finales):
    
    
    revisado = -1
    for f in range(len(tabla[0])):
        if(tabla[0][f] == 0):
            for c in range(len(posiciones_finales)):
                
                if (f == posiciones_finales[c][0]):
                    
                    revisado =  -1
                    break
                else:
                    revisado = f
                
        if (revisado > -1):
            return revisado
    return revisado


"""
Funcion:
Calcula la fila entrante, la saliente, el pivote y los asigno a globales

Parametros:
1- tabla
2- multiples
3- posiciones_finales

Salida:
Setea a las variables globales los datos de columna entrante, fila saliente
y pivote.
"""
import time
def entrante_saliente_pivote(tabla, multiples, posiciones_finales):
    global entrante,saliente,pivote,salida,degenerada

    """Entrante el menor de la fila U"""
    if(multiples):
        entrante = multiples_soluciones__obtener_indice(tabla,posiciones_finales)

    elif(not multiples):
        
        if(tipo == 1):
            entrante = np.argmin(tabla[0][0:len(tabla[0])-1])
        elif(tipo == 2):
            entrante = np.argmax(tabla[0][0:len(tabla[0])-1])
    contador=0
    resultado,resultado_anterior=0,0


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
            elif resultado == resultado_anterior:
                print("\nexisten resultados iguales para saliente")
                salida = salida + ' '.join(map(str,("\nexisten resultados iguales para saliente")))
            if resultado == 0 :
                
                degenerada = True

                print("\nla solucion es degenerada en fila: ",contador)
                salida = salida + ' '.join(map(str,("\nla solucion es degenerada en fila: ",contador)))
                break
    #print(entrante, saliente, pivote)
"""
Funcion:
Verifica si un problema es no acotado

Parametros:
1- tabla

Salida:
True si el problema es no acotado False en caso contrario.
"""
def es_no_acotado(tabla):
    global entrante,saliente,pivote
    
    bandera=False
    resultado,resultado_anterior=0,0
    """Para el saliente hacer calculos de LD/Entrante"""
    for filas in tabla[1:]:
        
        if filas[entrante] <= 0:
            
            bandera = True
        else:
            return False
            
            
    return bandera


"""
Funcion:
Aplica la formula de gaus jordan para cada fila excepto la nueva fila.

Parametros:
1- tabla

Salida:
Tabla con al formula de gaus jordan aplicada
"""
def gaus_jordan(tabla):
    i=0
    for filas in tabla:
        if i != saliente:
            """Formula Gaus jordan"""
            tabla[i] = filas-((tabla[i,entrante])*(tabla[saliente]))
        i+=1
    return tabla


"""
Funcion:
Calcula la U, se pasa una lista con una tupla de (Entrante,Saliente)
y se recorre en busca de las variables de decisión, de atras hacia adelante
por si hay más iteraciones de lo normal, luego multiplica 
la ecuación original * resultado de tablas

Parametros:
1- posiciones_finales
2- tabla

Salida:
El valor calculado del U 
"""
def calcular_u(posiciones_finales,tabla):
    global variables_de_decision,columnas,salida
    respuesta = np.empty(variables_de_decision)
    respuesta.fill(0)
    variables_de_decision_aux = variables_de_decision
    
    while(variables_de_decision >= 0):
        largo = len(posiciones_finales)-1
        while largo >=0:
            if(posiciones_finales[largo][0] == variables_de_decision-1):
                respuesta[posiciones_finales[largo][0]] = (tabla[posiciones_finales[largo][1],columnas-1])
                break
            largo-=1
        variables_de_decision -=1
    
    variables_de_decision = variables_de_decision_aux
    salida = salida +' '.join(map(str, ("\norden de ecuacion es [X1,X2...Xn]")))
    salida = salida +' '.join(map(str, ("\norden de respuesta es [X1,X2...Xn]")))
    print("\norden de ecuacion es [X1,X2...Xn]")
    print("\norden de respuesta es [X1,X2...Xn]")
    print("\necuacion: ",ecuacion,"| respuesta: ",respuesta)
    salida = salida + ' '.join(map(str,("\necuacion: ",ecuacion,"| respuesta: ",respuesta)))
    U = sum(ecuacion*respuesta)
    return U

"""
Funcion:
Encargada de gestionar todo el metodo simplex

Parametros: No

Salida:
Problema del archivo resuelto
"""

def validar_cientificos(tabla):
    i=0
    while(i < len(tabla[0])):
        var = str(tabla[0][i])
        if 'e' in var:
            tabla[0][i] = 0
        i+=1

    #print(tabla)
    return tabla

def operaciones_tabulares_simplex(tabla):
    global entrante, saliente, pivote,salida,degenerada
    optimo = prueba_optimalidad(tabla)
    contadorMultiples = 1
    multiples = False
    posiciones_finales = []
    primer_U = 0
    segundo_U = 0
    salida = salida +"Tabla inicial: \n"
    salida = salida + ' '.join(map(str, tabla))
    while(optimo!=True ):
        entrante,saliente,pivote=0,0,-1
        entrante_saliente_pivote(tabla,multiples,posiciones_finales)
        no_acotado = es_no_acotado(tabla)
        posiciones_finales.append([entrante,saliente])
        salida = salida +' '.join(map(str, ("\nEntrante: ", entrante, "\n", "Saliente: ", saliente, "\n", "Pivote: ", pivote)))
        salida = salida +("\n")
        tabla[saliente]= tabla[saliente] / pivote
        tabla = gaus_jordan(tabla)
        tabla = validar_cientificos(tabla)
        salida = salida +' '.join(map(str, tabla))
        if degenerada:
            break
        if multiples:
            posiciones_finales = posiciones_finales[1:]
        
        optimo = prueba_optimalidad(tabla)
        
        if no_acotado :
            print("\nno acotado en columna: ", entrante)
            salida = salida +' '.join(map(str, ("\nno acotado en columna: ", entrante)))
            break
        elif optimo:
            multiples = multiples_soluciones(tabla,posiciones_finales)
            
            if(multiples and contadorMultiples > 0):
                contadorMultiples= contadorMultiples-1
                primer_U = calcular_u(posiciones_finales,tabla)
                print("\nU max = ",primer_U)
                salida = salida +' '.join(map(str, ("\nU max = ",primer_U)))
                optimo = False

    if(optimo or no_acotado ):
        if no_acotado and not optimo:
            
            print("\nEl problema es no acotado en la columna mencionada")
            salida = salida +("\nEl problema es no acotado en la columna mencionada")
        elif optimo:

            segundo_U = calcular_u(posiciones_finales,tabla)
            
            if(primer_U == segundo_U and segundo_U != 0):
                print("\nU max = ",segundo_U)
                salida = salida +' '.join(map(str, ("\nU max = ",segundo_U)))
                print("\nEl problema tiene multiples soluciones listadas anteriormente")
                salida = salida +("\nEl problema tiene multiples soluciones listadas anteriormente")
            else:
                
                print("\nNo hay soluciones multiples la respuesta correcta es la primera desplegada")
                salida = salida +("\nNo hay soluciones multiples la respuesta correcta es la primera desplegada")
                if(degenerada and  segundo_U != 0):

                    print("\nU max = ",segundo_U)
                    salida = salida +' '.join(map(str, ("\nU max = ",segundo_U)))
                else:
                    print("\nU max = ",primer_U)
                    salida = salida +' '.join(map(str, ("\nU max = ",primer_U)))
                
        

"""
Funcion:
Se encarga de guardar le string de salida en un 
archivo para su permanencia en disco

Parametros:
1-string_salida
2-archivo

Salida:
Archivo creado en la carpeta con la salida del programa.
"""
def guardar_salida(string_salida,archivo):
    archivo = archivo +('_solucion.txt')
    archivo_salida = open (archivo,'w')
    archivo_salida.write(string_salida)
    archivo_salida.close()



"""
Funcion:
Se encarga de realizar la convercio4n a la forma apropiada
de la U.

Parametros:
1- Tabla con la U de forma directa

Salida:
2- Tabla con la U en forma apropiada.
"""
def forma_apropiada(tabla):
    tabla[0] = tabla[0] * 0
    i = 0
    """Coloco mis variables artificiales en U."""
    while(i<len(dos_fases)):
        if(dos_fases[i] != 0):
            tabla[0][variables_de_decision + i] = 1
        i+=1

    """Si es MIN lo transformo a MAX multiplicando por -1"""
    print(tabla[0])
    if (tipo == 1):
        tabla[0] = tabla[0]*-1
    for elemento in dos_fases:
        if(elemento != 0):
            tabla[0] = tabla[0] + (tabla[elemento - 1]*-1)
    return tabla



def primer_fase(tabla):
    tabla = forma_apropiada(tabla)
    operaciones_tabulares_simplex(tabla)



######################## DOS FASES ########################
def metodo_DosFases(tabla):
    #tabla[0] = np.apply_along_axis(sum,1,[tabla[dos])
    tabla = primer_fase(tabla)













"""Encargado de saber que metodo es el q tiene que usar."""
def metodos(lista_lineas):
    linea = list(lista_lineas[0].split(','))
    return int(linea[0])




"""
Funcion: Funcion encargada de ejecutarse al principio del flujo del programa
realiza la lectura del archivo y da inicio al flujo en general.

Recibe los argumentos de ejecucion.

Parametros:
1- args

Salida:

Archivo de salida con la ejecucion del programa

"""
def main(args):
    
    global lista_lineas,salida
    largo = len(sys.argv)
    archivo_dir = sys.argv[largo-1]
    #print("archivo path: ",archivo_dir)
    #archivo = open(archivo_dir, 'r')
    archivo = open('archivo1.txt', 'r')
    lista_lineas = archivo.read().split('\n')

    archivo.close()
    metodo = metodos(lista_lineas)
    

    if metodo == 0:
        print(metodo)
        tabla = crear_tabla(lista_lineas)
        operaciones_tabulares_simplex(tabla)
    elif metodo == 1:
        print(metodo)
        #metodo_GranM()
        tabla = crear_tabla_GranM(lista_lineas)
        operaciones_tabulares_simplex(tabla)
    elif metodo == 2:
        print(metodo)
        tabla = crear_tabla(lista_lineas)
        metodo_DosFases(tabla)
    else:
        print(metodo)
        #metodo_Dual()


    guardar_salida(salida,archivo_dir.replace(".txt",""))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))