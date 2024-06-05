import time 
import random 
from clases.controller import * 
from clases.pedido import * 

class Robot:
    tiempo_trabajo = random.uniform(5, 10)
    p_almacen = 0.8 
    
    def __init__(self):
        pass 
    
    # Va a recibir entre " " los id de los productos a poner en la cinta 
    def realizarTrabajo(self, json_message): 
        productos_no_encontrados = [] 

        productos = json_message['product_ids']  
        for producto in productos: 
            if round(random.uniform(0, 1), 1) <= self.p_almacen:
                # El robot ha encontrado el producto -> procede e ponerlo en la cinta transportadora 
                time.sleep(self.tiempo_trabajo)
            else:
                productos_no_encontrados.append(producto)
        
        if productos_no_encontrados == []:
            return True, productos
        
        return False, productos_no_encontrados   
    
    def getTiempoTrabajo(self):
        return self.tiempo_trabajo
    
    def getP_Almacen(self):
        return self.p_almacen
    
    def setP_Almacen(self, p_almacen):
        self.p_almacen = p_almacen
        return 
                
            
            
        
    