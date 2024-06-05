# practica2 - Redes II
**Authors**: Sergio Larriba Moreno, Javier Valero Velázquez 
## Set Up
1 - Tener RabbitMQ instalado
2 - Instalar los paquetes del fichero ``requirements.txt`` con el siguiente comando: 
<pre><code>pip install -r requirements.txt</code></pre>
Son librerias para la impresion de los resultados y mensajes en la terminal de forma agradable
## Ejecución
La práctica consta de 4 ficheros launch ejecutables en la carpeta ``src/`` y un fichero ``commandline_client.py`` que simula la interfaz de un cliente a través de linea de comandos. 
NOTA: Antes de ejecutar cualquiera de los 2 scripts del cliente (``launch_client.py`` y ``commandline_client.py``) es necesario ejecutar los actores del sistema, que son: el controlador, los robots y los repartidores. 

Pasos para su ejecución: 
<pre><code>cd src/</code></pre>
Los siguientes comandos se deben ejecutar en diferentes pestañas / ventanas de terminal
<pre><code>python3 launch_controller.py</code></pre>
<pre><code>python3 launch_robot.py</code></pre>
<pre><code>python3 launch_delivery.py</code></pre>
<pre><code>python3 launch_client.py</code></pre>
Una vez ejecutemos el cliente, podemos apreciar que se muestran diferentes mensajes en formato de tabla en cada una de las terminales que van indicando qué es lo que va haciendo cada actor, tanto los mensajes que envía como los que recibe. 
### Script global
El archivo ``src/launch_system.sh`` lanza todo el sistema concretamente: 1 controlador, 2 robots, 2 repartidores y 2 clientes. Cada uno de estos actores los lanza en una nueva terminal. 
Para ejecutarlo se debe hacer lo siguiente: 
<pre><code>cd src/</code></pre>
<pre><code>./launch_system.sh</code></pre>
## Launch Client
Simula el comportamiento por defecto de un cliente: 
1 - Prueba a registrar un cliente existente -> El controlador le devuelve ``NOT-REGISTERED`` porque ese cliente ya existe 
2 - Se loguea un cliente existente y procede a hacer un pedido con 3 productos 
3 - Despues ve el pedido solicitado y todos los que ha realizado
NOTA: Cancelar un pedido sólo es posible desde el archivo ``commandline_client.py``
## Commandline Client
Simula la interfaz de un cliente a través de la línea de comandos. Se ejecuta de la siguiente forma: 
<pre><code>cd src/</code></pre>
<pre><code>python3 commandline_client.py</code></pre>
Al comienzo nos da 2 opciones: 
<pre>
Seleccione una opcion: 
1. Registrarse
2. Log-In
</pre>
#### Opcion 1 - Registrarse. 
Necesitamos introducir un nombre de usuario y una contraseña. Quizás el nombre de usuario introducido no sirva debido a que ya existe otro usuario registrado con ese nombre, solo hay que probar con otro. 
<pre>
Introduzca el usuario: Javier
Introduzca la contraseña: Javier
 
[Cliente] Mensaje enviado al controlador: 
+----------+----------+
|   Key    |  Value   |
+----------+----------+
|  accion  | REGISTER |
|   user   |  Javier  |
| password |  Javier  |
+----------+----------+
 [Cliente] Mensaje recibido por el controlador: 
+-----------+--------------------------------------+
|    Key    |                Value                 |
+-----------+--------------------------------------+
|  accion   |              REGISTERED              |
| client_id | dc98962b-7ff3-4de3-968b-e4683785a7b1 |
|   user    |                Javier                |
| password  |                Javier                |
+-----------+--------------------------------------+
</pre>
#### Opcion 2 - Loguearse. 
Nos podemos loguear con el usuario registrado de ahora o con otro existente, como por ejemplo el usuario: Sergio, password: sergio
<pre>
Introduzca el usuario: Sergio
Introduzca la contraseña: sergio
 
[Cliente] Mensaje enviado al controlador: 
+----------+--------+
|   Key    | Value  |
+----------+--------+
|  accion  | LOGIN  |
|   user   | Sergio |
| password | sergio |
+----------+--------+
 [Cliente] Mensaje recibido por el controlador: 
+-----------+--------------------------------------+
|    Key    |                Value                 |
+-----------+--------------------------------------+
|  accion   |                LOGGED                |
| client_id | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |
|   user    |                Sergio                |
| password  |                sergio                |
+-----------+--------------------------------------+
</pre>
Si todo ha ido bien, nos aparecerá el siguiente menú: 
<pre>
¿Qué desea hacer?
1. Hacer pedido
2. Ver pedidos
3. Cancelar pedido
4. Salir
Opción: 
</pre>
En él, tenemos que seleccionar una opción (1, 2, 3 o 4). 
#### Opción 1 - Hacer pedido: 
<pre>
Opción: 1
Introduzca los productos (P1 P2 ...): 
</pre>
Introducimos los productos separados por un espacio, ejemplo: 
<pre>
Opción: 1
Introduzca los productos (P1 P2 ...): Macarrones Pizza Agua Hamburguesa
 
[Cliente] Mensaje enviado al controlador: 
+-------------+---------------------------------------+
|     Key     |                 Value                 |
+-------------+---------------------------------------+
|   accion    |                 ORDER                 |
| product_ids | ['Macarrones Pizza Agua Hamburguesa'] |
|    user     |                Sergio                 |
+-------------+---------------------------------------+
 [Cliente] Mensaje recibido por el controlador: 
+-------------+---------------------------------------+
|     Key     |                 Value                 |
+-------------+---------------------------------------+
|   accion    |                ORDERED                |
|  id_pedido  | f0c4be2b-b509-42da-809e-5cd9d0126dbd  |
| product_ids | ['Macarrones Pizza Agua Hamburguesa'] |
|  client_id  | 2f7dc411-0845-4abd-9335-f51198a3d4c4  |
+-------------+---------------------------------------+
¿Qué desea hacer?
1. Hacer pedido
2. Ver pedidos
3. Cancelar pedido
4. Salir
Opción: 
</pre>
Y como podemos ver, ya se ha mandado nuestro pedido al controlador y se está procesando. Para ver qué tal va seleccionamos la opción 2. Esta opción nos dará la información de todos los pedidos realizados por el cliente actual y del pedido nada mas realizado. 
#### Opción 2 - Ver Pedido
<pre>
[Cliente] Mensaje enviado al controlador: 
+--------+--------+
|  Key   | Value  |
+--------+--------+
| accion |  SEE   |
|  user  | Sergio |
+--------+--------+
 [Cliente] Mensaje recibido por el controlador: 
+--------------------------------------+--------------------------------------+-----------------------------------+----------------+
|              ID Pedido               |              ID Cliente              |             Productos             |     Estado     |
+--------------------------------------+--------------------------------------+-----------------------------------+----------------+
| 7b6a003c-feee-4b37-a68a-6f6d0e02236c | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |             Macarrones            |       1        |
| f916cdc4-7890-47b6-b893-ca664b85c735 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |               Pollo               |       1        |
| 19079173-038d-4ca9-9698-8478ac066be5 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |     Espinacas Pollo Macarrones    |       5        |
| 2d2a037d-3106-4729-bf96-eb9224ae5af9 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |               Carne               |       1        |
| 2965583d-8a19-4889-a1b5-71e6dc395c3f | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |             Pato asado            |       1        |
| 3082f2fb-0483-4d10-94f9-43f436e8d82e | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |             Macarrones            |       2        |
| a28d0628-e4a2-4df3-9044-8ad2e117dace | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |      Macarrones Pollo Patatas     |       1        |
| d87c6738-4d54-4dcc-b306-9266986abb90 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |             Producto1             |       1        |
| 9a726575-ce00-483f-ac72-fab4e8300a69 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P2                |       5        |
| 4d820f85-0ab1-4d10-8d7b-6f010c0be2a1 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P1                |       1        |
| d2492366-bc9c-46a7-9ba7-577288f9f52e | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |           Pedido prueba           |       1        |
| 9654b270-e245-4fe6-a7b6-76d9f6467f79 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                pato               |       1        |
| e3c41d64-6f8c-49ef-a030-fddcc149137d | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P1                |       5        |
| b0f1a242-e5b8-4841-8bbd-d41e80f07d67 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P2                |       1        |
| 3f12d354-ed0c-4e78-981b-965b73fbed1c | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P3                |       5        |
| 39682340-1bad-44b6-b342-9eec8730a3aa | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                P12                |       5        |
| ce4173a3-24ea-4b53-a7a3-86735a9b3143 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |            P1 P2 P3 P4            |       5        |
| 57808f5b-419c-4c0a-aa6f-dc24764bff02 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |            P1 P2 P3 P4            |       1        |
| 0f05f757-0d83-4e59-a30f-8a8ef23f29ba | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |       Pollo Espinacas Filete      |       1        |
| d35423cc-6539-4380-8ec0-8ed0aefb509c | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P1                |       1        |
| 7892c4a3-e9c4-4da4-bbf1-c38f8916780a | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 P1                |       1        |
| ec1a1ec4-018c-43aa-abdb-5a90eca7cd0a | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |                 p2                |   EN_ALMACEN   |
| 2a74ab8e-c445-453a-b580-cadedaad1869 | 2f7dc411-0845-4abd-9335-f51198a3d4c4 |               eoeoeo              | EN_PREPARACION |
| f0c4be2b-b509-42da-809e-5cd9d0126dbd | 2f7dc411-0845-4abd-9335-f51198a3d4c4 | Macarrones Pizza Agua Hamburguesa |   ENTREGADO    |
+--------------------------------------+--------------------------------------+-----------------------------------+----------------+
 
[Cliente] Send: {"accion": "SEE", "user": "Sergio"}
¿Qué desea hacer?
1. Hacer pedido
2. Ver pedidos
3. Cancelar pedido
4. Salir
Opción: 
</pre>
Podemos cancelar el pedido seleccionando la opción 3.
#### Opción 3 - Cancelar Pedido
Siempre y cuando no esté en reparto, el pedido se puede cancelar. Para ello seleccionamos la opción 3, introducimos el id del pedido a cancelar y el controlador nos devolverá una respuesta exitosa (CANCELED) si se ha cancelado o NOT-CANCELLED si no se ha podido cancelar por alguna de las razones anteriores. 
<pre>
Opción: 3
Introduzca el ID del pedido a cancelar: 
</pre>
#### Opción 4 - Salir
Equivale a hacer Ctrl+C. Con ello el programa commandline_client.py acaba su ejecución. 
## Tests Unitarios
Hemos implementado en la carpeta ``src/tests/classes_tests/`` tests unitarios para cada una de las clases de la carpeta ``src/clases/``. 
Para ejecutar todos los tests es necesario estar en el directorio ``tests/`` y ejecutar el siguiente comando: 
<pre><code>python3 all_tests.py</code></pre>
Su resultado es el siguiente: 
<pre>
sergio@sergio-AORUS-5-KE:~/Documentos/3_Curso/2o_Cuatri/Redes_2/Practicas/practica2/src/tests$ python3 all_tests.py

..........................
----------------------------------------------------------------------
Ran 26 tests in 0.012s

OK
sergio@sergio-AORUS-5-KE:~/Documentos/3_Curso/2o_Cuatri/Redes_2/Practicas/practica2/src/tests$ 
</pre>

