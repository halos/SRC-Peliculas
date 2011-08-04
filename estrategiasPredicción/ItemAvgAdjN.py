#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

from ItemAvgAdj1 import *

from math import fabs
from valoracion import Valoracion

class ItemAvgAdjN(ItemAvgAdj1):
    """ Clase que implementa el método de prediccion Item Average Adjustament (N), 
	    hereda de ItemAvgAdj1
	"""
    def __init__(self, motor):
        """ Constructor básico"""
        super(ItemAvgAdjN, self, motor).__init__()
        
    def predice(self, idUsu, idItem, n):
        """
            
        Metodo que devuelve el valor de prediccion para un item-usuario
        
        Params:
                idUsu    (Integer):
                idItem    (Integer): Identificador del item cuyo valora deseamos predecir

        Return:
                    
                prediccion(Valoracion): Valoración predicha para un valor desconocido
                    
        """
        
        media_item = self.__mediaitem(idItem)
        media_usu = self.__mediausuario(idUsu)
        sum_num = 0
        sum_den = 0
        nveces = 0
        lsim = self.__motor.getSimilitudesItem(idItem)
        lval = self.__motor.getValoracionesItem(idUsu)
        if n % 2 != 0 or n > (len(lval) - 1):
            print 'Error!'
        if len(lsim) != len(lval):
            print 'Error!'
        #Cálculo de la fórmula de la prediccion
        for i in len(lsim):
            if lval[i].idPel != idItem: # Obviamos la casilla del item a predecir
                sum_num += lsim[i].similitud * (lval[i].valoracion - media_usu)
                sum_den += fabs(lsim[i].similitud)
            if nveces >= n:
                break
            else:
                nveces += 1                
        vprediccion = sum_num / sum_den + media_item
        prediccion = Valoracion(idUsu, idItem, vprediccion)
        return prediccion

