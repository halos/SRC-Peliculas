#!/usr/bin/python
# -*- coding: utf-8 -*-
	
from motor import Motor

def carga_peliculas(nombre_archivo):
	""" Carga las películas

	Params:

		PARAM(): DESCRIPTION

	Return:

		(list): Lista con las peliculas (pelicula)
	"""
	
	peliculas = {}
	
	with open(nombre_archivo, 'r') as fd:
		lineas = fd.readlines()
		for linea in lineas:
			id, anno, nombre = linea.split(',', 2)
			
			peliculas[int(id)] = nombre
			
	return peliculas

def carga_valoraciones(nombre_archivo):
	""" Function doc

	Params:

		PARAM(): DESCRIPTION

	Return:

		(): DESCRIPTION
	"""
	
	with open(nombre_archivo, 'r') as fd:
		
		lineas = fd.readlines()
		
		val = valoracion.Valoracion
		vals = []
		
		for linea in lineas:
			
			# pelicula usu val fecha
			(pel, usu, punt, fecha) = linea.split(',')
			vals.append(val(int(usu),int(pel),int(punt)))
		
		return vals
	

#es = estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)

#pels = carga_peliculas("/media/BLADE/Universidad/II/2º/Sistemas Informaticos/Proyectos/Entrega 1/peliculas.csv")
#print "Películas cargadas"

#vals = carga_valoraciones("/media/BLADE/Universidad/II/2º/Sistemas Informaticos/Proyectos/Entrega 1/ratings2_2.csv")
#print "Valoraciones cargadas"

#print "Pearson:"
#for i in estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud).similitud(vals):
	#print '%s <-> %s --> %f' % (pels[i.idP1][:-1], pels[i.idP2][:-1], i.similitud)

#print "Coseno:"
#for i in estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud).similitud(vals):
	#print '%s <--> %s: --> %f' % (pels[i.idP1][:-1], pels[i.idP2][:-1], i.similitud)

#val = valoracion.Valoracion
#
#vals = []
#vals.append(val(1,333,5))
#vals.append(val(1,222,1))
#
#vals.append(val(2,111,4))
#vals.append(val(2,222,5))
#
#vals.append(val(3,222,4))
#vals.append(val(3,111,4))
#
#vals.append(val(8,888,5))
#vals.append(val(8,999,4))
#vals.append(val(8,333,5))
#
#vals.append(val(9,888,2))
#vals.append(val(9,999,4))
#
#print "Pearson:"
#for i in estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud).similitud(vals):
#	print '%d, %d: --> %f' % (i.idP1, i.idP2, i.similitud)
#
#print "Coseno:"
#for i in estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud).similitud(vals):
#	print '%d, %d: --> %f' % (i.idP1, i.idP2, i.similitud)
#
#vals_n = []
#vals_n.append(val(3,222,5))
#vals_n.append(val(2,111,5))
#
#print
#print '\t/' + "-" * len("Modelo Actualizado:") + '\\'
#print '\t|' + "Modelo Actualizado:" + '|'
#print '\t\\' + "-" * len("Modelo Actualizado:") + '/'
#print
#
#print "Pearson:"
#for i in estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud).actualizaSimilitud(vals, vals_n):
#	print '%d, %d: --> %f' % (i.idP1, i.idP2, i.similitud)
#
#print "Coseno:"
#for i in estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud).actualizaSimilitud(vals, vals_n):
#	print '%d, %d: --> %f' % (i.idP1, i.idP2, i.similitud)
m = Motor()
m.login(1,'asdf')
print 'Fin'