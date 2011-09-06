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
kval_vec = agrupamiento.Agrupamiento(1333).agrupknn(8593, 10)
t_inic = metricas.get_clock()
weithedSum.WeithedSum().predice(1333, 8593, kval_vec)
t_fin = metricas.get_clock()
print 'Tiempo total: %f' % (t_fin - t_inic)

