# -*- coding: cp1252 -*-
import simpy
import random

def proceso(nombre,t_ingreso,cant_inst,cant_RAM,ixu):
    global tiempoTotal
    
    entra=1
    while entra==1:
    
            yield ram.get(cant_RAM)
            
            yield env.timeout(t_ingreso)
            
            Tiempo_ingreso=env.now
            
            print ('ingreso del proceso %d al tiempo %d, RAM: %d' % (nombre,env.now,cant_RAM))
            with cpu.request() as reqCPU:
                yield reqCPU
                print ('cantidad de instrucciones %d del proceso %d' % (cant_inst,nombre))
                while cant_inst >= ixu:
                    cant_inst=cant_inst-ixu
                    yield env.timeout(1)
                    print ('quedan %d intrucciones del proceso %d' % (cant_inst,nombre))
                print('Se liberó el cpu del proceso %d al tiempo %d'% (nombre,env.now))
                   
            n = random.randint(1,2)
            if(n==1):
                with cpuEspera.request() as reqCPUEspera:
                    yield reqCPUEspera
                    yield env.timeout(1)
                    print('Estoy esperando')
            entra=1
            
            if(cant_inst<ixu):
                entra=2

    yield ram.put(cant_RAM)
    print('RAM: ',ram.level)
    print ('proceso %d terminado al tiempo %s' % (nombre, env.now))

    tiempoTotalxP = env.now - Tiempo_ingreso
    tiempoTotal = tiempoTotal + tiempoTotalxP

env = simpy.Environment()
cpu = simpy.Resource(env, capacity = 1) #El CPU puede atender 1 procesos
cpuEspera = simpy.Resource(env, capacity = 1)

RAM = 100
ixu = 3
random_seed= 40 #Definición de la semilla del random
random.seed(random_seed)
intervalo= 10 #Intervalo de creación de procesos
tiempoTotal = 0.0
cantProcesos = 1
#Creacion de los procesos
for  i in range (cantProcesos):
    cant_inst= random.randint(1,10) #Asignacion de instrucciones a realizar
    cant_RAM= random.randint(1,10)
    t_ingreso=random.expovariate(1.0/intervalo)
    env.process(proceso(i,t_ingreso,cant_inst,cant_RAM,ixu))
ram = simpy.Container(env, init=RAM, capacity=RAM) #el cargador de bateria soporta 2 carros
env.run()
print "el promedio es ", tiempoTotal/cantProcesos 
