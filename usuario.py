#!/usr/bin/python
# -*- coding: utf-8 -*-

class Usuario:
	""" Class Usuario """
	
	""" Identificador de usuario """
	
	idUsu = 0
	
	""" Contraseña de usuario """
	
	passw = ""
	
	def __init__ (self, idUsu, passw):
		""" Class initialiser """
		self.idUsu = idUsu
		self.passw = passw
