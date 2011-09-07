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
    vgmae = []
    vgtempPred = []
    # Inicializamos variables
    gtempMod = 0.0 
    for i in range(len(tep) * len(tk)):
        vgmae.append(0.0)
        vgtempPred.append(0.0)
    
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
        tempMod = t_fin - t_inic
        print 'Tiempo de proceso del modelo: %f' % tempMod
        
        (vmae, vtempPred) = ejecutaPrediccion(tk, tep, valtest)
        
        # Mostramos las estadísticas para dicho fold
        resultadosFold(i, es, tk, tep, vmae, tempMod, vtempPred) 
        
        # Almacenamos una copia de los datos del fold, para los resultados globales 
        gtempMod += tempMod
        for i in range(len(tep) * len(tk)):
            vgmae[i] += vmae[i]
            vgtempPred += vtempPred[i]
        
    # Finalmente, realizamos los cálculos de las medias y mostramos 
    gtempMod /= kfold
    for i in range(len(tep) * len(tk)):
        vgmae[i] /= kfold
        vgtempPred[i] /= kfold
    
    resultadosGlobales(es, tk, tep, vgmae, gtempMod, vgtempPred) 
    return None

def ejecutaPrediccion(tk, tep, valtest):

    vtemp = []
    vmae = []
    print 'Comenzamos la fase de predicción...'
    # Inicializamos vectores
    for i in range(len(tep) * len(tk)):
        vmae.append(0.0)
        vtemp.append(0.0)
            
    # Ordenamos la lista de valores para K (mayor a menor)
    lk = list(tk)
    lk.sort(reverse=True)
    
    for valoracion in valtest:
        cont = 0
        
        # Obtenemos la información necesaria de la BD
        m = motor.Motor()
        valsItem = m.getValoracionesItem(valoracion.idPel)
        valsUsu = m.getValoracionesUsuario(valoracion.idUsu)
        simsItem = m.getSimilitudesItem(valoracion.idPel)
        
        # Calculamos los k-vecinos más cercanos a ese elemento (con máximo "k")
        kmaxValVec = agrupamiento.Agrupamiento().agrupknn(simsItem, valsUsu, valoracion.idPel, lk[0])
        
        indice = 0
        for k in tk:
            
            for ep in tep:
                
                # Medimos el tiempo para la predicción
                t_inic = metricas.get_clock()
                # Si es itemAvgAdj, le aportamos los valores para las medias
                if ep[0] != "Weithed Sum":
                    ep[1].setValoracionesItem(valsItem)
                    ep[1].setValoracionesUsuario(valsUsu)
                
                # Creamos la estrategia de predicción
                # Predecimos... (usando ls k-vecinos especificados por el valor de la lista de todos)
                prediccion = ep[1].predice(simsItem, valoracion.idUsu, valoracion.idPel, kmaxValVec[:k])
               
                # Fin de la medición de tiempo
                t_fin = metricas.get_clock()
                vtemp[indice] += (t_fin - t_inic)
                vmae[indice] += abs(prediccion.valoracion - valoracion.valoracion)
                indice += 1
        
        
        cont += 1
        if cont % 100 == 0:
            print 'Llevamos %d items calculados de %d' % (cont, len(valtest))
    
    # Obtenemos el valor medio para cada configuracion
    for i in range(len(tep) *  len(tk)):
        vmae[i] /= len(valtest)
        vtemp[i] /= len(valtest)
    
    print 'Fin de la fase de predicción.'
    return (vmae, vtemp)

def resultadosFold(nfold, es, tk, tep, vmae, tempMod, vtempPred):
    ind = 0
    for k in tk:
        for ep in tep:
            print "*** ESTADISTICAS PARA EL FOLD: %d ***" % nfold
            print "PARTE OFF-LINE: "
            print "* Estrategia de similitud:" , es[0]
            print "* Tiempo medio del modelo: %f" % tempMod  
            print "PARTE ON-LINE: "
            print "* Valor de k en K-nn: %d" % k
            print "* Estrategia de predicción: " , ep[0]
            print "* Tiempo medio predicción: %f" % vtempPred[ind]
            print "* Mae medio: %f" % vmae[ind]
            ind += 1

def resultadosGlobales(es, tk, tep, vgmae, gtempMod, vgtempPred):
    ind = 0
    for k in tk:
        for ep in tep:
            print "*** ESTADISTICAS FINALES ***"
            print "PARTE OFF-LINE: "
            print "* Estrategia de similitud:" , es[0]
            print "* Tiempo medio del modelo: %f" % gtempMod  
            print "PARTE ON-LINE: "
            print "* Valor de k en K-nn: %d" % k
            print "* Estrategia de predicción: " , ep[0]
            print "* Tiempo medio predicción: %f" % vgtempPred[ind]
            print "* Mae medio: %f" % vgmae[ind]
            ind += 1
            
# Comienzo del Programa de prueba

if len(sys.argv) == 2 and (sys.argv[1] == '0' or sys.argv[1] == '1'):
    nes = int(sys.argv[1])
else:
    print 'Parámetros incorrectos: usa 0 para coseno y 1 para pearson'
    sys.exit(-1) 

#Definimos los distintos parámetros
kfold = 5
tk = (10, 20, 30)
tes = (( 'coseno', estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud)), 
       ( 'pearson', estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)))
tn = (2, 4, 8)
tep = [( "Item Average Adjustment All-1", itemAvgAdj1.ItemAvgAdj1())]
for n in tn:
    tep.append(( "Item Average Adjustment n = " + str(n), itemAvgAdjN.ItemAvgAdjN(n)))
tep.append(( "Weithed Sum", weithedSum.WeithedSum()))
    
# Comenzamos la ejecución de la prueba
print 'BEGIN'
print 'Ejecución de prueba para la estrategia de Predicción: %s' % tes[nes][0]
print 'Realizamos el particionamiento para k-cfv, siendo k = %d' % kfold
# Realizamos el particionamiento
crossval = crossValidation.CrossValidation(kfold)
ejecutaPrueba(kfold, tk, tes[nes], tep)
print 'THE END'