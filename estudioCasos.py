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
import estrategiaSimilitud
import itemAvgAdj1
import itemAvgAdjN
import weithedSum
import motor
import db

def ejecutaPrueba(p, k, es, ep):
    print "Datos:\n"
    print "Particionado:", p + "\%\n"
    print "k:", k + "\n"
    print "Estrategia de similitud:", es[1] , "\n"
    print "Estrategia de prediccion:", ep[1] , "\n"
    # Comenzamos la medición
    t_inic = metricas.get_clock()
    # Regeneramos la base de datos, con un porcentaje de particionamiento
    dbase = db.DB()
    valtest = dbase.regenerarDB(p)
    # Actualizamos el modelo
    m = motor.Motor()
    m.actualizarModelo()    
    # Realizamos el proceso de testing
    lpredicciones = []
    for valoracion in valtest:
        # Calculamos los k-vecinos
        kval_vec = agrupamiento.Agrupamiento(valoracion.idUsu).agrupknn(valoracion.idPel, k)
        # Creamos la estrategia de predicción
        # Predecimos...
        prediccion = ep.predice(valoracion.idUsu, valoracion.idPel, kval_vec)
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
            ejecutaPrueba(p, k, es, itemAvgAdj1.ItemAvgAdj1())

print 'Comienzo del estudio de casos para la estrategia de predicción ItemAvgAdjN:\n'            
 
for p in tp:
    for k in tk:
        for es in tes:
            for n in tn:
                print 'N: ', n , "\n"
                ejecutaPrueba(p, k, es, itemAvgAdjN.ItemAvgAdjN(n))
                
print 'Comienzo del estudio de casos para la estrategia de predicción WeithedSum:\n'

for p in tp:
    for k in tk:
        for es in tes:
            ejecutaPrueba(p, k, es, weithedSum.WeithedSum())