#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py
------------


"""

__author__ = 'juliowaissman'


import csp


class Nreinas(csp.GrafoRestriccion):
    """
    El problema de las n-reinas.

    Esta clase permite instanciar un problema de n reinas, sea n un numero entero mayor a 3
    (para 3 y para 2 no existe solución al problema).

    """

    def __init__(self, n=4):
        """
        Inicializa las n--reinas para n reinas, por lo que:

            dominio[i] = [0, 1, 2, ..., n-1]
            vecinos[i] = [0, 1, 2, ..., n-1] menos la misma i.

            ¡Recuerda que dominio[i] y vecinos[i] son diccionarios y no listas!

        """
        csp.GrafoRestriccion.__init__(self)
        for var in range(n):
            self.dominio[var] = range(n)
            self.vecinos[var] = [i for i in range(n) if i != var]

    def restriccion(self, (xi, vi), (xj, vj)):
        """
        La restriccion binaria entre dos reinas, las cuales se comen si estan
        en la misma posición o en una diagonal. En esos casos hay que devolver False
        (esto es, no se cumplió con la restricción).

        """
        return vi != vj and abs(vi - vj) != abs(xi - xj)

    @staticmethod
    def muestra_asignacion(asignacion):
        """
        Muestra la asignación del problema de las N reinas en forma de tablerito.

        Por supuesto que esta función solo sirve en este contexto.

        """
        n = len(asignacion)
        interlinea = "+" + "-+" * n
        print interlinea

        for i in range(n):
            linea = '|'
            for j in range(n):
                linea += 'X|' if j == asignacion[i] else ' |'
            print linea
            print interlinea

def prueba_reinas(n, metodo, tipo=1, traza=False):
    print "\n" + '-' * 20 + ' Para ', n, ' reinas ' + '_' * 20
    grafo_restriccion = Nreinas(n)
    asignacion = metodo(grafo_restriccion, ap={}, 
                        consist=tipo, traza=traza)
    if n < 20:
        Nreinas.muestra_asignacion(asignacion)
    else:
        print [asignacion[i] for i in range(n)]
    print "Y se tuvieron que realizar ", 
    print grafo_restriccion.backtracking, " backtrackings\n"


if __name__ == "__main__":

    # Utilizando consistencia
    prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    prueba_reinas(16, csp.asignacion_grafo_restriccion, tipo=1)
    prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=1)
    prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=1)

    # Utilizando consistencia
    #=============================================================================
    # 25 puntos: Probar y comentar los resultados del métdo de arco consistencia
    #=============================================================================
    # prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas(16, csp.asignacion_grafo_restriccion, tipo=2)
    # prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=2)
    # prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=2)


    # Utilizando minimos conflictos
    #=============================================================================
    # 25 puntos: Probar y comentar los resultados del métdo de mínios conflictos
    #=============================================================================
    #prueba_reinas(4, csp.min_conflictos)
    #prueba_reinas(8, csp.min_conflictos)
    #prueba_reinas(16, csp.min_conflictos)
    #prueba_reinas(51, csp.min_conflictos)
    #prueba_reinas(101, csp.min_conflictos)
    #prueba_reinas(1000, csp.min_conflictos)
