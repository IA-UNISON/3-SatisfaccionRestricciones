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


class GrafoRestriccion(object):
    """
    Clase abstracta para hacer un grafo de restricción 

    """

    def __init__(self):
        """
        Inicializa las propiedades del grafo de restriccón

        """
        self.dominio = {}
        self.vecinos = {}
        self.backtracking = 0  # Solo para efectos de comparación

    def restricción(self, xi_vi, xj_vj):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        xi, vi = xi_vi
        xj, vj = xj_vj
        raise NotImplementedError("Método a implementar")


def asignacion_grafo_restriccion(gr, ap={}, consist=1, traza=False):
    """
    Asigación de una solución al grafo de restriccion si existe
    por búsqueda primero en profundidad.

    Para utilizarlo con un objeto tipo GrafoRestriccion gr:
    >>> asignacion = asignacion_grafo_restriccion(gr)

    @param gr: Un objeto tipo GrafoRestriccion
    @param ap: Un diccionario con una asignación parcial
    @param consist: Un valor 0, 1 o 2 para máximo grado de consistencia
    @param dmax: Máxima profundidad de recursión, solo por seguridad
    @param traza: Si True muestra el proceso de asignación

    @return: Una asignación completa (diccionario con variable:valor)
             o None si la asignación no es posible.

    """

    if set(ap.keys()) == set(gr.dominio.keys()):
        #  Asignación completa
        return ap.copy()

    var = selecciona_variable(gr, ap)

    for val in ordena_valores(gr, ap, var):

        dominio = consistencia(gr, ap, var, val, consist)

        if dominio is not None:
            for variable in dominio:
                for valor in dominio[variable]:
                    gr.dominio[variable].remove(valor)
            ap[var] = val

            if traza:
                print(((len(ap) - 1) * '\t') + "{} = {}".format(var, val))

            apn = asignacion_grafo_restriccion(gr, ap, consist, traza)

            for variable in dominio:
                gr.dominio[variable] += dominio[variable]

            if apn is not None:
                return apn
            del ap[var]
    gr.backtracking += 1
    return None


def selecciona_variable(gr, ap):
    if len(ap) == 0:
        return max(gr.dominio.keys(), key=lambda v: gr.vecinos[v])
    return min([var for var in gr.dominio.keys() if var not in ap],
               key=lambda v: len(gr.dominio[v]))


def ordena_valores(gr, ap, xi):
    def conflictos(vi):
        acc = 0
        for xj in gr.vecinos[xi]:
            if xi not in ap:
                for vj in gr.dominio[xj]:
                    if not gr.restricción((xi, vi), (xj, vj)):
                        acc += 1
        return acc
    return sorted(gr.dominio[xi], key=conflictos, reverse=True)


def consistencia(gr, ap, xi, vi, tipo):
    if tipo == 0:
        for (xj, vj) in ap.iteritems():
            if xj in gr.vecinos[xi] and not gr.restricción((xi, vi), (xj, vj)):
                return None
        return {}

    dominio = {}
    if tipo == 1:
        for xj in gr.vecinos[xi]:
            if xj not in ap:
                dominio[xj] = []
                for vj in gr.dominio[xj]:
                    if not gr.restricción((xi, vi), (xj, vj)):
                        dominio[xj].append(vj)
                if len(dominio[xj]) == len(gr.dominio[xj]):
                    return None
        return dominio
    if tipo == 2:
        raise NotImplementedError("AC-3  a implementar")
        # ================================================
        #    Implementar el algoritmo de AC3
        #    y probarlo con las n-reinas
        # ================================================


def min_conflictos(gr, rep=100, maxit=100):
    for _ in range(maxit):
        a = minimos_conflictos(gr, rep)
        if a is not None:
            return a
    return None


def minimos_conflictos(gr, rep=100):
    # ================================================
    #    Implementar el algoritmo de minimos conflictos
    #    y probarlo con las n-reinas
    # ================================================
    raise NotImplementedError("Minimos conflictos  a implementar")
