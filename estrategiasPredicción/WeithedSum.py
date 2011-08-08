#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append("..")

from valoracion import Valoracion

class WeithedSum:
    """ Clase que implementa el método de prediccion WeithedSum """

    def __init__(self, motor):
        """ Constructor básico"""
        self.__motor = motor
        
    def predice(self, idUsu, idItem):
        """
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		
				idItem: Identificador del item cuyo valora deseamos predecir
				valoraciones(dict): Contiene todos las valoraciones aportadas por todos los usuarios
				similitudes(dict): Contiene los pares de similitud entre items devueltos por el agrupamiento	

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
        sum_num = 0
        sum_den = 0
        lsim = self.__motor.getSimilitudesItem(idItem)
        lval = self.__motor.getValoracionesItem(idUsu)
        #Cálculo de la fórmula de la prediccion        
        if len(lsim) != len(lval):
            print 'Error!'
        for i in len(lsim):
            if lsim[i].idPel != idItem: # Obviamos la casilla del item a predecir
                sum_num += lsim[i].similitud * lval[i].valoracion
                sum_den += lsim[i].similitud
        vprediccion = sum_num / sum_den
        prediccion = Valoracion(idUsu, idItem, vprediccion)
        return prediccion
        


