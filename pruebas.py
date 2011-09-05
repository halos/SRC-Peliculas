#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('estrategiasPredicción')
	
import itemAvgAdj1
import itemAvgAdjN
import weithedSum
import agrupamiento


kval_vec = agrupamiento.Agrupamiento(1333).agrupknn(8593, 5)
# Creamos la estrategia de predicción
# Predecimos...
ep = itemAvgAdj1.ItemAvgAdj1()
prediccion = ep.predice(1333, 8593, kval_vec)