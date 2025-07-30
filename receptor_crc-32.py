import zlib
import socket

# CAPA 5: TRANSMISIÓN
def recibir_trama(host='localhost', puerto=5000):
    print("--- CAPA DE TRANSMISIÓN ---")
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((host, puerto))
    servidor.listen(1)
    print(f"Escuchando en {host}:{puerto}...")
    cliente, direccion = servidor.accept()
    print(f"Conexión establecida desde {direccion}")
    datos = b''
    while True:
        parte = cliente.recv(4096)
        if not parte:
            break
        datos += parte
    cliente.close()
    print("Trama recibida.")
    try:
        trama = datos.decode()
    except UnicodeDecodeError:
        print("Error: No se pudo decodificar la trama recibida.")
        return None
    return trama

# CAPA 3: ENLACE
def verificar_integridad(trama_recibida):
    print("\n--- CAPA DE ENLACE ---")
    if trama_recibida is None:
        return None, None, True
    if len(trama_recibida) < 32:
        print("Error: La trama recibida es demasiado corta para contener CRC.")
        return None, None, True
    mensaje_binario = trama_recibida[:-32]
    crc_recibido = trama_recibida[-32:]
    # Reconstruir texto para cálculo de CRC
    mensaje_texto = ""
    for i in range(0, len(mensaje_binario), 8):
        byte = mensaje_binario[i:i+8]
        mensaje_texto += chr(int(byte, 2))
    valor_crc_calc = zlib.crc32(mensaje_texto.encode())
    crc_calc_bin = format(valor_crc_calc & 0xFFFFFFFF, '032b')
    print(f"CRC recibido: {crc_recibido}")
    print(f"CRC calculado: {crc_calc_bin}")
    error = crc_calc_bin != crc_recibido
    if error:
        print("Error detectado en la transmisión (CRC diferente).")
    else:
        print("No se detectaron errores (CRC coincide).")
    return mensaje_binario, mensaje_texto, error

# CAPA 2: PRESENTACIÓN y CAPA 1: APLICACIÓN
def procesar_mensaje(mensaje_binario, mensaje_texto, error):
    print("\n--- CAPA DE PRESENTACIÓN ---")
    if error:
        print("No es posible decodificar el mensaje debido a errores detectados.")
        return
    # Decodificar binario a mensaje
    mensaje_decodificado = ""
    for i in range(0, len(mensaje_binario), 8):
        byte = mensaje_binario[i:i+8]
        mensaje_decodificado += chr(int(byte, 2))
    print("--- CAPA DE APLICACIÓN ---")
    print("Mensaje recibido correctamente:")
    print(mensaje_decodificado)

if __name__ == "__main__":
    print("--- RECEPTOR INICIADO ---")
    trama = recibir_trama()
    mensaje_binario, mensaje_texto, error = verificar_integridad(trama)
    procesar_mensaje(mensaje_binario, mensaje_texto, error)
