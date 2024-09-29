import socket
import threading

# Configuración del servidor
host = '127.0.0.1'  # Localhost
port = 12345        # Puerto que escucha el servidor

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociar el socket a la dirección y puerto
server_socket.bind((host, port))

# Escuchar conexiones entrantes
server_socket.listen(5)
print(f"Servidor escuchando en {host}:{port}...")

# Lista de clientes conectados
clientes = []

# Variable para saber si el server sigue activo
servidor_activo = True

# Función para manejar a cada cliente
def manejar_cliente(cliente_socket, cliente_address):
    print(f"Conectado por: {cliente_address}")
    while True:
        try:
            # Recibir el mensaje del cliente
            mensaje = cliente_socket.recv(1024).decode()
            if not mensaje:
                break
            
            print(f"{cliente_address} dice: {mensaje}")
            # Retransmitir el mensaje a todos los demás clientes
            retransmitir_mensaje(mensaje, cliente_socket)
        
        except:
            break

    # Eliminar al cliente de la lista y cerrar la conexión
    if cliente_socket in clientes:
        clientes.remove(cliente_socket)    
    cliente_socket.close()
    print(f"Desconectado: {cliente_address}")

# Función para retransmitir el mensaje a todos los clientes conectados excepto el que envió
def retransmitir_mensaje(mensaje, emisor_socket=None):
    for cliente in clientes:
        if cliente != emisor_socket:
            try:
                cliente.send(mensaje.encode())
            except:
                cliente.close()
                clientes.remove(cliente)
    
# Función para que el servidor envíe mensajes a los clientes
def enviar_mensajes_servidor():
    global servidor_activo
    while servidor_activo:
        mensaje = input("Escribe un mensaje para los clientes ó escribe (apagar) para cerrar el servidor: ")
        if mensaje.lower() == 'apagar':
            servidor_activo = False
            apagar_servidor()
            break
        retransmitir_mensaje(f'Servidor: {mensaje}')

# Función para cerrar el servidor y desconectar a todos los clientes
def apagar_servidor():
    print("Apagando el servidor... uwu")
    # Enviar mensaje a los clientes para hacerles saber que el server se apaga
    retransmitir_mensaje("El servidor se está apagando y serán desconcetados. ", None)

    # Cerrar las conexiones de todos los clientes
    for cliente in clientes:
        try:
            cliente.close()
        except:
            pass
    
    # Cerrar el socket del servidor
    server_socket.close()
    print("Servidor Apagado.")

# Bucle principal del servidor
def aceptar_conexiones():
    while servidor_activo:
        try:
            cliente_socket, cliente_address = server_socket.accept()
            clientes.append(cliente_socket)

            # Crear un nuevo hilo para manejat a un cliente
            cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente_socket, cliente_address))
            cliente_thread.start()
        except:
            break

# Crear un hilo para aceptar conexiones de clientes
hilo_aceptar = threading.Thread(target=aceptar_conexiones)
hilo_aceptar.start()

# Iniciar el hilo para que el servidor envie mensajes
enviar_mensajes_servidor()