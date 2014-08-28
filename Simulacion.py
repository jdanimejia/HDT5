#--------------------------------------------------
#Universidad del Valle de Guatemala
#Algoritmos y estructura de datos
#Seccion 30
#Diego juarez 13280
#Daniel Mejia 13271
#H.D.T.5.py
#--------------------------------------------------

#se importan los modulos a utilizar en este caso es el random y el simpy
import random
import simpy

#se le envian parametros a utilizar, como el numero total de procesos
#y con que intervalo se va a generar entre procesos
RANDOM_SEED = 42
nuevoProceso = 25 
IntervaloEntreP = 10.0 

# se declaran las funcions que recibe 6 parametros dentro de estos parametros
# esta el ambiente, el valor, intervalos, memoriaRam, Procesador y El tiempo de Espera
# esto nos va a generar procesos al azar conforme a los parametros que se le
#enviaron, la memoriaRaM esel recurso de memoria que se empleara para los procesos
#mientras que el procesador es la cantidad de recursos que se tiene asignados
#al procesadoir para correr el proceso que se le indico 
def source (Ambiente, Valor, intervalos, MemoriaRam, Procesador, Espera) :
        # dentro de este for se mira cada proceso que tiene un numero al azar de
        #instrucciones a ejecutar, asi mismo se necesita una cantidad al azar de
        # memoria RAm
    for i in range (Valor): 
        instrucciones = random.randint(1,10)
        memoria = random.randint (1,10)
        vari = proceso(Ambiente, 'ID%02d' %  i, memoria, MemoriaRam, Procesador, Espera, instrucciones)
        Ambiente.process(vari)
        variDos = random.expovariate(1.0 / intervalos)
        yield Ambiente. timeout (variDos)

# se define la funcion de proceso la cual pasa por todas las etapas y luego termina su ejecucion
# los parametros que recibe esta funcion son Ambiente, ProcesoDeDatos, Memoria, MemoriaRam, Procesador,
#Espera y instrucciones, asi mismo se definen las variables TiempoTotal, promedio
#y contador como Global para hacer uso en todo el programa y mantener los datos
# que estas variables poseen
def proceso (Ambiente, procesoDeDatos, memoria, MemoriaRam, Procesador, Espera, instrucciones):
    global TiempoTotal
    global promedio
    global Contador
    llegada = Ambiente. now
    print ('%7.4f %s: NEW (esperando MemoriaRam %s), MemoriaRam disponible %s' %(llegada, procesoDeDatos,memoria, MemoriaRam.level))
    # se realiza un yield el cual espera a que la memoria ram este disponible
    with MemoriaRam.get (memoria) as req:
        yield req 
        
        wait = Ambiente.now - llegada
        print ('%7.4f %s: READY espero MemoriaRam %6.3f' % (Ambiente.now, procesoDeDatos, wait))

        #mientras tenga instrucciones por ejecutar se realizan enstas operaciones
        while instrucciones > 0:

            with Procesador.request() as reqProcesador:
                # se realiza un yield para poder esperar por los procesadores
                yield reqProcesador 
                print ('%7.4f %s: RUNNING instrucciones %6.3f' % (Ambiente.now, procesoDeDatos, instrucciones))

                # este yield esta dedicado exclusivamente al tiempo de ejecucion por procesador
                yield Ambiente.timeout (1) 
                # se revisa la cantidad de instrucciones que quedan
                if instrucciones > 3:
                    instrucciones = instrucciones -3
                else:
                    instrucciones -0
            # conprueva que existan mas intrucciones por ejecutarse
            # si existe alguna la realiza
            if instrucciones >0:
                siguiente = random.choice (["ready","waiting"])
                if siguiente =="waiting":
                    with Espera.request() as reqEspera:
                        yield reqEspera 
                        print ('%7.4f %s: Waiting' % (Ambiente.now, procesoDeDatos))

                        yield Ambiente.timeout(1) 

                #ahora se pasa a hacer nuevamente cola para esperar al Procesador
                print('%7.4f  %s: READY' % (Ambiente.now, procesoDeDatos))

        #se termino el proceso
        tiempoProceso = Ambiente.now - llegada
        print ('%7.4f %s: TERMINATED tiempo ejecucion %s' % (Ambiente.now,procesoDeDatos,tiempoProceso))

        #Regresar la memoria
        TiempoTotal = TiempoTotal + tiempoProceso
        Contador = Contador + 1
        with MemoriaRam.put(memoria) as reqDevolverMemoriaRam:
            # se regresa la memoria que se utilizo en el programa
            yield reqDevolverMemoriaRam 
            print ('%7.4f %s: Regresando MemoriaRam %s' % (Ambiente.now, procesoDeDatos, memoria))


# se carga el ambiente para poder iniciarlo
# asi mismo se cargan los valores iniciales
# como la cantidad de procesadors y la cantidad de memoria 
print ('Inicio del Sistema Operativo linux 9.8')
random.seed(RANDOM_SEED)
Ambiente = simpy.Environment()
TiempoTotal = 0
Contador = 0
Procesador = simpy.Resource(Ambiente, capacity = 1) 
MemoriaRam = simpy.Container(Ambiente, init = 100, capacity=100) 
Espera = simpy.Resource(Ambiente, capacity=1)
Ambiente.process(source(Ambiente,nuevoProceso, IntervaloEntreP, MemoriaRam, Procesador, Espera))
Ambiente.run()
promedio = TiempoTotal/Contador
print ('Tiempo total en Correr: ',TiempoTotal, 'Promedio total: ',(promedio))













                

