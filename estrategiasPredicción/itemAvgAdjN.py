#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
from math import fabs
from valoracion import Valoracion
from motor import Motor

class ItemAvgAdjN():
    """ Clase que implementa el método de prediccion Item Average Adjustament (N), 
	    hereda de ItemAvgAdj1
	"""
    def __init__(self):
        """ Constructor básico"""
        
    def __mediausuario(self, idUsu, idItem):
        """
            Metodo que calcula la media de las valoraciones
            hechas por un usuario a todos sus items
            
            Params:
                    idUsu (Integer):
                    idItem (Integer):
                    
            Return:
                    media_usuario (Float): Media de las valoraciones hechas por un usuario a todos sus items
            
        """
        m = Motor() # Clase Singleton
        lval_usuario = m.getValoracionesUsuario(idUsu).values()
        nval = 0
        media_usuario = 0
        for valoracion in lval_usuario:
            media_usuario += valoracion.valoracion
            nval+= 1
        media_usuario /= nval
        return media_usuario

    def __mediaitem(self, idUsu, idItem):

        """
            Metodo que calcula la media de las valoraciones
            hechas para un determinado item
            
            Params:
                    idUsu    (Integer):
                    idItem    (Integer): 
                    
            Return:
                    media_usuario: Media de las valoraciones hechas para un determinado item
            
        """
        m = Motor() # Clase Singleton
        lval_item = m.getValoracionesItem(idItem).values()
        nval = 0
        media_item = 0
        for valoracion in lval_item:
            media_item += valoracion.valoracion
            nval+= 1
        media_item /= nval
        return media_item
        
        
    def predice(self, idUsu, idItem, n):
        """
            
        Metodo que devuelve el valor de prediccion para un item-usuario
        
        Params:
                idUsu    (Integer):
                idItem    (Integer): Identificador del item cuyo valora deseamos predecir
                n (Integer): Número de valoraciones a tener en cuenta
        Return:
                    
                prediccion(Valoracion): Valoración predicha para un valor desconocido
                    
        """
        m = Motor()
        media_item = self.__mediaitem(idItem)
        media_usu = self.__mediausuario(idUsu)
        sum_num = 0
        sum_den = 0
        dsim = m.getSimilitudesItem(idItem).values() # Diccionario de similitudes, clave idItem
        lval = m.getValoracionesUsuario(idUsu) # Lista de valoraciones para un usuario
        if n % 2 != 0 or n > len(lval):
            print 'Error!'
        #Cálculo de la fórmula de la prediccion
        nveces = 0 # Contador que vigila que no se superen n evaluaciones
        for val in lval:
            simil = dsim.get(val.idPel, 0)
            if simil != 0: # Existe similitud para el item de esa valoracion
                sum_num += simil.similitud * (val.valoracion - media_usu)
                sum_den += fabs(simil.similitud)    
                if nveces >= n:
                    break
                else:
                    nveces += 1  
        if sum_den == 0:
            print 'Error, division por cero!'
            sys.exit(-1)                          
        vprediccion = sum_num / sum_den + media_item
        prediccion = Valoracion(idUsu, idItem, vprediccion)
        return prediccion
 
