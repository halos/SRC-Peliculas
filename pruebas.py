import sys
sys.path.append("estrategiasSimilitud")

import estrategiaSimilitud
import coseno
import pearson
import valoracion

es = estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)

val = valoracion.Valoracion

vals = []
vals.append(val(1,333,5))
vals.append(val(1,222,1))
vals.append(val(2,111,4))
vals.append(val(2,222,5))
vals.append(val(3,222,4))
vals.append(val(3,111,4))

print "Pearson:"
print estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud).similitud(vals)

print "Coseno:"
print estrategiaSimilitud.EstrategiaSimilitud(coseno.calcula_similitud).similitud(vals)

# break estrategiaSimilitud:45
# break coseno:18
