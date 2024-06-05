import time 
import random 
from clases.pedido import * 

class Delivery: 
    p_entrega = 0.8
    
    def __init__(self):
        pass 
    
    def entregarPedido(self):
        # Cada repartidor intenta entregar el paquete 3 veces con una probabilidad de éxito p_entrega
        for i in range (0, 3):
            # Intento -> espera aleatoria entre 10 y 20 segundos 
            time.sleep(random.uniform(10, 20))
            if round(random.uniform(0, 1), 1) < self.p_entrega:
                return True
            
        return False 
    
