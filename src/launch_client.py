from asyncio import sleep
import json  
import pika 
from clases.client import Client
from format.print_pretty import print_pretty
import uuid

localhost = 'localhost'
uam_server = 'redes2.ii.uam.es'
host = localhost 

class LaunchClient():

        def __init__(self):
                # Usuario que se registra
                self.user_register = Client(user="admin10", password="admin10")
                
                # Usuario que se loguea
                self.user_login = Client(user="alumnodb1", password="alumnodb")
                self.client_id = self.user_login.getClientId()
                
                # Establezco una conexión con RabbitMQ 
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
                self.channel = self.connection.channel()

                # Declaración de las colas 
                # RPC queue 
                result = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
                self.callback_queue = result.method.queue
                # self.channel.basic_qos(prefetch_count=1)

                
                self.channel.basic_consume(queue=self.callback_queue, 
                                        on_message_callback=self.on_response, 
                                        auto_ack=True)
                self.corr_id = None
        
        def on_response(self, ch, method, properties, body):    
                if self.corr_id == properties.correlation_id:
                        self.response = body.decode()
                        message = json.loads(self.response)
                        
                        print(f" [Cliente] Mensaje recibido por el controlador...")
                        accion = message['accion']
                        if accion != 'SEEN':
                                print_pretty(json_message=message)
                        else: 
                                pedidos_str = message['pedidos']
                                Client.imprimir_pedidos(pedidos_str)
        
                                
        def call(self, message): 
                self.corr_id = str(uuid.uuid4())
                self.channel.basic_publish(exchange='', 
                                           routing_key='2321_04_rpc_queue', 
                                           properties=pika.BasicProperties(reply_to=self.callback_queue, 
                                                                        correlation_id=self.corr_id),
                                        body=message)
                self.connection.process_data_events(time_limit=None)

        def register(self):
                message = {"accion": "REGISTER", 
                           "user": self.user_register.getUser(),
                           "password": self.user_register.getPassword()}
                
                print(f" [Cliente] Mensaje de registro enviado al controlador: ")
                print_pretty(json_message=message)
                
                message = json.dumps(message).encode()

                self.call(message)
                
        def login(self):
                message = {"accion": "LOGIN", 
                           "user": self.user_login.getUser(), 
                           "password": self.user_login.getPassword()}
                                
                print(f" [Cliente] Mensaje de logueo enviado al controlador: ")
                print_pretty(json_message=message)
        
                message = json.dumps(message).encode()

                self.call(message)
        
        def hacer_pedido(self): 
                product_ids = ["P1", "P2", "P3"] 
                message = {"accion": "ORDER", 
                        "product_ids": product_ids, 
                        "user": self.user_login.getUser(),
                }
                print(f" \n[Cliente] Mensaje enviado al controlador: ")
                print_pretty(json_message=message)
                message = json.dumps(message).encode()
                
                self.call(message)
        
        def ver_pedido(self): 
                message = {"accion": "SEE", 
                   "user": self.user_login.getUser(), 
                }
        
                print(f" \n[Cliente] Mensaje enviado al controlador: ")
                print_pretty(json_message=message)
                message = json.dumps(message)
                
                self.call(message)


if __name__ == "__main__":
        try:
                client = LaunchClient()
                client.register()
                client.login()
                client.hacer_pedido()
                client.ver_pedido()
                client.connection.close()
        except KeyboardInterrupt:
                print(" [Cliente] Cliente terminado")
                client.connection.close() 
        
