#Ale Sierra, Emily Góngora, y Camila Sandoval
# Simulador de un sistema de procesamiento de procesos con CPU y RAM
# Se simula el procesamiento de varios procesos con diferentes configuraciones de memoria y CPU
import simpy
import matplotlib.pyplot as plt
import numpy as np

#clase que simula la memoria RAM y verifica si hay suficiente memoria para ejecutar un proceso
class RAM:
    def __init__(self, env, memoria_total):
        self.memoria_disponible = simpy.Container(env, init=memoria_total, capacity=memoria_total)
        self.env = env

    def reservar_memoria(self, proceso):
        yield self.memoria_disponible.get(proceso.memoria_requerida)

    def liberar_memoria(self, proceso):
        yield self.memoria_disponible.put(proceso.memoria_requerida)

#clase que simula el CPU y procesa instrucciones de un proceso
class CPU:
    def __init__(self, env, velocidad):
        self.env = env
        self.velocidad = velocidad  # Instrucciones por unidad de tiempo

    def procesar(self, proceso):
        instrucciones_a_ejecutar = min(proceso.instrucciones, self.velocidad)
        yield self.env.timeout(1) 
        proceso.instrucciones -= instrucciones_a_ejecutar

#clase que simula un proceso con una cantidad de instrucciones y memoria requerida
class Proceso:
    def __init__(self, id, memoria_requerida, instrucciones):
        self.id = id
        self.memoria_requerida = memoria_requerida
        self.instrucciones = instrucciones
        self.tiempo_inicial = None
        self.tiempo_final = None

#clase que simula el sistema de procesamiento de procesos con CPU y RAM
#contiene una lista de CPUs y un objeto de la clase RAM, y métodos para gráficar acorde a las configuraciones
class Simulador:
    def __init__(self, env, memoria_total, velocidad_cpu, num_cpus=1):
        self.env = env
        self.ram = RAM(env, memoria_total)
        self.cpus = [CPU(env, velocidad_cpu) for _ in range(num_cpus)]
        self.tiempos_finales = [] 

    def ejecutar_proceso(self, proceso):
        proceso.tiempo_inicial = self.env.now
        yield self.env.process(self.ram.reservar_memoria(proceso))
        
        while proceso.instrucciones > 0:
            cpu = self.cpus[proceso.id % len(self.cpus)]
            yield self.env.process(cpu.procesar(proceso))
        
        proceso.tiempo_final = self.env.now
        self.tiempos_finales.append(proceso.tiempo_final - proceso.tiempo_inicial) 
        yield self.env.process(self.ram.liberar_memoria(proceso))

    def ejecutar_simulacion(self, procesos):
        for proceso in procesos:
            self.env.process(self.ejecutar_proceso(proceso))
        self.env.run()
        
    def graficar_resultados(self, resultados, titulo):
        cantidades_procesos = list(resultados.keys())
        tiempos_promedio = [np.mean(resultados[cantidad]) for cantidad in cantidades_procesos]

        plt.plot(cantidades_procesos, tiempos_promedio, marker='o')
        plt.xlabel('Cantidad de Procesos')
        plt.ylabel('Tiempo Promedio de Realización')
        plt.title(titulo)
        plt.grid(True)
        plt.show()

def ejecutar_multiples_simulaciones(memoria_total, velocidad_cpu, num_cpus, intervalos, titulo):
    resultados = {25: [], 50: [], 100: [], 150: [], 200: []}

    for cantidad in resultados.keys():
        for _ in range(intervalos):  #aca intervalo de llegada de procesos
            env = simpy.Environment()
            simulador = Simulador(env, memoria_total=memoria_total, velocidad_cpu=velocidad_cpu, num_cpus=num_cpus)
            procesos = [Proceso(id=i, memoria_requerida=np.random.randint(10, 30), instrucciones=np.random.randint(50, 150)) for i in range(cantidad)]
            simulador.ejecutar_simulacion(procesos)
            resultados[cantidad].append(np.mean(simulador.tiempos_finales))
            simulador.tiempos_finales.clear()  # clear los tiempos para la siguiente simulación

    simulador.graficar_resultados(resultados, titulo)

# estrategias para mejorar el tiempo promedio
# i. Incrementar la memoria a 200
ejecutar_multiples_simulaciones(memoria_total=200, velocidad_cpu=3, num_cpus=1, intervalos=1, titulo='Memoria 200, CPU 3, 1 CPU')
# ii. Memoria 100, CPU más rápido (6 instrucciones por unidad de tiempo)
ejecutar_multiples_simulaciones(memoria_total=100, velocidad_cpu=6, num_cpus=1, intervalos=1, titulo='Memoria 100, CPU 6, 1 CPU')
# iii. Velocidad normal del procesador pero emplear 2 procesadores
ejecutar_multiples_simulaciones(memoria_total=100, velocidad_cpu=3, num_cpus=2, intervalos=1, titulo='Memoria 100, CPU 3, 2 CPUs')