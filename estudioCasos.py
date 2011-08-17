#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

sys.path.append("estrategiasSimilitud")
sys.path.append("estrategiasPredicción")

import coseno
import pearson
import metricas
import estrategiaSimilitud
import particionamiento
import itemAvgAdj1
import itemAvgAdjN
import weithedSum
import motor


def ejecutaPrueba1(p, k, es, ep):
    print "Datos:\n"
    print "Particionado:", p + "\%\n"
    print "k:", k + "\n"
    print "Estrategia de similitud:", es[1] , "\n"
    print "Estrategia de prediccion:", ep[1] , "\n"
    t_inic = metricas.get_clock()
    
    lpredicciones = []    

    (valtrain, valtest) = particionamiento.Particionamiento().divTrainTest(vals, p)
    lsimilitudes = es.similitud(valtrain)
    for valoracion in valtest:
        prediccion = ep.predice(valoracion.idUsu, valoracion.idItem, valtrain,lsimilitudes)
        lpredicciones.append(prediccion)
    v_mae = metricas.mae(lpredicciones, valtest)
    
    t_fin = metricas.get_clock()
    print "Tiempo: %f\n" % (t_fin - t_inic)    
    print "Mae:", v_mae, "\n"
    
    return None

def ejecutaPrueba2(p, k, es, ep, n):
    print "Datos:\n"
    print "Particionado:", p + "\%\n"
    print "k:", k + "\n"
    print "Estrategia de similitud:", es[1] , "\n"
    print "Estrategia de prediccion:", ep[1] , "\n"
    t_inic = metricas.get_clock()
    
    lpredicciones = []    

    m = motor.Motor()
    m.getValoraciones()
    (valtrain, valtest) = particionamiento.Particionamiento().divTrainTest(vals, p)
    lsimilitudes = es.similitud(valtrain)
    for valoracion in valtest:
        prediccion = ep.predice(valoracion.idUsu, valoracion.idItem, valtrain,lsimilitudes)
        lpredicciones.append(prediccion)
    v_mae = metricas.mae(lpredicciones, valtest)
    
    t_fin = metricas.get_clock()
    print "Tiempo: %f\n" % (t_fin - t_inic)    
    print "Mae:", v_mae, "\n"
    
    return None

def ejecutaPrueba3(p, k, es, ep):
    print "Datos:\n"
    print "Particionado:", p + "\%\n"
    print "k:", k + "\n"
    print "Estrategia de similitud:", es[1] , "\n"
    print "Estrategia de prediccion:", ep[1] , "\n"
    t_inic = metricas.get_clock()
    
    lpredicciones = []    

    (valtrain, valtest) = particionamiento.Particionamiento().divTrainTest(vals, p)
    lsimilitudes = es.similitud(valtrain)
    for valoracion in valtest:
        prediccion = ep.predice(valoracion.idUsu, valoracion.idItem, valtrain,lsimilitudes)
        lpredicciones.append(prediccion)
    v_mae = metricas.mae(lpredicciones, valtest)
    
    t_fin = metricas.get_clock()
    print "Tiempo: %f\n" % (t_fin - t_inic)    
    print "Mae:", v_mae, "\n"
    
    return None


#Definimos los distintos parámetros
tp = {80, 70}
tk = {3, 5, 10}
tes = {estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud), estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)}
tn = {2, 4, 8}

print 'Comienzo del estudio de casos para la estrategia de predicción ItemAvgAdj1:\n'

for p in tp:
    for k in tk:
        for es in tes:
            ejecutarPrueba1(p, k, es)

print 'Comienzo del estudio de casos para la estrategia de predicción ItemAvgAdjN:\n'            
 
for p in tp:
    for k in tk:
        for es in tes:
            for n in tn:
                ejecutarPrueba2(p, k, es, n)
                
print 'Comienzo del estudio de casos para la estrategia de predicción WeithedSum:\n'

for p in tp:
    for k in tk:
        for es in tes:
            for n in tn:
                ejecutarPrueba3(p, k, es)