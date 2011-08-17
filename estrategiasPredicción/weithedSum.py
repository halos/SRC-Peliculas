#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append("..")

from valoracion import Valoracion
from motor import Motor

class WeithedSum:
    """ Clase que implementa el método de prediccion WeithedSum """

    def __init__(self):
        """ Constructor básico"""
        
    def predice(self, idUsu, idItem, valoraciones):
        """
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		        idUsu (Integer)
				idItem (Integer): Identificador del item cuyo valora deseamos predecir
				valoraciones(dict):
		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
        m = Motor()
        sum_num = 0
        sum_den = 0
        dsim = m.getSimilitudesItem(idItem).values() # Diccionario de similitudes, clave idItem
        #Cálculo de la fórmula de la prediccion        
        for val in valoraciones:
            simil = dsim.get(val.idPel, 0)
            if simil != 0: # Existe similitud para el item de esa valoracion
                sum_num += simil.similitud * val.valoracion
                sum_den += simil.similitud    
        if sum_den == 0:
            print 'Error, division por cero!'
            sys.exit(-1)
        vprediccion = sum_num / sum_den
        prediccion = Valoracion(idUsu, idItem, vprediccion)
        return prediccion
        


