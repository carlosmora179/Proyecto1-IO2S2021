**Proyecto1**\
**Intituto tecnologico de Costa Rica**\
**Investigacion de operaciones**\
**IS 2021**
# Instrucciones de ejecucion
Para ejecutar el codigo es necesario correr el siguiente comando dentro de la carpeta del proyecto llamada simplex.
~~~
$python3 simplex.py [nombre de archivo]
~~~

Donde [nombre de archivo] es sustituido por el nombre del archivo con el problema a resolver segun el formato especificado.

# Ejemplo de archivo

Estructura del archivo de entrada (texto plano con elementos separados por coma):
***
**método, optimización, Número de variables de decisión, Número de restricciones**\
**coeficientes de la función objetivo**\
**coeficientes de las restricciones y signo de restricción**
***
Donde método es un valor numérico [ 0=Simplex, 1=GranM, 2=DosFases], y en
este proyecto solo se empleará la forma del simplex normal con maximización.
Y optimización se indica de forma textual con min o max.
### Ejemplo:
~~~
0,max,2,3
3,5
2,1,<=,6
-1,3,<=,9
0,1,<=,4
~~~

# Autores

**Carlos Mario Mora Murillo 2017238926**\
**Luis Ortiz Rua 2016117738**
