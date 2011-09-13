#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append('..')

from math import fabs
import valoracion
#import motor

class ItemAvgAdjN():
    """ Clase que implementa el método de prediccion Item Average Adjustament (N), 
	    hereda de ItemAvgAdj1
	"""    
    def __init__(self, n):
        """ Constructor básico"""
        if n < 1:
            print 'Error, n debe ser mayor que 0'
            sys.exit(-1)
        self.__n = n
        self.__lvalsUsu = []
        self.__lvalsItem = []
        
    def setValoracionesUsuario(self, valsUsu):
        self.__lvalsUsu = valsUsu.values()
        
    def setValoracionesItem(self, valsItem):
        self.__lvalsItem = valsItem.values()
        
    def __mediausuario(self, idUsu):
        """
            Metodo que calcula la media de las valoraciones
            hechas por un usuario a todos sus items
            
            Params:
                    idUsu (Integer):
                    
            Return:
                    media_usuario (Float): Media de las valoraciones hechas por un usuario a todos sus items
            
        """
#        m = motor.Motor() # Clase Singleton
#        lval_usuario = m.getValoracionesUsuario(idUsu).values()
        media_usuario = 0.0
        
        for valoracion in self.__lvalsUsu:
            media_usuario += valoracion.valoracion
            
        if len(self.__lvalsUsu) == 0:
            media_usuario /= 0.00000000001
        else:
            media_usuario /= len(self.__lvalsUsu)
        
        return media_usuario

    def __mediaitem(self, idItem):

        """
            Metodo que calcula la media de las valoraciones
            hechas para un determinado item
            
            Params:
                    idItem    (Integer): 
                    
            Return:
                    media_usuario: Media de las valoraciones hechas para un determinado item
            
        """
#        m = motor.Motor() # Clase Singleton
#        lval_item = m.getValoracionesItem(idItem).values()
        media_item = 0.0
        
        for valoracion in self.__lvalsItem:
            media_item += valoracion.valoracion
        
        if len(self.__lvalsItem) == 0:
            media_item /= 0.00000000001
        else:
            media_item /= len(self.__lvalsItem)
            
        return media_item
        
        
    def predice(self, simsItem, idUsu, idItem, kval_vec):
        """
            
        Metodo que devuelve el valor de prediccion para un item-usuario
        
        Params:
                idUsu    (Integer):
                idItem    (Integer): Identificador del item cuyo valora deseamos predecir
                kval_vec
        Return:
                    
                prediccion(Valoracion): Valoración predicha para un valor desconocido
                    
        """
#        m = motor.Motor()
#        dsim = m.getSimilitudesItem(idItem) # Diccionario de similitudes, clave idItem
        
        sum_num = 0.0
        sum_den = 0.0
        media_item = self.__mediaitem(idItem)
        media_usu = self.__mediausuario(idUsu)
        
        #Cálculo de la fórmula de la prediccion
        nveces = 0 # Contador que vigila que no se superen n evaluaciones
        for val in kval_vec:
            if val.idPel in simsItem:
                simil = simsItem.get(val.idPel)
                sum_num += simil.similitud * (val.valoracion - media_usu)
                sum_den += fabs(simil.similitud)    
                if nveces >= self.__n:
                    break
                else:
                    nveces += 1  
        
        if sum_den == 0:
            sum_den = 0.00000000001                              
        
        vprediccion = sum_num / sum_den + media_item
        prediccion = valoracion.Valoracion(idUsu, idItem, vprediccion)
        
        return prediccion
 
