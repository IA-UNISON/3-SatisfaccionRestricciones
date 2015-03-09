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


class ProblemaCSP:
    """
    Clase abstracta para hacer un problema CSP en entornos discretos finitos.

    """

    def __init__(self):
        """
        Inicializa los valores de la clase

        """
        self.dominio = {}
        self.vecinos = {}
        self.backtracking = 0  # Solo para efectos de comparación

    def restriccion_binaria(self, (xi, vi), (xj, vj)):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        raise NotImplementedError("Método a implementar en la subclase que hereda de ProblemaCSP")


def solucion_CSP_bin(problemaCSP):
    """
    Encuentra una asignación que solucione un problema CSP con únicamente restricciones binarias

    @param problemaCSP: Un objeto de una clase decendiente de ProblemaCSP

    @return: Un diccionario tal que asignacion[var] = val para toda val en problemaCSP.variables,
    y tal que val pertenece a problemaCSP.dominio de tal manera que se satisfagan todas las
    restricciones binarias. En caso que no exista una asignación que satisfaga las restricciones,
    regresa None

    """
    asignacion = {}
    if sol_CSP_bin_rec(problemaCSP, asignacion):
        return asignacion
    return None


def sol_CSP_bin_rec(problemaCSP, asignacion):
    """
    Algoritmo recursivo para la solución de CSP binarios. Funcion interna. Modifica en forma recursiva la
    variable mutable asignación. Igualmente modifica en forma recursiva el objeto problemaCSP, pero recupera
    la información antes de regresar (sin error por supuesto)

    @param problemaCSP: Un problema tipo CSP binario
    @param asignacion: Un diccionario con la aignación

    @return: False si no hay asignación, True si hay asignación. La función modifica la variable mutable 
             `asignacion` 

    """
    # Checa si la asignación es completa
    if set(asignacion.keys()) == set(problemaCSP.dominio.keys()):
        return True

    var = selecciona_variable(problemaCSP, asignacion)
    for val in ordena_valores(problemaCSP, asignacion, var):
        reduccion = consistencia(problemaCSP, asignacion, var, val)
        if reduccion is None:
            continue
        asignacion[var] = val
        bandera = sol_CSP_bin_rec(problemaCSP, asignacion)
        restaura(problemaCSP, reduccion)
        if bandera:
            return True
        del(asignacion[var])
    problemaCSP.backtracking += 1  # Esta linea es solo para probar el método, significa que hay un backtracking
    return False


def selecciona_variable(problemaCSP, asignacion):
    """
    Si asignacion esta vacío, grado heurístico.
    Si no, heurística de la variable más restringida (se selecciona la variable
    que menos valores en su dominio tiene).

    """
    if len(asignacion) == 0:
        return max(problemaCSP.dominio.keys(), key=lambda var: len(problemaCSP.vecinos[var]))

    return min([var for var in problemaCSP.dominio.keys() if var not in asignacion],
               key=lambda var: len(problemaCSP.dominio[var]))


def ordena_valores(problemaCSP, asignacion, variable):
    """
    Heurística del valor menos restrictivo. Ordena los valores de un dominio en orden
    en el que los valores pueden restringir menos los posibles valores de los vecinos de la variable.

    Esta heurística es lenta pero suele dar muy buenos resultados, evitando una gran cantidad de backtrackings.

    """
    def num_conflictos(valor):    
        conflictos = 0
        for otra_variable in problemaCSP.vecinos[variable]:
            if otra_variable not in asignacion:
                for otro_valor in problemaCSP.dominio[otra_variable]:
                    if not problemaCSP.restriccion_binaria((variable, valor), (otra_variable, otro_valor)):
                        conflictos += 1
        return conflictos
        
    return sorted(problemaCSP.dominio[variable], 
                  key=lambda v: num_conflictos(v))


def consistencia(problemaCSP, asignacion, variable, valor):
    """
    Reduce los valores de los dominios de las variables que no están asignadas.

    """
    # 0-consistencia (reducción de su propio dominio)
    if len(problemaCSP.dominio[variable]) == 0:
        return None
    for vecino, val_vecino in asignacion.iteritems():
        if (vecino in problemaCSP.vecinos[variable] and 
            not problemaCSP.restriccion_binaria((variable, valor), (vecino, val_vecino))):
            return None

    # Crea el diccionario reducción y reduce el dominio de la variable seleccionada
    reduccion = {var: [] for var in problemaCSP.vecinos}
    reduccion[variable] = [x for x in problemaCSP.dominio[variable] if x != valor]
    problemaCSP.dominio[variable] = [valor]

    # 1-consistencia (reducción del dominio de los vecinos inmediatos)
    for vecino in problemaCSP.vecinos[variable]:
        if vecino not in asignacion:
            for val_vecino in problemaCSP.dominio[vecino]:
                if not problemaCSP.restriccion_binaria((variable, valor), (vecino, val_vecino)):
                    reduccion[vecino].append(val_vecino)
                    problemaCSP.dominio[vecino].remove(val_vecino)
            if len(problemaCSP.dominio[vecino]) == 0:
                restaura(problemaCSP, reduccion)
                return None

    # 2-consistencia (reducción del dominio por arcos)
    cola = [(xi, xj) for xi in problemaCSP.vecinos[variable] 
                     for xj in problemaCSP.vecinos[xi] 
                     if xi not in asignacion]

    while len(cola) > 0:
        (var1, var2) = cola.pop()
        redujo = False
        for val2 in problemaCSP.dominio[var2]:
            for val1 in problemaCSP.dominio[var1]:
                if problemaCSP.restriccion_binaria((var1, val1), (var2, val2)):
                    break
            else:
                reduccion[var2].append(val2)
                problemaCSP.dominio[var2].remove(val2)
                redujo = True
        if redujo:
            if len(problemaCSP.dominio[var2]) == 0:
                restaura(problemaCSP, reduccion)
                return None
            cola.extend([(var2, var3) for var3 in problemaCSP.vecinos[var2]])
    return reduccion


def restaura(problemaCSP, reduccion):
    """
    Recupera los valores del dominio original antes de modificarse

    """
    for variable in reduccion:
        problemaCSP.dominio[variable] += reduccion[variable]



def min_conflictos(problemaCSP):
    """
    Algoritmo de mínimos conflictos

    @param problemaCSP: Un problema de satisfacción de restricciones binario

    @return: Un diccionario con la asignación correspondiente.
    """ 
    #=================================================================
    # 20 puntos: INSERTAR SU CÓDIGO AQUI (minimos conflictos)
    #=================================================================
