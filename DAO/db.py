#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
from singleton import *


class DB(Singleton):
    """ clase generica encargada de la conexion con la base de datos """
    def __init__(self):
        """Inicializa la conexión a la base de datos"""
        self._conectar()
        return
    
    def _conectar(self):
        """crea la conexion"""
        self.conexion = MySQLdb.connect(host="localhost", \
                                        user= "rec", \
                                        passwd="SistemasInformaticos", \
                                        db="ssii", \
                                        port=3306)
        return
    
    def _get_cursor(self):
        """hace ping a la conexión y devuelve el cursor"""
        try:
            self.conexion.ping()
        except:
            self._conectar()
        return self.conexion.cursor()
    
    def get_fila(self, consulta):
        """devuelve una única fila de la consulta"""
        cursor=self._get_cursor()
        cursor.execute(consulta)
        filas = cursor.fetchone()
        cursor.close()
        return filas
    
    def get_filas(self,consulta):
        """devuelve todas las filas"""
        cursor=self._get_cursor()
        cursor.execute(consulta)
        filas = cursor.fetchall()
        cursor.close()
        return filas
    
    def ejecutar(self,consulta):
        """Ejecuta otras operaciones, como inserciones, actualizaciones y borrados"""
        cursor = self._get_cursor()  
        cursor.execute(consulta)
        cursor.execute("COMMIT")  
        cursor.close()  
        return

    # Métodos adicionales
    
    def __borrar_DB(self):
        """
            Borra todas las tablas de la DB
            Params:
                usu: usuario a inserta
        """
        res = self.get_filas("SHOW TABLES")
        tables = []
        for i in res:
            tables.append(i[0])
        for tname in tables:
            self.ejecutar('DROP TABLE IF EXISTS ' + tname + ' CASCADE')
