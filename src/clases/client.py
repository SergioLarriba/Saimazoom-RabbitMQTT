from clases.pedido import *
from prettytable import PrettyTable
import uuid
import json 

class Client: 
    pedidos_realizados: list[Pedido] = []
    
    def __init__(self, user, password): 
        self.client_id = str(uuid.uuid4())
        self.registrado = False 
        self.user = user    
        self.password = password
        
    def registrarCliente(self): 
        self.registrado = True 
        
    def getRegistrado(self): 
        return self.registrado 
    
    def getClientId(self): 
        return self.client_id 
    
    def getUser(self): 
        return self.user
    
    def getPassword(self):
        return self.password
    
    def isRegistrado(self):
        if self.registrado == True: 
            return True 
        return False 
    
    def realizarPedido(self, pedido): 
        self.pedidos_realizados.append(pedido)

    @classmethod
    def imprimir_pedidos(cls, pedidos_str):
        tabla = PrettyTable(["ID Pedido", "ID Cliente", "Productos", "Estado"])
        for pedido_json in pedidos_str:
            pedido = json.loads(pedido_json)  # Convertir la cadena JSON a un diccionario
            tabla.add_row([pedido['id_pedido'], pedido['client_id'], ', '.join(pedido['product_ids']), pedido['estadoPedido']])
        
        print(tabla)
        
        