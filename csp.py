#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
csp.py
------------

Implementación de los algoritmos más clásicos para el problema
de satisfacción de restricciones. Se define formalmente el
problema de satisfacción de restricciones y se desarrollan los
algoritmos para solucionar el problema por búsqueda.

En particular se implementan los algoritmos de forward checking y
el de arco consistencia. Así como el algoritmo de min-conflics.

En este modulo no es necesario modificar nada.

"""

__author__ = 'juliowaissman'

from collections import deque


class GrafoRestriccion:
    """
    Clase abstracta para hacer un grafo de restricción

    El grafo de restricción se representa por:

    1. dominio: Un diccionario cuyas llaves son las variables (vertices)
                del grafo de restricción, y cuyo valor es un conjunto
                (objeto set en python) con los valores que puede tomar.

    2. vecinos: Un diccionario cuyas llaves son las variables (vertices)
                del grafo de restricción, y cuyo valor es un conjunto
                (objeto set en python) con las variables con las que
                tiene restricciones binarias.

    3. restriccion: Un método que recibe dos variables y sus respectivos
                    valores y regresa True/False si la restricción se cumple
                    o no.

    """

    def __init__(self):
        """
        Inicializa las propiedades del grafo de restriccón

        """
        self.dominio = {}
        self.vecinos = {}
        self.backtracking = 0  # Solo para efectos de comparación

    def restriccion(self, xi_vi, xj_vj):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        x_i, v_i = xi_vi
        x_j, v_j = xj_vj
        raise NotImplementedError("Método a implementar")


def asignacion_grafo_restriccion(grafo, asignacion=None, consist=1, traza=False):
    """
    Asigación de una solución al grafo de restriccion si existe
    por búsqueda primero en profundidad.

    Para utilizarlo con un objeto tipo GrafoRestriccion gr:
    >>> asignacion = asignacion_grafo_restriccion(gr)

    @param grafo: Un objeto tipo GrafoRestriccion
    @param asignacion: Un diccionario con una asignación parcial
    @param consist: Un valor 0, 1 o 2 para máximo grado de consistencia
    @param dmax: Máxima profundidad de recursión, solo por seguridad
    @param traza: Si True muestra el proceso de asignación

    @return: Una asignación completa (diccionario con variable:valor)
             o None si la asignación no es posible.

    """

    if asignacion is None:
        asignacion = {}

    #  Checa si la asignación completa y devuelve el resultado de ser el caso
    if set(asignacion.keys()) == set(grafo.dominio.keys()):
        return asignacion.copy()

    # Selección de variables, el código viene más adelante
    var = selecciona_variable(grafo, asignacion)

    # Los valores se ordenan antes de probarlos
    for val in ordena_valores(grafo, asignacion, var):

        # Función con efecto colateral, en dominio
        # si no es None, se tiene los valores que se
        # redujeron del dominio del objeto gr. Al salir
        # del ciclo for, se debe de restaurar el dominio
        dominio_reducido = consistencia(grafo, asignacion, var, val, consist)

        if dominio_reducido is not None:
            # Se realiza la asignación de esta variable
            asignacion[var] = val

            # Solo para efectos de impresión
            if traza:
                print(((len(asignacion) - 1) * '\t') + "{} = {}".format(var, val))

            # Se manda llamar en forma recursiva (búsqueda en profundidad)
            apn = asignacion_grafo_restriccion(grafo, asignacion, consist, traza)

            # Restaura el dominio
            for valor in dominio_reducido:
                grafo.dominio[valor] = grafo.dominio[valor].union(dominio_reducido[valor])

            # Si la asignación es completa revuelve el resultado
            if apn is not None:
                return apn
            del asignacion[var]
    grafo.backtracking += 1
    return None


def selecciona_variable(grafo, asig_parcial):
    """
    Selecciona la variable a explorar, para usar dentro de
    la función asignacion_grafo_restriccion

    @param grafo: Objeto tipo GrafoRestriccion
    @param asig_parcial: Un diccionario con una asignación parcial

    @return: Una variable de gr.dominio.keys()

    """
    # Si no hay variables en la asignación parcial, se usa el grado heurístico
    if not asig_parcial:
        return max(grafo.dominio.keys(), key=lambda v: len(grafo.vecinos[v]))
    # Si hay variables, entonces se selecciona
    # la variable con el dominio más pequeño
    return min([var for var in grafo.dominio.keys() if var not in asig_parcial],
               key=lambda v: len(grafo.dominio[v]))


def ordena_valores(grafo, asig_parcial, x_i):
    """
    Ordena los valores del dominio de una variable de acuerdo
    a los que restringen menos los dominios de las variables
    vecinas. Para ser usada dentro de la función
    asignacion_grafo_restriccion.

    @param grafo: Objeto tipo GrafoRestriccion
    @param asig_parcial: Un diccionario con una asignación parcial
    @param x_i: La variable a ordenar los valores

    @return: Un generador con los valores de gr.dominio[xi] ordenados

    """
    def conflictos(v_i):
        return sum((1 for x_j in grafo.vecinos[x_i] if x_j not in asig_parcial
                    for v_j in grafo.dominio[x_j]
                    if grafo.restriccion((x_i, v_i), (x_j, v_j))))
    return sorted(list(grafo.dominio[x_i]), key=conflictos, reverse=True)


def consistencia(grafo, asig_parcial, x_i, v_i, tipo):
    """
    Calcula la consistencia y reduce el dominio de las variables, de
    acuerdo al grado de la consistencia. Si la consistencia es:

        0: Reduce el dominio de la variable en cuestión
        1: Reduce el dominio de la variable en cuestion
           y las variables vecinas que tengan valores que
           se reduzcan con ella.
        2: Reduce los valores de todas las variables que tengan
           como vecino una variable que redujo su valor. Para
           esto se debe usar el algoritmo AC-3.

    @param grafo: Objeto tipo GrafoRestriccion
    @param asig_parcial: Un diccionario con una asignación parcial
    @param x_i: La variable a ordenar los valores
    @param v_i: Un valor que puede tomar xi

    @return: Un diccionario con el dominio que se redujo (como efecto
             colateral), a gr.dominio

    """
    # Primero reducimos el dominio de la variable de interes si no tiene
    # conflictos con la asignación previa.
    dom_red = {}
    for (x_j, v_j) in asig_parcial.items():
        if x_j in grafo.vecinos[x_i] and not grafo.restriccion((x_i, v_i), (x_j, v_j)):
            return None
    dom_red[x_i] = {v for v in grafo.dominio[x_i] if v != v_i}
    grafo.dominio[x_i] = {v_i}

    # Tipo 1: lo claramente sensato
    # Se ve raro la forma en que lo hice pero es para dejar mas fácil
    # el desarrollo del algoritmo de AC-3,  y dejar claras las diferencias.
    if tipo == 1:
        pendientes = deque([(x_j, x_i) for x_j in grafo.vecinos[x_i] if x_j not in asig_parcial])
        while pendientes:
            x_a, x_b = pendientes.popleft()
            temp = reduce_ac3(x_a, x_b, grafo)
            if temp:
                if not grafo.dominio[x_a]:
                    grafo.dominio[x_a] = temp
                    for valor in dom_red:
                        grafo.dominio[valor] = grafo.dominio[valor].union(dom_red[valor])
                    return None
                if x_a not in dom_red:
                    dom_red[x_a] = set({})
                dom_red[x_a] = dom_red[x_a].union(temp)

    # Tipo 2: lo ya no tan claramente sensato
    # Al no estar muy bien codificado desde el punto de vista de eficiencia
    # puede tardar mas (el doble) que la consistencia tipo 1 pero debe de
    # generar mucho menos backtrackings.
    #
    # Por ejemplo, para las 4 reinas deben de ser 0 backtrackings y para las
    # 101 reina, al rededor de 4
    if tipo == 2:
        # ================================================
        #    Implementar el algoritmo de AC3
        #    y print()robarlo con las n-reinas
        # ================================================
        raise NotImplementedError("AC-3  a implementar")

    return dom_red


def reduce_ac3(x_a, x_b, grafo):
    """
    Funcion interna para consistencia (tanto tipo 1 como tipo 2)

    """
    reduccion = set([])
    valores_xa = list(grafo.dominio[x_a])
    for v_a in valores_xa:
        for v_b in grafo.dominio[x_b]:
            if grafo.restriccion((x_a, v_a), (x_b, v_b)):
                break
        else:
            reduccion.add(v_a)
            grafo.dominio[x_a].discard(v_a)
    return reduccion


def min_conflictos(grafo, rep=100, maxit=100):
    """
    La aplicación de mínimos conflictos con reinicios aleatorios

    """
    for _ in range(maxit):
        solucion_plausible = minimos_conflictos(grafo, rep)
        if solucion_plausible is not None:
            return solucion_plausible
    return None


def minimos_conflictos(grafo, rep=100):
    """
    Incluir el docstring porfavor

    """
    # ================================================
    #    Implementar el algoritmo de minimos conflictos
    #    y probarlo con las n-reinas
    # ================================================
    raise NotImplementedError("Minimos conflictos  a implementar")
