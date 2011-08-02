#!/usr/bin/python
# -*- coding: utf-8 -*

import metricas
from particionamiento import Particionamiento

def ejecutarPrueba(p, k, es, ep, vals):
	print "Datos:\n"
	print "Particionado:", p + "\%\n"
	print "k:", k + "\n"
	print "Estrategia de similitud:", es[1] , "\n"
	print "Estrategia de prediccion:", ep[1] , "\n"
	t_inic = metricas.get_clock()
	
	lpredicciones = []	

	(valtrain, valtest) = Particionamiento().divTrainTest(vals, p)
	lsimilitudes = es.similitud(valtrain)
	for valoracion in valtest:
		prediccion = ep.predice(valoracion.idUsu, valoracion.idItem, valtrain,lsimilitudes)
		lpredicciones.append(prediccion)
	v_mae = metricas.mae(lpredicciones, valtest)
	
	t_fin = metricas.get_clock()
	print "Tiempo: %f\n" % (t_fin - t_inic)	
	print "Mae:", v_mae, "\n"
	
	return None
