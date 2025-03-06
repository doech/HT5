#Emily Gongora Camila Sandoval Alejandra Sierra
#gestionar la memoria del sistema para los procesos.  asignar y liberar memoria

import simpy

class RAM:
    def __init__(self, env, memoria_total):
        self.env = env
        self.memoria_total = memoria_total
        self.memoria_disponible = simpy.Container(env, init=memoria_total, capacity=memoria_total)

    def reservar_memoria(self, proceso):
        yield self.memoria_disponible.get(proceso.memoria_requerida)

    def liberar_memoria(self, proceso):
        yield self.memoria_disponible.put(proceso.memoria_requerida)

