#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py
------------


"""

__author__ = 'juliowaissman'


import csp


class Nreinas(csp.ProblemaCSP):
    """
    El problema de las n-reinas.

    Esta clase permite instanciar un problema de n reinas, sea n un numero entero mayor a 3
    (para 3 y para 2 no existe solución al problema).

    """

    def __init__(self, n=4):
        """
        Inicializa las n--reinas para n reinas, por lo que:

            dominio[i] = [1, 2, ..., n]
            vecinos[i] = [1, 2, ..., n] menos la misma i.

            ¡Recuerda que dominio[i] y vecinos[i] son diccionarios y no listas!

        """
        csp.ProblemaCSP.__init__(self)
        variables = range(1, n + 1)
        for var in variables:
            self.dominio[var] = variables[:]
            self.vecinos[var] = [i for i in variables if i != var]

    def restriccion_binaria(self, (xi, vi), (xj, vj)):
        """
        La restriccion binaria entre dos reinas, las cuales se comen si estan
        en la misma posición o en una diagonal. En esos casos hay que devolver False
        (esto es, no se cumplió con la restricción).

        """
        if vi == vj or abs(vi - vj) == abs(xi - xj):
            return False
        return True

    def muestra_asignacion(self, asignacion):
        """
        Muestra la asignación del problema de las N reinas en forma de tablerito.

        Por supuesto que esta función solo sirve en este contexto.

        """
        interlinea = "+" + "-+" * len(asignacion)
        print interlinea

        for i in range(1, len(asignacion) + 1):
            linea = '|'
            for j in range(1, len(asignacion) + 1):
                linea += 'X|' if j == asignacion[i] else ' |'
            print linea
            print interlinea

def prueba_reinas(n, metodo):
    print "\n" + '-' * 20 + ' Para ', n, ' reinas ' + '_' * 20
    problema = Nreinas(n)
    asignacion = metodo(problema)
    if n < 20:
        problema.muestra_asignacion(asignacion)
    else:
        print [asignacion[i] for i in range(1, n+1)]
    print "Y se tuvieron que realizar ", problema.backtracking, " backtrackings\n"


if __name__ == "__main__":

    # Utilizando consistencia
    prueba_reinas(4, csp.solucion_CSP_bin)
    prueba_reinas(8, csp.solucion_CSP_bin)
    prueba_reinas(16, csp.solucion_CSP_bin)
    prueba_reinas(50, csp.solucion_CSP_bin)
    prueba_reinas(101, csp.solucion_CSP_bin)


    # Utilizando minimos conflictos
    #=============================================================================
    # 20 puntos: Probar y comentar los resultados del métdo de mínios conflictos
    #=============================================================================

    #prueba_reinas(4, csp.min_conflictos)
    #prueba_reinas(8, csp.min_conflictos)
    #prueba_reinas(16, csp.min_conflictos)
    #prueba_reinas(51, csp.min_conflictos)
    #prueba_reinas(101, csp.min_conflictos)
    #prueba_reinas(1000, csp.min_conflictos)
