#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("estrategiasSimilitud")
sys.path.append("estrategiasPredicción")

import coseno
import pearson
import metricas
import particionamiento
from estrategiaSimilitud import EstrategiaSimilitud
from estrategiaPrediccion import EstrategiaPrediccion
import ItemAvgAdj1
import ItemAvgAdjN
import WeithedSum

# ---> Variables con los elementos a probar <--- #

# Obtenemos la lista de valoraciones de la base de datos

# particiones
lp = [80, 70]

# k
lk = [2, 4, 8]

# lista con las estrategias de similitud

ees = [] # almacena pares (función, nombre)
ees.append((coseno.calcula_similitud, "coseno"))
ees.append((pearson.calcula_similitud, "pearson"))

# lista con las estrategias de prediccion

eep = []

ws = WeithedSum.WeithedSum()

eep.append((ws.predice, "weithed sum"))
eep.append((ItemAvgAdj1().predice, "Item average + Adjustment, todos menos 1"))
eep.append((ItemAvgAdjN().predice, "Item average + Adjustment, dados n"))



# Prueba general

niter = 0

for p in lp:
	for k in lk:
		for es in ees:
			for ep in eep:
				niter += 1
				print "------------ Prueba nº", niter , "------------\n"
				ejecutarPrueba(p,k,es[0],ep[0],vals)

	

# ---> Prueba de similitudes <--- #

vals = [] # valoraciones

# cargar las valoraciones
# más tarde se usarán los valores de verdad
vals.append(Valoracion(1,333,5))
vals.append(Valoracion(1,222,1))
vals.append(Valoracion(2,111,4))
vals.append(Valoracion(2,222,5))
vals.append(Valoracion(3,222,4))
vals.append(Valoracion(3,111,4))

for func, nombr in ees:
	print "Midiendo el tiempo de %s" % (nombr, )
	t_inic = metricas.get_clock()
	similitudes = EstrategiaSimilitud(func).similitud(vals)
	t_fin = metricas.get_clock()
	
	print "El tiempo que ha tardado en ejecutarse %s: %f" % (nombr, t_fin - t_inic)
	print
	
# ---> Prueba de predicciones <--- #


# Funciones adicionales

def ejecutarPrueba(p, k, es, ep, vals):
	print "Datos:\n"
	print "Particionado:", p + "\%\n"
	print "k:", k + "\n"
	print "Estrategia de similitud:", es[1] , "\n"
	print "Estrategia de prediccion:", ep[1] , "\n"
	t_inic = metricas.get_clock()
	
	lpredicciones = []	

	(valtrain, valtest) = Particionamiento(vals, p)
	lsimilitudes = es.similitud(valtrain)
	for valoracion in test:
		prediccion = ep.predice(valoracion.idUsu, valoracion.idItem, valtrain,lsimilitudes)
		lpredicciones.append(prediccion)
	v_mae = mae(lpredicciones, valtest)
	
	t_fin = metricas.get_clock()
	print "Tiempo: %f\n" % (t_fin - t_inic)	
	print "Mae:", v_mae, "\n"
	
	return None

