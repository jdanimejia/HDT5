# Diego Juarez 13280
# Daniel Mejia 13271
# HDT5

import simpy

#numero: identificacion del dato
#ram: ram
#proceso_duracion: cuanto tiempo le toma realizar el proceso
#entrada_time: tiempo al que entra el dato o instruccion

def datos(env, numero, ram, entrada_time, proceso_duration):
    
    yield env.timeout(entrada_time)

    print('%s El dato ingreso a %d' % (numero, env.now))
    with ram.request() as req:  #pedimos entrar al proceso
        yield req

        # procesamos la instruccion
        print('%s ingreso al precesador a %s' % (numero, env.now))
        yield env.timeout(proceso_duration)
        print('%s termino proceso a  %s ' % (numero, env.now))

#
env = simpy.Environment()  #crear ambiente de simulacion
ram = simpy.Resource(env, capacity=2) #procesos que se pueden realizar simultaneamiente

# crea las instucciones o datos
for i in range(5):
    env.process(datos(env, 'Dato %d' % i, ram, i*2, 5))

# corremos la simulacion
env.run()
    
