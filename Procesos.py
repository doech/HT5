# Emily Góngora, Camila Sandoval, Ale Sierra
# clase que crea procesos y los hace pasar por los estados de un ciclo de vida de un proceso
import random
import simpy

class Proceso:
    def __init__(self, env, id_proceso, ram, cpu):
        self.env = env
        self.id_proceso = id_proceso
        self.ram = ram
        self.cpu = cpu
        self.memoria_requerida = random.randint(1, 10)
        self.instrucciones = random.randint(1, 10)
        self.estado = 'new'
    
    def ciclo_vida(self):
        self.estado = 'waiting'
        print (f'Proceso {self.id_proceso} en estado {self.env.now}: Está solicitando {self.memoria_requerida} de memoria RAM')
        yield self.ram.get(self.memoria_requerida)
        
        self.estado = 'ready'
        print (f'Proceso {self.id_proceso} en estado {self.env.now}: listo para pasar a la CPU')

        while self.instrucciones > 0:
            with self.cpu.request() as req:
                yield req
                self.estado = 'running'
                print (f'Proceso {self.id_proceso} en estado {self.env.now}: en ejecución')
                instrucciones_a_ejecutar = min (3, self.instrucciones)
                yield self.env.timeout(1)
                self.instrucciones -= instrucciones_a_ejecutar
                print (f'Proceso {self.id_proceso} en estado {self.env.now}: instrucciones restantes {self.instrucciones}')
            if random.ranint(1, 20) == 1:
                self.estado = 'waiting'
                print (f'Proceso {self.id_proceso} en estado {self.env.now}: solicitando E/S')
                yield self.env.timeout(random.randint(1, 3))
                print (f'Proceso {self.id_proceso} en estado {self.env.now}: E/S completada')
            self.estado = 'ready'
        self.estado = 'terminated'
        print (f'Proceso {self.id_proceso} en estado {self.env.now}: terminado')
        yield self.ram.put(self.memoria_requerida)
