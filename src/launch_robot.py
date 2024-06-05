import pika 
import json 
from clases.robot import Robot
from format.print_pretty import print_pretty

localhost = 'localhost'
uam_server = 'redes2.ii.uam.es'
host = localhost 

class LaunchRobot:
    
    def __init__(self):
        # Conexión al broker RabbitMQ en localhost 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaración de las colas 
        self.channel.queue_declare(queue='2321_04_controlador_robots_queue', durable=False, auto_delete=True)
        self.channel.queue_declare(queue='2321_04_robots_controlador_queue', durable=False, auto_delete=True)

        print(' [Robot] Robot esperando mensajes...')

        # Inicio el robot 
        self.robot = Robot()


    # Callback para la recepción de mensajes 
    def callback(self, ch, method, properties, body):
        message = body.decode()
        json_message = json.loads(message) 
        accion = json_message['accion']
        id_pedido = json_message['id_pedido']
        client_id = json_message['client_id']
        
        print(f" [Robot] Mensaaje recibido del controlador: ")
        print_pretty(json_message=json_message) 
        
        if accion == 'MOVE':
            print(f" [Robot] Buscando productos...")

            result, productos = self.robot.realizarTrabajo(json_message=json_message)
            if result == True: 
                message = {"accion": "MOVED",
                        "id_pedido": id_pedido,
                        "product_ids": productos, 
                        "client_id": client_id}
                json_message = json.dumps(message)
            else: 
                message = {"accion": "NOT-MOVED",
                        "id_pedido": id_pedido,
                        "product_ids": productos, 
                        "client_id": client_id}
                json_message = json.dumps(message)
                
            self.channel.basic_publish(exchange='', routing_key='2321_04_robots_controlador_queue', body=json_message)

    def consume(self):
        # Establecemos el envío justo -> Solo 1 mensaje va a recibir el controlador a la vez 
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='2321_04_controlador_robots_queue', on_message_callback=self.callback, auto_ack=True)

        # Empezamos a consumir los mensajes 
        self.channel.start_consuming()

        
if __name__ == '__main__':
    try: 
        launch_robot = LaunchRobot()
        launch_robot.consume()
    except KeyboardInterrupt:
        print(" [Robot] Robot terminado")
        launch_robot.connection.close()