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
import crossValidation

def ejecutaPrueba(kfold, tk, tes, tep):
    for es in tes:
        print "DATOS PARTE OFF-LINE:"
        print "* %d-fold cross validation" % kfold
        print "* Estrategia de similitud:" , es[0]
        vgmae = []
        vgtemp = []        
        # Realizamos k iteraciones y luego realizamos la media aritmética
        for i in range(kfold):
            # Particionamos el espacio, siendo el fold 'i' el validador
            print 'Particionamos, siendo fold de test el nº: %d' % i
            valtest = crossval.ejecutaIter(i)
            # Comenzamos la medición tiempo modelo
            t_inic = metricas.get_clock()
            # Actualizamos el modelo
            print 'Creamos el modelo...'
            m = motor.Motor()
            m.crearModelo(es[1])
            print 'Fin del cálculo del modelo'
            # Fin de la medición de tiempo del modelo
            t_fin = metricas.get_clock()
            time_mod = t_fin - t_inic
            print 'Tiempo de proceso del modelo: %f' % time_mod
            (vmae, vtemp) = ejecutaPrediccion(tk, tep, valtest, time_mod)
            # Añadimos el valor de los vectores al que ya teníamos almacenado
            if not vgmae:
                vgmae = vmae[:]
            else:
                for i in range(len(vmae)):
                    vgmae[i] += vmae[i]
            if not vgtemp:
                vgtemp = vtemp[:]
            else:
                for i in range(len(vtemp)):
                    vgtemp[i] += vtemp
        # Finalmente, realizamos los cálculos de las medias y mostramos
        resultados(kfold, tk, tep, vgmae, vgtemp)        
        return None

def ejecutaPrediccion(tk, tep, valtest, time_mod):
    vtemp = []
    vmae = []
    for k in tk:
        for ep in tep:
            # Medimos el tiempo para la predicción
            t_inic = metricas.get_clock()
            # Realizamos el proceso de testing (predicción)
            lpredicciones = []
            
            for valoracion in valtest:
                # Calculamos los k-vecinos
                kval_vec = agrupamiento.Agrupamiento(valoracion.idUsu).agrupknn(valoracion.idPel, k)
                # Creamos la estrategia de predicción
                # Predecimos...
                prediccion = ep.predice(valoracion.idUsu, valoracion.idPel, kval_vec)
                lpredicciones.append(prediccion)
            # Fin de la medición de tiempo del modelo
            t_fin = metricas.get_clock()
            
            vtemp.append(time_mod + (t_fin - t_inic))
            vmae.append(metricas.mae(lpredicciones, valtest))
            
    return (vmae, vtemp)

def resultados(kfold, tk, tep, vgmae, vgtemp):
    ind = 0
    for k in tk:
        for ep in tep:
            print "DATOS PARTE ON-LINE:"
            print "* Valor de k en K-nn: %d" % k
            print "* Estrategia de predicción: " , ep
            print "* Tiempo medio: %f" % (vgtemp[ind] / kfold)
            print "* Mae medio: %f" % (vgmae[ind] / kfold)
            ind += 1

#Definimos los distintos parámetros
kfold = 5
tk = (10, 20, 30)
tes = (('coseno', estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud)), ('pearson', estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)))
tn = (2, 4, 8)
tep = [itemAvgAdj1.ItemAvgAdj1]
for n in tn:
    tep.append(itemAvgAdjN.ItemAvgAdjN(n))
tep.append(weithedSum.WeithedSum())
    
print 'BEGIN'
print 'Realizamos el particionamiento para k-cfv'
# Realizamos el particionamiento
crossval = crossValidation.CrossValidation(kfold)
ejecutaPrueba(kfold, tk, tes, tep)
print 'THE END'