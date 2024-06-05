import uuid

class EnumEstadosPedido: 
    EN_ALMACEN = "EN_ALMACEN"
    EN_PREPARACION = "EN_PREPARACION"
    EN_CINTA = "EN_CINTA"
    EN_RUTA = "EN_RUTA"
    ENTREGADO = "ENTREGADO"
    
    ERROR = "ERROR"
    CANCELADO = "CANCELADO"
    
class Pedido: 
    product_ids = [] 
    
    def __init__(self, client_id, product_ids, id_pedido):
        self.estadoPedido = EnumEstadosPedido.EN_ALMACEN
        self.id_pedido = id_pedido
        self.client_id = client_id
        self.product_ids = product_ids
        
    def cancelarPedido(self):
        # Si el cliente cancela un pedido -> el estado pasa a "CANCELADO"
        if self.sePuedeCancelarPedido(self.estadoPedido) == True:
            self.estadoPedido = EnumEstadosPedido.CANCELADO 
            return True
        return False 
        
    def getIdPedido(self):
        return self.id_pedido 
    
    def getProductIds(self):
        return self.product_ids 
    
    def getEstadoPedido(self):
        return self.estadoPedido
    
    def estadoValido(self, estado):
        if estado in EnumEstadosPedido.__dict__.values():   
            return True 
        return False 
    
    def setEstadoPedido(self, estado):
        if self.estadoValido(estado=estado) == True:
            self.estadoPedido = estado
            return True 
        else:
            return False 
        
    def sePuedeCancelarPedido(self, estado):
        if estado == EnumEstadosPedido.EN_ALMACEN or estado == EnumEstadosPedido.EN_PREPARACION or estado == EnumEstadosPedido.EN_CINTA:
            return True 
        return False
        
    def sePuedeProcesarElPedido(self):
        if (self.estadoPedido != EnumEstadosPedido.ERROR and self.estadoPedido != EnumEstadosPedido.CANCELADO):
            return True
        return False 
    
    def getClientId(self):
        return self.client_id
    
    def to_dict(self):
        return {
            'id_pedido': self.id_pedido,
            'client_id': self.client_id,
            'product_ids': self.product_ids,
            'estadoPedido': self.estadoPedido
        }
        
            
        
        
        
         