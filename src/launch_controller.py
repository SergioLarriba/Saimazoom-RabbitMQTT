import pika 
import json 
from clases.controller import Controller
from format.print_pretty import print_pretty
from clases.pedido import * 

localhost = 'localhost'
uam_server = 'redes2.ii.uam.es'
host = localhost 

class LaunchController:
    
    def __init__(self):
        # Conexión al broker RabbitMQ en localhost 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaracion de las colas 
        # RPC queue 
        self.channel.queue_declare(queue='2321_04_rpc_queue', durable=False)

        self.channel.queue_declare(queue='2321_04_controlador_robots_queue', durable=False, auto_delete=True)
        self.channel.queue_declare(queue='2321_04_robots_controlador_queue', durable=False, auto_delete=True)
        self.channel.queue_declare(queue='2321_04_repartidores_controlador_queue', durable=False, auto_delete=True)
        self.channel.queue_declare(queue='2321_04_controlador_repartidores_queue', durable=False, auto_delete=True)
        
        print(' [Controlador] Controlador esperando mensajes...')

        # Iniciar el controlador 
        self.controller = Controller() 
        
        
    def on_request(self, ch, method, properties, body): 
        message = body.decode()
        message = json.loads(message)
        print(f" [Controlador] Recibido del cliente: ")
        print_pretty(json_message=message) 
        
        accion = message['accion'] 
        user = message['user']
        
        # CLIENTE SE REGISTRA  
        if accion == 'REGISTER': 
            # Registramos el cliente 
            password = message['password']
            
            clienteRegistrado = self.controller.registrarCliente(message=message) 
            if clienteRegistrado is not None:
                message = {"accion": "REGISTERED",
                            "client_id": clienteRegistrado.getClientId(), 
                            "user": user,
                            "password": password
                }
                message = json.dumps(message).encode()
            else:
                message = {"accion": "NOT-REGISTERED",
                            "user": user,
                            "password": password, 
                            "causa": "El cliente ya existe"
                }
                message = json.dumps(message).encode()
                
           # Envío mensaje al cliente
            self.channel.basic_publish(exchange='',
                                    routing_key=properties.reply_to,
                                    properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                    body=message)
        # CLIENTE SE LOGUEA
        elif accion == 'LOGIN':
            # El cliente se loguea 
            password = message['password']
            
            if self.controller.loginCliente(user=user, password=password) == True:
                message = {"accion": "LOGGED",
                            "client_id": self.controller.getClientIdFromUser(user=user), 
                            "user": user,
                            "password": password
                }
                message = json.dumps(message).encode()
            else:
                message = {"accion": "NOT-LOGGED",
                            "client_id": self.controller.getClientIdFromUser(user=user), 
                            "user": user,
                            "password": password, 
                            "causa": "Usuario o contraseña incorrectos"
                }
                message = json.dumps(message).encode()
            # Envío mensaje al cliente
            self.channel.basic_publish(exchange='',
                                    routing_key=properties.reply_to,
                                    properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                    body=message)        
        # CLIENTE REALIZA PEDIDO 
        elif accion == 'ORDER': 
            # El cliente tiene que realizar un pedido 
            # 1 - Compruebo si el cliente está registrado         
            if self.controller.isClienteRegistrado(user=user) == True:
                # 2 - Hago el pedido y si todo ha ido bien, le digo al cliente que su pedido se está procesando 
                message['client_id'] = self.controller.getClientIdFromUser(user=user)
                pedido = self.controller.realizarPedido(message=message) 
                
                if pedido.sePuedeProcesarElPedido() == True: 
                    message = {"accion": "ORDERED", 
                            "id_pedido": pedido.getIdPedido(), 
                            "product_ids": pedido.getProductIds(), 
                            "client_id": self.controller.getClientIdFromUser(user=user)}
                    message = json.dumps(message).encode()
                    
                    # Envío mensaje al cliente
                    self.channel.basic_publish(exchange='',
                                            routing_key=properties.reply_to,
                                            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                            body=message)
                    
                    # 3 - Poner a los robots en marcha -> Les pongo un mensaje en la cola 
                    # Cambio el estado del pedido a EN_PREPARACION
                    pedido.setEstadoPedido(EnumEstadosPedido.EN_PREPARACION)
                    
                    # Verificar si el cliente ha cancelado el pedido 
                    if pedido is not None and pedido.sePuedeProcesarElPedido() == True: 
                        message = {"accion": "MOVE",
                                    "id_pedido": pedido.getIdPedido(),
                                    "product_ids": pedido.getProductIds(),
                                    "client_id": self.controller.getClientIdFromUser(user=user), 
                                    "estado": pedido.getEstadoPedido()}
                        json_message = json.dumps(message)
                        
                        self.channel.basic_publish(exchange='', routing_key='2321_04_controlador_robots_queue', body=json_message)
                        # 4 - Responder al cliente con lo que haya pasado -> función callback_robots
                    else: 
                        # Cambio el estado del pedido a CANCELADO
                        pedido.setEstadoPedido(EnumEstadosPedido.CANCELADO)
                        
                        message = {"accion": "CANCELLED",
                                    "id_pedido": pedido.getIdPedido(),
                                    "user": user}
                        message = json.dumps(message).encode()
                        
                        # Envío mensaje al cliente
                        self.channel.basic_publish(exchange='',
                                                routing_key=properties.reply_to,
                                                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                                body=message)
                else:
                    print("Error al realizar el pedido")
                    
        # CLIENTE CANCELA PEDIDO 
        elif accion == 'CANCEL':
            client_id = self.controller.getClientIdFromUser(user=user)
            # El cliente tiene que estar registrado y el pedido no puede estar en reparto
            if self.controller.isClienteRegistrado(user=user) == True:
                id_pedido = message["id_pedido"]
                if (self.controller.cancelarPedido(id_pedido=id_pedido) == True):
                    # El pedido se ha cancelado correctamente 
                    message = {"accion": "CANCELLED",
                            "id_pedido": id_pedido,
                            "client_id": client_id
                    }
                    message = json.dumps(message).encode()

                else: 
                    message = {"accion": "NOT-CANCELLED",
                            "id_pedido": id_pedido,
                            "client_id": client_id,
                            "causa": "El pedido no existe o ya está en reparto"
                    }
                    message = json.dumps(message).encode()

            else:
                message = {"accion": "NOT-CANCELLED",
                        "id_pedido": id_pedido,
                        "client_id": client_id, 
                        "causa": "El cliente no está registrado"
                }
                message = json.dumps(message).encode()
            # Envío mensaje al cliente
            self.channel.basic_publish(exchange='',
                                    routing_key=properties.reply_to,
                                    properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                    body=message)
            
        elif accion == 'SEE':
            client_id = self.controller.getClientIdFromUser(user=user)
            if self.controller.isClienteRegistrado(user=user) == True:
                pedidos = self.controller.verPedidos(id_cliente=client_id)
                pedidos_str = [json.dumps(pedido.to_dict()) for pedido in pedidos]

                message = {"accion": "SEEN",
                        "client_id": client_id, 
                        "pedidos": pedidos_str
                }
                message = json.dumps(message).encode()
            else:
                message = {"accion": "NOT-SEEN",
                        "client_id": client_id,
                        "causa": "El cliente no está registrado"}
                message = json.dumps(message).encode()
                
            # Envío mensaje al cliente
            self.channel.basic_publish(exchange='',
                                    routing_key=properties.reply_to,
                                    properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                    body=message)

                
    def callback_robots(self, ch, method, properties, body):
        message = body.decode()
        json_message = json.loads(message)
        accion = json_message['accion']
        id_pedido = json_message['id_pedido']
        product_ids = json_message['product_ids'] 
        client_id = json_message['client_id']
        
        pedido = self.controller.getPedidoFromId(id_pedido=id_pedido) 
        
        # Si no se ha cancelado -> pongo en marcha a los repartidores
        if pedido.getEstadoPedido() != EnumEstadosPedido.CANCELADO:
            print(f" [Controlador] Mensaje recibido de los robots: ")
            print_pretty(json_message=json_message)
            if accion == 'MOVED':
                # Cambio el estado del pedido a EN_CINTA
                self.controller.setEstadoPedido(id_pedido=id_pedido, estado=EnumEstadosPedido.EN_CINTA)
                
                if pedido.sePuedeProcesarElPedido() == True:
                    # Cambio el estado del pedido a EN_RUTA
                    self.controller.setEstadoPedido(id_pedido=id_pedido, estado=EnumEstadosPedido.EN_RUTA)
                    
                    delivery_message = {"accion": "DELIVERY",
                                        "id_pedido": id_pedido,
                                        "product_ids": product_ids, 
                                        "client_id": client_id, 
                                        "estado": pedido.getEstadoPedido()}
                    delivery_message = json.dumps(delivery_message) 
                    
                    self.channel.basic_publish(exchange='', routing_key='2321_04_controlador_repartidores_queue', body=delivery_message)
                
            elif accion == 'NOT-MOVED':
                print("Error al mover los productos de los robots")
        
        
    def callback_repartidores(self, ch, method, properties, body):
        
        message = body.decode()
        message = json.loads(message)
        # print(f" [Repartidor] Recibido: {message}") 
        
        accion = message['accion']
        id_pedido = message['id_pedido']
        product_ids = message['product_ids'] 
        client_id = message['client_id']
        
        pedido = self.controller.getPedidoFromId(id_pedido=id_pedido)
            
        if pedido.sePuedeProcesarElPedido() == True:
            print(f" [Controlador] Mensaje recibido de los repartidores: ")
            print_pretty(json_message=message)
            
            if accion == 'DELIVERED':
                # Cambio el estado del pedido a ENTREGADO
                pedido.setEstadoPedido(EnumEstadosPedido.ENTREGADO) 
            else:
                # Cambio el estado del pedido a ERROR
                pedido.setEstadoPedido(EnumEstadosPedido.ERROR) 
            
    
    def consume(self):
        # Establecemos el envío justo -> Solo 1 mensaje va a recibir el controlador a la vez 
        self.channel.basic_qos(prefetch_count=1)
        
        self.channel.basic_consume(queue='2321_04_robots_controlador_queue', on_message_callback=self.callback_robots, auto_ack=True)
        self.channel.basic_consume(queue='2321_04_repartidores_controlador_queue', on_message_callback=self.callback_repartidores, auto_ack=True)
        self.channel.basic_consume(queue='2321_04_rpc_queue', on_message_callback=self.on_request, auto_ack=True)

        # Empezamos a consumir los mensajes 
        self.channel.start_consuming()
        
if __name__ == '__main__':
    try:
        launch_controller = LaunchController()
        launch_controller.consume() 
    except KeyboardInterrupt:
        print(" [Controlador] Controlador terminado")
        launch_controller.connection.close() 
