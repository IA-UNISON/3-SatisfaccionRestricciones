![](ia.png)

# Algoritmos de satisfacción de restricciones

**Evaluación de competencias 3**

## Objetivo

En esta actividad se espera que los estudiantes desarrollen la habilidad para
expresar un problema de satisfacción de restricciones binarias de manera formal,
y que los algoritmos básicos de satisfacción de restricciones puedan utilizarse.
De forma adicional, se espera que en este trabajo los estudiantes puedan
desarrollar y probar un algoritmo de satisfacción de restricciones por búsqueda
local relativamente simple.

## Trabajos a desarrollar

Lo que hay que hacer en este trabajo es:

1. En el archivo `csp.py` agregar el método de AC3 a la función de consistencia
   como se vio en clase.

2. En el archivo `nreinasCSP.py` Probar el algoritmo de busqueda con
   2-consistencia y compararlo con el de 1-consistencia y reportar las
   diferencias encontradas.

3. En el archivo `sudoku.py` se ofrece una explicación breve del juego del
   sudoku, cual es el objetivo y cual es la forma en que buscamos formalizar el
   estado con un arreglo de 81 valores. Una vez comprendido el problema y la
   representación, el dominio de cada variable es ya programado por el profesor.
   El alumno deberá ser capaz de definir los vecinos de cada variable.

4. En el archivo `sudoku.py`, desarrollar la restriccion binaria para dos
   variables que se asumen son vecinos.

5. En el archivo `sudoku.py` probar y encontrar la solución para los dos sudokus
   que en internet se presentan como los más dificiles de resolver por un
   humano. Verificar la solución.

6. En el archivo `csp.py` agregar el método de solución de problemas de
   satisfacción de restricciones binarias conocido como **mínimos conflictos**,
   el cual se vió en clase.

7. En el archivo `nreinasCSP.py` Probar el algoritmo de mínimos conflictos y
   compararlo con el de búsqueda en grafos de restriccion y reportar las
   diferencias encontradas.

8. En el archivo `cuadrado_magico_4.py` desarrollar un problema el cual sea la
   generación de un cuadrado mágico de 4 x 4. Probar su resolución con
   cualquiera de los algoritmos vista, y comprobar que efectivamente el
   resultado es una solución posible.
