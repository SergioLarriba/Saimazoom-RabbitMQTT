import pika 
import json 
from clases.delivery import Delivery
from clases.pedido import EnumEstadosPedido
from format.print_pretty import print_pretty 

localhost = 'localhost'
uam_server = 'redes2.ii.uam.es'
host = localhost 

class LaunchDelivery:
    
    def __init__(self):
        # Conexión al broker RabbitMQ en localhost 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaración de las colas 
        self.channel.queue_declare(queue='2321_04_repartidores_controlador_queue', durable=False, auto_delete=True)
        self.channel.queue_declare(queue='2321_04_controlador_repartidores_queue', durable=False, auto_delete=True)

        print(' [Repartidor] Repartidor esperando mensajes...')

        # Iniciar el repartidor 
        self.repartidor = Delivery()

    # Callback para la recepción de mensajes 
    def callback(self, ch, method, properties, body):
        message = body.decode()
        json_message = json.loads(message)
        
        accion = json_message['accion']
        id_pedido = json_message['id_pedido'] 
        product_ids = json_message['product_ids']
        client_id = json_message['client_id']
        estado_pedido = json_message['estado']
        
        if accion == 'DELIVERY' and estado_pedido != EnumEstadosPedido.EN_PREPARACION:
            print(f" [Repartidor] Mensaje recibido del controlador: ")
            print_pretty(json_message=json_message)
            print(" [Repartidor] Repartiendo pedido...")
                    
            done = self.repartidor.entregarPedido() 
            if done == True:
                # Pedido entregado con éxito -> Se lo digo al controlador para que se lo diga al cliente 
                response = {"accion": "DELIVERED", 
                            "id_pedido": id_pedido, 
                            "product_ids": product_ids, 
                            "client_id": client_id}
                response = json.dumps(response) 
                
                self.channel.basic_publish(exchange='', routing_key='2321_04_repartidores_controlador_queue', body=response)
            else:
                # No se ha podido entregar el pedido -> Igualmente se lo digo al controlador 
                response = {"accion": "NOT-DELIVERED", 
                            "id_pedido": id_pedido, 
                            "product_ids": product_ids, 
                            "client_id": client_id}
                response = json.dumps(response) 
                self.channel.basic_publish(exchange='', routing_key='2321_04_repartidores_controlador_queue', body=response)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='2321_04_controlador_repartidores_queue', on_message_callback=self.callback, auto_ack=True)

        # Empezamos a consumir los mensajes 
        self.channel.start_consuming()
        
        
if __name__ == '__main__':
    try:
        launch = LaunchDelivery()
        launch.consume()
    except KeyboardInterrupt:
        print(' [Repartidor] Repartidor terminado')
        launch.connection.close()

