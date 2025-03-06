import simpy

class CPU:
    def _init_(self, env, velocidad):
        self.env = env
        self.velocidad = velocidad  # Instrucciones por unidad de tiempo

    def procesar(self, proceso):
        """ Ejecuta instrucciones en el CPU. """
        instrucciones_a_ejecutar = min(proceso.instrucciones, self.velocidad)
        yield self.env.timeout(1)  # Simula el tiempo de procesamiento
        proceso.instrucciones -= instrucciones_a_ejecutar
