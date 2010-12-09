#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time

def mae(predicciones, reales):
	""" Function doc

	Params:

		predicciones (list): Lista con las predicciones hechas
		reales (list): Lista con los datos reales

	Return:

		(float): Error absoluto medio
	"""
	
	if len(predicciones) != len(reales):
		print "Número de predicciones y valores reales diferentes!"
		exit()

	tam = len(predicciones)
	_mae = 0

	for i in xrange(tam):
		_mae += abs(predicciones[i] - reales[i])

	_mae /= tam
	
	return _mae
	
	
def get_clock():
	""" Function doc

	Return:

		(float): Hora de linux
	"""
	
	return time.time()
