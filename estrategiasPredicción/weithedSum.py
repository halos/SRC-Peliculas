#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append("..")

import valoracion
#import motor

class WeithedSum:
    """ Clase que implementa el método de prediccion WeithedSum """

    def __init__(self):
        """ Constructor básico"""
        pass
        
    def predice(self, simsItem ,idUsu, idItem, kval_vec):
        """
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		        idUsu (Integer)
				idItem (Integer): Identificador del item cuyo valora deseamos predecir
				valoraciones(dict):
		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
        sum_num = 0.0
        sum_den = 0.0
#        m = motor.Motor()
#        dsim = m.getSimilitudesItem(idItem).values() # Diccionario de similitudes, clave idItem
        
        #Cálculo de la fórmula de la prediccion        
        for val in kval_vec:
            if val.idPel in simsItem:
                simil = simsItem.get(val.idPel)
                sum_num += simil.similitud * val.valoracion
                sum_den += simil.similitud    
        
        if sum_den == 0:
            sum_den = 0.00000000001
        
        vprediccion = sum_num / sum_den
        prediccion = valoracion.Valoracion(idUsu, idItem, vprediccion)
        
        return prediccion
        


