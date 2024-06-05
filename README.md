
# Índice

1. [Introdución](#introduccion)

2. [Definición del proyecto](#definicion)

3. [Implementación](#solucion)

3. [Conclusiones](#conclusiones)

  
  

# 1. Introducción

El objetivo de Saimazoom es el de crear un sistema para la gestión de pedidos online. Este sistema debe incluir a los actores:

* **Cliente**, que realiza y gestiona pedidos de productos.

* **Controlador** central, que gestiona todo el proceso.

* **Robots**, que se encargan de buscar los productos en el almacén y colocarlos en las cintas transportadoras.

* **Repartidores**, encargados de transportar el producto a la casa del cliente

* **Admin** encargados de gestionar la base de datos del controlador central

  

El sistema debe de gestionar las interacciones entre todos estos actores, para las comunicaciones correspondientes se empleará una cola de mensajes.

  
  

# 2. Definición del proyecto

El sistema Saimazoom, como conjunto, debe gestionar pedidos, en los que los **clientes** pueden solicitar un producto. Una vez recibido un pedido, el **controlador** debe avisar a un **robot**, que mueve dicho producto del almacén a la cinta transportadora. Una vez en la cinta transportadora, el controlador avisa a un **repartidor**, que lleva el producto a la casa del **cliente**.

<!-- Las comunicaciones pertinentes entre estos elementos estarán gestionadas por un **controlador** central, que mantiene la comunicación entre los **clientes**, **robots** y **repartidores**. -->

  

## 2.1. Objetivos y funcionalidad

Los objetivos principales son:

* La gestión de los pedidos de los **clientes**, que pueden hacer, ver y cancelar pedidos.

* La gestión de los **robots**, que reciben ordenes de de transportar los productos del almacen a la cinta transportadora.

* La gestión de los **repartidores**, que reparten los productos que hay en la cinta transportadora a la casa de los clientes.

* La gestión del **controlador** central, que tiene que mantener un control de productos, **clientes**, **robots** y **repartidores**. Tiene que guardar también los pedidos, con sus estados, que dependen de la relación con el resto de actores.

* La comunicación entre el **controlador** y el resto de actores

  

Para cumplir estos objetivos es necesario desarrollar una serie de funcionalidades básicas:

1. Registro de **Cliente**: registro desde una petición de un **Cliente** con un identificador de **cliente** que tiene que ser único.

2. Registro de Pedido: registro en la base de datos del **controlador** central con un id de **cliente** y de producto, también le asigna un estado al pedido.

3. Recepción de pedidos de los **Clientes**: hay que recibir y guardar los pedidos a realizar que están asociados a un **Cliente** y a un producto.

4. Asignación de trabajo a los **Robots**: hay que asignar a los **robots** las tareas de transporte de productos correspondientes a pedidos.

5. Asignación de trabajo a los **Repartidores**: hay que asignar a los **repartidores** las tareas de transporte de productos correspondientes a pedidos.

  

## 2.2. Requisitos

Nos limitaremos a los requisitos funcionales, estos los podemos dividir en los siguientes apartados:

  

### 2.2.1. **Lógica de clientes**

**LoCl1**. Registro en la aplicación en el que se recibe confirmación

**LoCl2**. Realizar un pedido, en el que se pide un producto

**LoCl3**. Pedir una lista de los pedidos realizados en la que se incluya id del producto correspondiente al pedido y estado del pedido

**LoCl4**. Pedir la cancelación de un pedido

  
  
  

# 3. Implementación

Una vez definidos los requerimientos del sistema, la solución propuesta empleada se describe en las siguientes secciones de forma general. Si se quieren ver los diagramas realizados (de clases, de colas, casos de uso, estados de un pedido), están adjuntados en la memoria en la raíz del proyecto. 

## 3.1 Diagrama de clases 
En el diagrama de clases se representan los diferentes componentes de la aplicación. Se pueden distinguir 2 tipos de clases, aquellas relacionadas con el lanzamiento de los componentes (empiezan por el prefijo “Launch”) y aquellas relacionadas con la gestión de la funcionalidad interna.

Cada clase “Launch” tiene asociada su clase de gestión interna. Las clases de tipo “Launch” sirven para toda la inicialización, envío y recepción de mensajes a través de las colas de mensajes, mientras que las otras clases sirven para funcionalidades más específicas.
Por ejemplo, la clase “LaunchClient” tiene toda la gestión del envío de mensajes por parte del cliente al controlador y la recepción de las respuestas de éste, sin embargo, dicha clase como tal no realiza ninguna funcionalidad interna (registro de un cliente por ejemplo), para ello se emplea la clase “Client”.

De esta forma conseguimos modularizar mucho más el código y separar las funcionalidades con el objetivo de hacer un código mucho más legible, modificable y entendible para cualquier nuevo integrante que desee formar parte del proyecto.

A continuación se adjunta el diagrama de clases realizado:

![Diagrama De Clases](https://git.eps.uam.es/redes2/2324/2301-2321/p04/practica2/-/blob/main/Dise%C3%B1o/Diagrama_De_Clases/Diagrama_De_Clases.png)

Como se puede observar, las colas, representadas por flechas discontinuas, conectan las diferentes
clases de tipo “Launch”, y la funcionalidad como tal de la aplicación la realizan el resto de clases,
cada una siendo accesible desde su respectiva clase “Launch”.
La clase “SaimazoonClient” corresponde al archivo commandline_client.py, que simula la interfaz
que recibiría un cliente por la línea de comandos. Dicha clase también es de tipo “Launch” y la clase
que gestiona su funcionamiento interno es “Client”, la misma para la clase “LaunchClient”.
## 3.2 Diagrama de estados de un pedido 
![Diagrama De Estados de un pedido](https://git.eps.uam.es/redes2/2324/2301-2321/p04/practica2/-/blob/main/Dise%C3%B1o/Diagrama_Estados_Pedido/Diagrama_Estados_Pedido_Final.png)
## 3.3 Diagrama de casos de uso
### 3.3.1 Pedido completado hasta el final
![Pedido completado hasta el final](https://git.eps.uam.es/redes2/2324/2301-2321/p04/practica2/-/blob/main/Dise%C3%B1o/Casos_De_Uso/Pedido_completado_hasta_el_final.png)
### 3.3.2 Pedido que se cancela antes de empezar el reparto
![Pedido que se cancela antes de empezar el reparto](https://git.eps.uam.es/redes2/2324/2301-2321/p04/practica2/-/blob/main/Dise%C3%B1o/Casos_De_Uso/Pedido_se_cancela_antes_del_reparto.png)
### 3.3.3 Pedido en el que el robot no encuentra el producto
![Pedido en el que el robot no encuentra el producto](https://git.eps.uam.es/redes2/2324/2301-2321/p04/practica2/-/blob/main/Dise%C3%B1o/Casos_De_Uso/Pedido_robot_no_encuentra_producto.png)

## 3.4 Diseño y uso de las colas de mensajes
Hemos usado tanto colas RPC (solicitud - respuesta) como colas de trabajo (distribuir tareas entre diferentes trabajadores).

  ![Diagrama de colas](https://git.eps.uam.es/redes2/2324/2301-2321/p04/practica2/-/blob/main/Dise%C3%B1o/Diagrama_Colas.png)

-   2321_04_rpc_queue: Esta cola funciona para que el cliente pueda generar mensajes, productor, que el controlador procesa, consumidor. Es de tipo RPC ya que en algunas ocasiones el cliente debe esperar una respuesta antes de continuar con su ejecución (por ejemplo al hacer login, hasta que no se loguea no puede hacer pedidos). Para otros casos, como el registro, se sigue haciendo uso de esta cola pero de manera asíncrona. Además, el objetivo principal que nos ha llevado a usar una RPC es para que el controlador sepa a qué cliente le está mandando la respuesta a su solicitud correspondiente.
    
-   2321_04_controlador_robots_queue: Esta cola sirve para enviar mensajes desde el controlador a los robots. Es una cola de trabajo (work queue), es decir, simplemente coloca los mensajes y el primer robot en estar disponible los recoge, permitiendo así dividir el trabajo entre múltiples entidades.
    
-   2321_04_robots_controlador_queue: Esta cola sirve exclusivamente para que los robots informen al controlador sobre el éxito o fracaso en la puesta de los productos solicitados en la cinta, al igual que la cola de ida, también es una cola de trabajo.
    
-   2321_04_controlador_repartidores_queue: Esta cola tiene un funcionamiento muy similar a la cola “2321_04_controlador_robots_queue”, y al igual que ella, también es una cola de trabajo, pero en vez de ser robots, esta vez son repartidores.
    

-   2321_04_repartidores_controlador_queue: Esta cola tiene un funcionamiento idéntico a la cola “2321_04_robots_controlador_queue” pero orientado a los repartidores. Simplemente sirve para avisar por parte de los repartidores al controlador del éxito o fracaso en la entrega.
## 3.5 Descripción de los mensajes: sintaxis y formato
Todos los mensajes intercambiados entre las diferentes colas de mensajes tienen formato JSON. Es un
formato ligero y fácilmente interpretable tanto por humanos como por máquinas, lo que agiliza el
procesamiento y la manipulación de la información.
#### Mensajes desde el cliente al controlador
- Registro:
message = {"accion": "REGISTER",
"user": "String con el nombre de usuario",
"password": "String con la contraseña"
}
- Login:
message = {"accion": "LOGIN",
"user": "String con el nombre de usuario",
"password": "String con la contraseña"
}
- Hacer pedido:
message = {"accion": "ORDER",
“product_ids”: [Array con los productos que pide el cliente en el pedido],
“user”: “String con el nombre de usuario”
}
- Ver pedido:
message = {"accion": "SEE",
“user”: “String con el nombre de usuario”
}
- Cancelar pedido:
message = {"accion": "CANCEL",
“id_pedido”: “String con el identificador del pedido a cancelar”,
“user”: “String con el nombre de usuario”
}
#### Mensajes desde el controlador al cliente (Respuesta a las solicitudes del cliente)
- Confirmación exitosa del registro:
message = {"accion": "REGISTERED",
“client_id”: “String con el id del cliente registrado”,
"user": "String con el nombre de usuario",
"password": "String con la contraseña"
}
- Fallo en el registro:
message = {"accion": "NOT-REGISTERED",
"user": "String con el nombre de usuario",
"password": "String con la contraseña",
“causa”: “El cliente ya existe”
}
- Confirmación exitosa del login:
message = {"accion": "LOGGED",
“client_id”: “String con el id del cliente registrado”,
"user": "String con el nombre de usuario",
"password": "String con la contraseña"
}
- Fallo en el login:
message = {"accion": "NOT-LOGGED",
“client_id”: “String con el id del cliente registrado”,
"user": "String con el nombre de usuario",
"password": "String con la contraseña",
“causa”: “Usuario o contraseña incorrectos”
}
- Confirmación exitosa del pedido:
message = {"accion": "ORDERED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente registrado”
}
- Confirmación exitosa de la cancelación de un pedido:
message = {"accion": "CANCELLED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“client_id”: “String con el id del cliente registrado”
}
- Confirmación no exitosa de la cancelación de un pedido (el pedido está ya entregado o
en reparto):
message = {"accion": "NOT-CANCELLED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“client_id”: “String con el id del cliente registrado”,
“causa”: “El pedido no existe o ya está en reparto”
}
- Confirmación no exitosa de la cancelación de un pedido (el cliente no está registrado):
message = {"accion": "NOT-CANCELLED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“client_id”: “String con el id del cliente registrado”,
“causa”: “El cliente no está registrado”
}
- Confirmación exitosa de ver pedidos:
message = {"accion": "SEEN",
“client_id”: “String con el id del cliente registrado”,
“pedidos”: “String con todos los pedidos del cliente”
}
- Confirmación no exitosa de ver pedidos:
message = {"accion": "NOT-SEEN",
“client_id”: “String con el id del cliente registrado”,
“causa”: “El cliente no está registrado”
}
#### Mensajes desde el controlador a los robots
- Puesta a los robots en marcha:
message = {"accion": "MOVE",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente que ha hecho el pedido”,
“estado”: “String con el estado de EnumEstadosPedido del pedido”
}
#### Mensajes desde el controlador a los repartidores

- Puesta a los repartidores en marcha:
message = {"accion": "DELIVERY",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente que ha hecho el pedido”,
“estado”: “String con el estado de EnumEstadosPedido del pedido”
}
#### Mensajes desde el repartidor al controlador
- Confirmación del pedido entregado con éxito:
message = {"accion": "DELIVERED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente que ha hecho el pedido”,
}
●Confirmación de que el pedido no ha sido entregado con éxito:
message = {"accion": "NOT-DELIVERED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente que ha hecho el pedido”,
}
#### Mensajes desde el robot al controlador
- Confirmación del pedido movido con éxito:
message = {"accion": "MOVED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente que ha hecho el pedido”,
}
- Confirmación de que el pedido no ha sido movido con éxito:
message = {"accion": "NOT-MOVED",
“id_pedido”: “String con el identificador del pedido solicitado”,
“product_ids”: Array con los productos que contiene el pedido,
“client_id”: “String con el id del cliente que ha hecho el pedido”,
}

## 3.6 Desarrollo
Durante el desarrollo del proyecto, se optó en primera instancia por utilizar el sistema de colas de mensajes para enviar y recibir mensajes básicos. Posteriormente, se desarrolló en paralelo la gestión de las bases de datos, el controlador y una interfaz de línea de comandos para el cliente. A medida que se avanzaba en el proyecto, se logró implementar un sistema funcional de registro de usuarios, inicio de sesión y generación de órdenes de compra, sin embargo, estas órdenes no eran procesadas adecuadamente.

Con el objetivo de solucionar esta situación, se procedió a desarrollar una primera versión de los programas de robots y delivery para que las órdenes fueran procesadas correctamente y entregadas a los clientes. A medida que se avanzaba en el proyecto, se identificaron diferentes matices y problemas, como el control de errores del sistema, la cancelación de pedidos y la elaboración más profunda del sistema de cliente manual.

Finalmente, se resolvieron estas dificultades hasta lograr un sistema de comercio electrónico completamente funcional. Posteriormente, se implementó el "cliente automático": launch_client. Con esto, se dio por concluido el desarrollo del proyecto.


# 4. Conclusiones

  
  

## 4.1 Conclusiones técnicas

  
  

En primer lugar, se ha podido comprobar la utilidad y eficacia de la implementación de colas de mensajes en el desarrollo de aplicaciones distribuidas. El uso de este patrón de comunicación permitió separar la lógica de los diferentes componentes del sistema, lo que facilitó su desarrollo y su escalabilidad.

  

Por otra parte, se destaca la importancia de la implementación de un sistema de control de errores y excepciones en una aplicación compleja como esta. Gracias a la detección y manejo adecuado de estos errores, se logró reducir el impacto de posibles fallos en el sistema y mantener su estabilidad y

fiabilidad.

  

Otro punto a destacar es la implementación de la funcionalidad de cancelación de pedidos, el cual hizo que se tuviese que pensar el proyecto de forma holística, lo cual ayudó a entender mejor cómo funcionan los sistemas basados en microservicios.

  

## 4.2 Conclusiones personales

  
  

En primer lugar, es importante destacar el valor de trabajar en equipo y la importancia de una buena planificación y organización. A lo largo del desarrollo de Saimazoom, se encontraron diversos desafíos técnicos que se pudieron superar gracias al trabajo en equipo y al esfuerzo conjunto.

  

Por otro lado, el uso de herramientas y tecnologías actuales, como el sistema de colas de mensajes, permitió desarrollar un proyecto moderno y con un alto nivel de escalabilidad. Asimismo, la implementación de buenas prácticas de programación, como el uso de patrones de diseño y la gestión adecuada de las bases de datos, contribuyeron a la calidad del proyecto y facilitaron su mantenimiento.

  

Finalmente, el proyecto Saimazoom fue una experiencia enriquecedora que permitió poner en práctica los conocimientos adquiridos a lo largo del curso y desarrollar habilidades técnicas y de trabajo en equipo que serán útiles en el futuro.
> Written with [StackEdit](https://stackedit.io/).
