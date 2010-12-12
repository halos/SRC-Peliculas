#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("estrategiasSimilitud")

import coseno
import pearson
import metricas
from estrategiaSimilitud import EstrategiaSimilitud
from valoracion import Valoracion

# ---> Variables con los elementos a probar <--- #

# particiones
p = [(80, 20), (70, 30)]

# k
k = [1, 5, 10]

# n
n = [2, 4, 8]

# lista con las estrategias de similitud
ees = [] # almacena pares (función, nombre)
ees.append((coseno.calcula_similitud, "coseno"))
ees.append((pearson.calcula_similitud, "pearson"))

# lista con las estrategias de prediccion
eep = []
#eep.append(, "weithed sum")
#eep.append(, "Item average + Adjustment, todos menos 1")
#eep.append(, "Item average + Adjustment, dados n")

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

