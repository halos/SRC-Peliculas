#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("estrategiasSimilitud")
sys.path.append("estrategiasPredicción")
sys.path.append("DAO")

import agrupamiento
import coseno
import pearson
import metricas
import estrategiaSimilitud
import itemAvgAdj1
import itemAvgAdjN
import weithedSum
import motor
import db
import crossValidation

print 'Midiendo tiempos...'
t_inic = metricas.get_clock()
kval_vec = agrupamiento.Agrupamiento(1333).agrupknn(8583, 10)
t_fin = metricas.get_clock()
print 'Tiempo de agrupamiento: %f' % (t_fin - t_inic)
t_inic = metricas.get_clock()
itemAvgAdj1.ItemAvgAdj1().predice(1333, 8593, kval_vec)
t_fin = metricas.get_clock()
print 'Tiempo de predicción: %f' % (t_fin - t_inic)

