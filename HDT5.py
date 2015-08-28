# -*- coding: cp1252 -*-
#Universida del Valle de Guatemala
#Algoritmos y Estructura de datos
#Christopher Chiroy, 14411
#Freddy Ruiz, 14592
#Hoja de trabajo 5
#Funcionalidad:
# Este programa consiste en la simulación de corrida de procesos en un sistema operativo de tiempo compartido
# pasando cada uno de ellos por 5 estados, desarrollados a continuación.
# 1) New: Asigna memoria RAM al proceso y si el CPU no está ocupado pasa a Ready. 
#         sino se mantiene esperando por memoria. 
# 2) Ready: Proceso se asignan una cantidad de instrucciones a realizar. Al desocuparse
#           el CPU pasa a running
# 3) Running: El proceso realiza 3 instrucciones de un proceso en una unidad de tiempo y luego
#             el CPU se libera y atiende a otro proceso.
# Después de haber sido atendido un proceso por el CPU pueden ocurrir 3 situaciones
# este sale del sistema si ya no tiene instrucciones a realizar, si aún tiene espera a ser
# atentido otra vez en la cola Ready o hace una pequeña espera y vuelve a entrar a la cola
# de ready.

#Importación de las librerias.
import simpy
import random
import math

#Método Proceso
#Función:
#Simular el corrimiento de un sistema operativo de un proceso
#pasando por cada uno de los estados que fueron mencionados
#con anterioridad.
#Parámetros:
#nombre: Identificador del proceso
#t_ingreso:Tiempo expovariencial de ingreso de cada uno de los procesos
#cant_inst: cantidad de instrucciones asignadas a ejecutar del proceso
#cant_RAM: cantidad de RAM a utilizar
#ixu: Instrucciones por unidad de tiempo
def proceso(nombre,t_ingreso,cant_inst,cant_RAM,ixu):
    #Definición de la variable global 
    global tiempoTotal
    global listaDesviacion
    
    #Esta variable tendrá la función de mantener el while en funcionamiento
    entra=1
    while entra==1:
            #Solicitud de memoria al container, este se lo dará hasta que haya disponible en el contenedor
            yield ram.get(cant_RAM)
            
            #Retraso para la simulación de entrada de un proceso al Sistema Operativo
            yield env.timeout(t_ingreso)
            
            #Almacenamiento del tiempo de ingreso
            Tiempo_ingreso=env.now
            
            print ('Proceso %d,   ingreso al tiempo %d, RAM: %d' % (nombre,env.now,cant_RAM))
            
            #Solicitud de atención del CPU a uno de los procesos
            #Será atendido hasta que este esté desocupado
            with cpu.request() as reqCPU:
                yield reqCPU 
                print ('Proceso %d,   cantidad de instrucciones %d' % (nombre,cant_inst))
                while cant_inst >= ixu:
                    cant_inst=cant_inst-ixu
                    yield env.timeout(1)
                    print ('Proceso %d,   quedan %d intrucciones' % (nombre,cant_inst))
                print('Proceso %d,   liberó el cpu al tiempo %d'% (nombre,env.now))
                
            #Creación del número random para la continuidad del programa
            #Si es 1 entra a la cola de waiting
            #Si es 2 regresa a ready
            n = random.randint(1,2)
            if(n==1):
                #Solicitud de ingreso a la cola de espera
                with cpuEspera.request() as reqCPUEspera:
                    yield reqCPUEspera
                    yield env.timeout(1)
                    print('Proceso %d,   entra en espera al timepo %d' % (nombre,env.now))
            #Mantiene el while funcionaniando
            entra=1
            
            #En caso que la cantidad de instrucciones del proceso sea menor a las realizables del cpu
            #Será liberado el cpu con anticipación o ya no lo atenderá.
            if(cant_inst<ixu):
                entra=2

#Proceso Terminated, regresa la ram tomada al contenedor que fue entregada al principio
    yield ram.put(cant_RAM)
    print('RAM: ',ram.level)
    print ('Proceso %d,    terminado al tiempo %s' % (nombre, env.now))
    
    #Operaciones para el cálculo del tiempo promedio de un solo proceso
    tiempoTotalxP = env.now - Tiempo_ingreso
    tiempoTotal = tiempoTotal + tiempoTotalxP
    listaDesviacion.append(tiempoTotalxP)

    
#Creación del environment y definición de variables
#env: Environment
#cpu: Encargado de la atención de procesos
#cpuEspera: Espera cola del waiting
#RAM: Cantidad de RAM disponible en el Sistema operativo
#ram: Definición del contenedor
#ixu: Cantidad de instrucciones a realizar por unidad de tiempo
env = simpy.Environment()
cpu = simpy.Resource(env, capacity = 1) #El CPU puede atender 1 procesos
cpuEspera = simpy.Resource(env, capacity = 1)
RAM = 100
ram = simpy.Container(env, init=RAM, capacity=RAM) #Capacidad de la memoria RAM
ixu = 3
random_seed= 40 #Definición de la semilla del random
random.seed(random_seed)
intervalo= 10 #Intervalo de creación de procesos
tiempoTotal = 0.0
cantProcesos = 25
desviacion = 0.0
listaDesviacion = []

#Creacion de los procesos
for  i in range (cantProcesos):
    cant_inst= random.randint(1,10) #Asignacion de instrucciones a realizar
    cant_RAM= random.randint(1,10) #Asignación de cantidad de RAM a solicitar
    t_ingreso=random.expovariate(1.0/intervalo) #Tiempo de ingreso
    env.process(proceso(i,t_ingreso,cant_inst,cant_RAM,ixu)) #Creación del proceso
#corre el enviroment
env.run()
#Muestra del promedio
print "el promedio es ", tiempoTotal/cantProcesos 
#Almacenamiento de la desviación estandar
for i in listaDesviacion:
    desviacion = desviacion+(i-(tiempoTotal/cantProcesos))**2
    
#Muestra la desviación estandar 
print 'Desviacion: ', math.sqrt(desviacion/(cantProcesos-1))
