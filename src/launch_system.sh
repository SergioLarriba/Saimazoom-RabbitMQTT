#!/bin/bash 

# Funcion para matar a los procesos en caso de error 
function kill_all_processes() {
    echo "Matando todos los procesos..."

    pkill -f "python3 launch_controller.py"
    pkill -f "python3 launch_robot.py"
    pkill -f "python3 launch_delivery.py"
    pkill -f "python3 launch_client.py"
    exit 1 
}

# Añadir controlador de interrupción
trap kill_all_processes SIGINT

# Ejecuta un controlador (launch_controller.py) en una nueva terminal 
gnome-terminal --title="Controller" -- python3 launch_controller.py

# Espera un segundo antes de continuar con el siguiente archivo
sleep 1

# Ejecuta dos robots (launch_robot.py) en una nueva terminal
gnome-terminal --title="Robot1" -- python3 launch_robot.py

# Espera un segundo antes de continuar con el siguiente archivo
sleep 1

gnome-terminal --title="Robot2" -- python3 launch_robot.py

# Ejecuta dos deliverys (launch_delivery.py) en una nueva terminal
gnome-terminal --title="Delivery1" -- python3 launch_delivery.py

# Espera un segundo antes de continuar con el siguiente archivo
sleep 1

gnome-terminal --title="Delivery2" -- python3 launch_delivery.py

sleep 1

# Ejecuta launch_client.py en una nueva terminal
gnome-terminal --title="Cliente1" -- python3 launch_client.py

sleep 1 

# Ejecuta launch_client.py en una nueva terminal
gnome-terminal --title="Cliente2" -- python3 launch_client.py

# Todos los archivos han sido lanzados
echo "Todos los archivos han sido lanzados."