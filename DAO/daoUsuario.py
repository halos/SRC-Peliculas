#!/usr/bin/python
# -*- coding: utf-8 -*-

import usuario
from db import *
from singleton import *

class DAOUsuario(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getUsuarios(self):
		"""
		metodo que devuelve todos los usuarios registrados en la aplicacion
		
		"""
		datos = DB()
		res=datos.get_filas("SELECT * FROM usuarios")
		usus=[]
		for i in res:
			usus.append(usuario.Usuario(i[0],i[1]))
		return usus
	
	def getUsuario(self,id):
		"""
		metodo que busca un usuario concreto
		Params:
			id: identificador del usuario a buscar
		"""
		datos=DB()
		consulta="SELECT * FROM usuarios WHERE id = "+str(id)
		res=datos.get_fila(consulta)
		usu = usuario.Usuario(res[0],res[1])
		return usu