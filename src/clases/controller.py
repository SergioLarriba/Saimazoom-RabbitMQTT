from clases.client import Client
from clases.pedido import * 
import uuid
import pickle 
import os 

class Controller: 
    clientes_registrados: list[Client] = [] 
    pedidos_realizados: list[Pedido] = []
    
    def __init__(self): 
        orders_serialized = "orders.pickle"
        clientes_serialized = "clients.pickle"
        
        # Si existen los archivos serializados, los cargo 
        path_orders = os.path.join(os.getcwd(), 'pickle', orders_serialized)
        path_clients = os.path.join(os.getcwd(), 'pickle', clientes_serialized)
        
        # Cargo los clientes registrados
        if os.path.exists(path_clients):
            with open(path_clients, 'rb') as file:
                self.clientes_registrados = pickle.load(file)            
                
        # Cargo los pedidos realizados
        if os.path.exists(path_orders):
            with open(path_orders, 'rb') as file:
                self.pedidos_realizados = pickle.load(file)
    
    def registrarCliente(self, message):
        accion = message["accion"]
        user = message["user"]
        password = message["password"]
        
        for cliente in self.clientes_registrados:
            if cliente.getUser() == user: 
                return None
        
        if accion == 'REGISTER' and user is not None and password is not None: 
            # Si el mensaje está bien -> registro al cliente 
            cliente = Client(user=user, password=password)
            cliente.registrarCliente() 
            
            self.clientes_registrados.append(cliente)
            
            # Guardar los clientes registrados
            self.serialize_clients_and_orders()
            
            return cliente
        else:
            print("ERROR al registrar el cliente")
            return None 
        
    def loginCliente(self, user, password):
        for cliente in self.clientes_registrados:
            if cliente.getUser() == user and cliente.getPassword() == password:
                return True 
        return False
        
    def realizarPedido(self, message):
        if message is None:
            print("Introduzca un mensaje no vacio")
            return None
        
        # Realizo el pedido 
        client_id = message["client_id"]
        product_ids = message["product_ids"] 
        id_pedido = str(uuid.uuid4())
        pedido = Pedido(client_id=client_id, product_ids=product_ids, id_pedido=id_pedido)
        
        # Inserto el pedido realizado en el array de pedidos realizados y en el array de pedidos del cliente
        self.pedidos_realizados.append(pedido)
        self.getClientFromClientId(client_id).realizarPedido(pedido)
        
        # Guardar los pedidos registrados
        self.serialize_clients_and_orders()
        
        return pedido  
    
    def setEstadoPedido(self, id_pedido, estado):
        pedido = self.getPedidoFromId(id_pedido=id_pedido)
        if pedido in self.pedidos_realizados and pedido.sePuedeProcesarElPedido() == True:
            pedido.setEstadoPedido(estado=estado)
            return True 
        return False
    
    def cancelarPedido(self, id_pedido):
        pedido = self.getPedidoFromId(id_pedido=id_pedido) 
        if pedido in self.pedidos_realizados and (pedido.cancelarPedido() == True): 
            return True 
        return False 
    
    def verPedidos(self, id_cliente):
        pedidos = []
        for pedido in self.pedidos_realizados:
            if pedido.getClientId() == id_cliente:
                pedidos.append(pedido)
        return pedidos 
    
    # Persistencia de clientes y pedidos 
    def serialize_clients_and_orders(self):
        os.makedirs('pickle', exist_ok=True)

        serialized_clients = pickle.dumps(self.clientes_registrados)
        with open('pickle/clients.pickle', 'wb') as file:
            file.write(serialized_clients)
                
        serialized_orders = pickle.dumps(self.pedidos_realizados)
        with open('pickle/orders.pickle', 'wb') as file:
            file.write(serialized_orders)
        
    def getClientesRegistrados(self): 
        return self.clientes_registrados 
    
    def getClientFromClientId(self, client_id):
        for cliente in self.clientes_registrados:
            if cliente.getClientId() == client_id:
                return cliente 
        return None 
    
    def getClientIdFromUser(self, user):
        for cliente in self.clientes_registrados:
            if cliente.getUser() == user:
                return cliente.getClientId()
        return None 
    
    def isClienteRegistrado(self, user):
        for cliente in self.clientes_registrados:
            if cliente.getUser() == user:
                return True 
        return False 
    
    def getPedidoFromId(self, id_pedido):
        for pedido in self.pedidos_realizados:
            if pedido.getIdPedido() == id_pedido:
                return pedido
        return None 

    def containsPedido(self, id_pedido):
        for pedido in self.pedidos_realizados:
            if pedido.getIdPedido() == id_pedido:
                return True 
        return False
    
