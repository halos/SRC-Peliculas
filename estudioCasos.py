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



def ejecutaPrueba(kfold, tk, es, tep):
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
    print 'Comenzamos la fase de predicción...'
    # Ordenamos la lista de valores para K (mayor a menor)
    lk = tk[:]
    lk.sort(reverse=True)
    
    for valoracion in valtest:
        
        # Obtenemos la información necesaria de la BD
        m = motor.Motor()
        valItem = m.getValoracionesItem(valoracion.idPel)
        valUsu = m.getValoracionesUsuario(valoracion.idUsu)
        simItem = m.getSimilitudesItem(valoracion.idPel)
        
        # Calculamos los k-vecinos más cercanos a ese elemento (con máximo "k")
        kmaxValVec = agrupamiento.Agrupamiento().agrupknn(simItem, valUsu, valoracion.idPel, lk[0])
        
        for k in tk:
            
            for ep in tep:
                
                # Medimos el tiempo para la predicción
                t_inic = metricas.get_clock()
                # Creamos la estrategia de predicción
                # Predecimos...
                prediccion = ep.predice(valoracion.idUsu, valoracion.idPel, kmaxValVec[:k])
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

# Comienzo del Programa de prueba

if len(sys.argv) == 2 and (sys.argv == 0 or sys.argv == 1):
    nes = sys.argv[1]
else:
    print 'Parámetros incorrectos, usa 0 para coseno y 1 para pearson'
    sys.exit(-1) 

#Definimos los distintos parámetros
kfold = 5
tk = (10, 20, 30)
tes = (('coseno', estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud)), 
       ('pearson', estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)))
tn = (2, 4, 8)
tep = [itemAvgAdj1.ItemAvgAdj1()]
for n in tn:
    tep.append(itemAvgAdjN.ItemAvgAdjN(n))
tep.append(weithedSum.WeithedSum())
    

print 'BEGIN'
print 'Ejecución de prueba para la estrategia de Predicción: %s' % tes[nes][0]
print 'Realizamos el particionamiento para k-cfv, siendo k = %d' % kfold
# Realizamos el particionamiento
crossval = crossValidation.CrossValidation(kfold)
ejecutaPrueba(kfold, tk, tes[nes], tep)
print 'THE END'