#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



"""

__author__ = 'juliowaissman'


import csp


class Nreinas(csp.GrafoRestriccion):
    """
    El problema de las n-reinas.

    Esta clase permite instanciar un problema de n reinas, sea n un
    numero entero mayor a 3 (para 3 y para 2 no existe solución al
    problema).

    """

    def __init__(self, n=4):
        """
        Inicializa las n--reinas para n reinas, por lo que:

            dominio[i] = [0, 1, 2, ..., n-1]
            vecinos[i] = [0, 1, 2, ..., n-1] menos la misma i.

            ¡Recuerda que dominio[i] y vecinos[i] son diccionarios y no listas!

        """
        super().__init__()
        for var in range(n):
            self.dominio[var] = set(range(n))
            self.vecinos[var] = {i for i in range(n) if i != var}

    def restriccion(self, xi_vi, xj_vj):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        La restriccion binaria entre dos reinas, las cuales se comen
        si estan en la misma posición o en una diagonal. En esos casos
        hay que devolver False (esto es, no se cumplió con la
        restricción).

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        xi, vi = xi_vi
        xj, vj = xj_vj
        return vi != vj and abs(vi - vj) != abs(xi - xj)

    @staticmethod
    def muestra_asignacion(asignacion):
        """
        Muestra la asignación del problema de las N reinas en forma de
        tablerito.

        """
        n = len(asignacion)
        interlinea = "+" + "-+" * n
        print(interlinea)
        for i in range(n):
            linea = '|'
            for j in range(n):
                linea += 'X|' if j == asignacion[i] else ' |'
            print(linea)
            print(interlinea)


def prueba_reinas(n, metodo, tipo=1, traza=False):
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    asignacion = metodo(g_r, ap={}, consist=tipo, traza=traza)
    if n < 20:
        Nreinas.muestra_asignacion(asignacion)
    else:
        print([asignacion[i] for i in range(n)])
    print("Y se realizaron {} backtrackings".format(g_r.backtracking))


if __name__ == "__main__":

    # Utilizando 1 consistencia
    # prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    # prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    # prueba_reinas(16, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    # prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=1)
    prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=1)

    # Utilizando consistencia
    # ==========================================================================
    # Probar y comentar los resultados del métdo de arco consistencia
    # ==========================================================================
    # prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas(16, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=2)
    prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=2)

    # Utilizando minimos conflictos
    # ==========================================================================
    # Probar y comentar los resultados del métdo de mínios conflictos
    # ==========================================================================
    # prueba_reinas(4, csp.min_conflictos)
    # prueba_reinas(8, csp.min_conflictos)
    # prueba_reinas(16, csp.min_conflictos)
    # prueba_reinas(51, csp.min_conflictos)
    # prueba_reinas(101, csp.min_conflictos)
    # prueba_reinas(1000, csp.min_conflictos)
