import socket
import threading

# Configuración del cliente
host = '127.0.0.1'  # Localhost
port = 12345        # El puerto debe coincidir con el del servidor

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect((host, port))

# Función para recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            # Recibir mensaje del servidor
            mensaje = client_socket.recv(1024).decode()
            if not mensaje:
                break
            print(f"\nMensaje recibido: {mensaje}")
        except:
            print("Error al recibir mensajes")
            break

# Crear un hilo para escuchar los mensajes del servidor
hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

# Bucle para enviar mensajes al servidor
while True:
    mensaje = input("Escribe un mensaje: ")
    if mensaje.lower() == "salir":
        client_socket.close()
        break
    client_socket.sendall(mensaje.encode())