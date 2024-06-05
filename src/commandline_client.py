import pika 
import json
import uuid
from format.print_pretty import print_pretty
from clases.client import Client

localhost = 'localhost'
uam_server = 'redes2.ii.uam.es'
host = localhost 

class SaimazoonClient:
    
    def __init__(self): 
        self.user = None
        self.password = None
        self.loggedin = False 
        
        # Establezco una conexión con RabbitMQ 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        
        # Deckaración de la cola RPC
        result = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        self.callback_queue = result.method.queue
        
        self.channel.basic_consume(queue=self.callback_queue, 
                                   on_message_callback=self.on_response, 
                                   auto_ack=True)
        self.corr_id = None
        self.response = None
    
    
    def on_response(self, ch, method, properties, body):    
        if self.corr_id == properties.correlation_id:
            self.response = body.decode()
            message = json.loads(self.response)
            
            accion = message['accion']

            print(f" [Cliente] Mensaje recibido por el controlador: ")
            
            if accion != 'SEEN':
                print_pretty(json_message=message)
                if accion == 'REGISTERED':
                    self.loggedin = True
                elif accion == 'LOGGED': 
                    self.loggedin = True
                elif accion == 'NOT-REGISTERED':
                    print(f"{message['causa']}")
            else: 
                pedidos_str = message['pedidos']
                Client.imprimir_pedidos(pedidos_str)
        else: 
            return 
            
    def send_to_controller(self, message): 
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='2321_04_rpc_queue',
            body = message,
            properties=pika.BasicProperties(reply_to=self.callback_queue,correlation_id=self.corr_id)
        )
        self.connection.process_data_events(time_limit=None)
    
    def registrar_cliente(self):
        # Mientras no esté registrado... 
        while self.loggedin == False:           
            opcion = input("Seleccione una opcion: \n1. Registrarse\n2. Log-In\nCtrl+C para salir\n")
            
            if opcion == '1': # REGISTRO
                # Solicito los datos 
                self.user = input("Introduzca el usuario: ")
                self.password = input("Introduzca la contraseña: ")
                
                # Generamos mensaje para el controlador 
                message = {"accion": "REGISTER", 
                           "user": self.user,
                           "password": self.password}
                
                print(f" \n[Cliente] Mensaje enviado al controlador: ")
                print_pretty(json_message=message)
                
                message = json.dumps(message)
                                
                # Mandamos mensaje al controlador 
                self.send_to_controller(message)
            elif opcion == '2': #LOG-IN
                # Solicito los datos 
                self.user = input("Introduzca el usuario: ")
                self.password = input("Introduzca la contraseña: ")
                
                # Generamos mensaje para el controlador
                message = {"accion": "LOGIN",
                            "user": self.user,
                            "password": self.password}
                
                print(f" \n[Cliente] Mensaje enviado al controlador: ")
                print_pretty(json_message=message)
                
                message = json.dumps(message)

                # Mandamos mensaje al controlador
                self.send_to_controller(message)
            
        
    def hacer_pedido(self, producto):        
        # Generamos mensaje para el controlador
        product_ids = [producto]
        message = {"accion": "ORDER", 
                   "product_ids": product_ids, 
                   "user": self.user,}
        
        print(f" \n[Cliente] Mensaje enviado al controlador: ")
        print_pretty(json_message=message)
        
        message = json.dumps(message)
        
        # Mandamos mensaje al controlador
        self.send_to_controller(message)
       
    
    def ver_pedidos(self):        
        # Generamos mensaje para el controlador 
        message = {"accion": "SEE", 
                   "user": self.user}
        
        print(f" \n[Cliente] Mensaje enviado al controlador: ")
        print_pretty(json_message=message)
        
        message = json.dumps(message)
        
        # Mandamos mensaje al controlador
        self.send_to_controller(message)
        print(f" \n[Cliente] Send: {message}")
            
    
    def cancelar_pedido(self, id_pedido):        
        # Generamos mensaje para el controlador
        message = {"accion": "CANCEL", 
                   "id_pedido": id_pedido, 
                   "user": self.user}
        
        print(f" \n[Cliente] Mensaje enviado al controlador: ")
        print_pretty(json_message=message)
        
        message = json.dumps(message)
        
        # Mandamos mensaje al controlador
        self.send_to_controller(message)

                
    def manejar_solicitudes(self):
        print("--------------------------- USUARIO ---------------------------")
        
        while True:
            print("¿Qué desea hacer?")
            print("1. Hacer pedido")
            print("2. Ver pedidos")
            print("3. Cancelar pedido")
            print("4. Salir")
            
            opcion = input("Opción: ")
            
            if opcion == '1':
                producto = input("Introduzca los productos (P1 P2 ...): ")
                self.hacer_pedido(producto)
            elif opcion == '2':
                self.ver_pedidos()
            elif opcion == '3':
                id_pedido = input("Introduzca el ID del pedido a cancelar: ")
                self.cancelar_pedido(id_pedido)
            elif opcion == '4':
                break
            else:
                print("Opción no válida")
        
    def getClientId(self):
        return self.client_id
    
def main():
    try:
        # 1 - Instancia de la clase SaimazoonClient + Conexión con RabbitMQ 
        client = SaimazoonClient() 
        # 2 - Registro de cliente (o log-in si ya está registrado)
        client.registrar_cliente()
        # 3 - Manejo de solicitudes e interacciones con el cliente 
        client.manejar_solicitudes()
        # 4 - Cierre de la conexión con RabbitMQ
        client.connection.close()
    except KeyboardInterrupt:
        print(" [Cliente] Cliente terminado")
        client.connection.close()
        exit(0)
    
if __name__ == '__main__':
    main()
    
    
    
    
