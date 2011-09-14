#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

sys.path.append("estrategiasSimilitud")
sys.path.append("estrategiasPredicción")
sys.path.append("DAO")

import agrupamiento
import coseno
import pearson
import metricas
import itemAvgAdj1
import itemAvgAdjN
import weightedSum
import motor
import db
import crossValidation
import valoracion

tn = (2, 4, 8)
tk = (10, 20, 30)
tep = [( "Item Average Adjustment All-1", itemAvgAdj1.ItemAvgAdj1())]
for n in tn:
    tep.append(( "Item Average Adjustment n = " + str(n), itemAvgAdjN.ItemAvgAdjN(n)))
tep.append(( "Weighted Sum", weightedSum.WeightedSum()))
vtemp = []
vmae = []
print 'Comenzamos la fase de predicción...'

# Ordenamos la lista de valores para K (mayor a menor)
lk = list(tk)
lk.sort(reverse=True)

# Serie de valoraciones
lval = []
lval.append(valoracion.Valoracion(1333, 8593, 5))
lval.append(valoracion.Valoracion(303948, 4, 2))
lval.append(valoracion.Valoracion(2089379, 7, 2))
lval.append(valoracion.Valoracion(504440, 9, 1))
lval.append(valoracion.Valoracion(2299436, 11, 4))

for valoracion in lval:
    t_ig = metricas.get_clock()
    t_inic = metricas.get_clock()
    
    # Obtenemos la información necesaria de la BD
    m = motor.Motor()
    t_inic = metricas.get_clock()
    valsUsu = m.getValoracionesUsuario(valoracion.idUsu)
    t_fin = metricas.get_clock()
    print 'Tiempo de procesamiento de valsUser: %f' % (t_fin - t_inic)
    t_inic = metricas.get_clock()
    valsItem = m.getValoracionesItem(valoracion.idPel)
    t_fin = metricas.get_clock()
    print 'Tiempo de procesamiento de valsItem: %f' % (t_fin - t_inic)
    t_inic = metricas.get_clock()
    simsItem = m.getSimilitudesItem(valoracion.idPel)
    t_fin = metricas.get_clock()
    print 'Tiempo de procesamiento de simsItem: %f' % (t_fin - t_inic)


    # Calculamos los k-vecinos más cercanos a ese elemento (con máximo "k")
    t_inic = metricas.get_clock()
    kmaxValVec = agrupamiento.Agrupamiento().agrupknn(simsItem, valsUsu, valoracion.idPel, lk[0])
    t_fin = metricas.get_clock()
    print 'Tiempo de agrupamiento: %f' % (t_fin - t_inic)
    
    t_inic = metricas.get_clock()
    for k in tk:
        
        for ep in tep:
            
            # Medimos el tiempo para la predicción
            
            # Si es itemAvgAdj, le aportamos los valores para las medias
            if ep[0] != "Weighted Sum":
                ep[1].setValoracionesItem(valsItem)
                ep[1].setValoracionesUsuario(valsUsu)
            # Creamos la estrategia de predicción
            # Predecimos... (usando ls k-vecinos especificados por el valor de la lista de todos)
            prediccion = ep[1].predice(simsItem, valoracion.idUsu, valoracion.idPel, kmaxValVec[:k])
    
    t_fin = metricas.get_clock()
    print 'Tiempo de predicción: %f' % (t_fin - t_inic)
    t_fg = metricas.get_clock()
    print 'Tiempo total: %f' % (t_fg - t_ig)
print 'Fin de la fase de predicción.'
