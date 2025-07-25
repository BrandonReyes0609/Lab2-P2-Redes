import zlib
import random
import socket

# CAPA 1: APLICACIÓN
def solicitar_mensaje():
    print("--- CAPA DE APLICACIÓN ---")
    mensaje = input("Ingrese el mensaje a enviar: ")
    print("Ingrese la probabilidad de error en porcentaje (por ejemplo: 10, 50, 90):")
    porcentaje_error = input("Probabilidad de error (%): ")
    try:
        porcentaje_error = float(porcentaje_error)
        probabilidad_error = porcentaje_error / 100
    except ValueError:
        print("Entrada inválida. Se usará 0% de error por defecto.")
        probabilidad_error = 0.0
    return mensaje, probabilidad_error

# CAPA 2: PRESENTACIÓN
def codificar_ascii_binario(mensaje_original):
    print("\n--- CAPA DE PRESENTACIÓN ---")
    mensaje_binario = ""
    for caracter in mensaje_original:
        ascii_bin = format(ord(caracter), '08b')
        mensaje_binario += ascii_bin
    print("Mensaje codificado en binario: " + str(mensaje_binario))
    return mensaje_binario

# CAPA 3: ENLACE
def calcular_crc32(mensaje_binario):
    print("\n--- CAPA DE ENLACE ---")
    mensaje_texto = ""
    for i in range(0, len(mensaje_binario), 8):
        grupo = mensaje_binario[i:i+8]
        caracter = chr(int(grupo, 2))
        mensaje_texto += caracter
    valor_crc = zlib.crc32(mensaje_texto.encode())
    crc_binario = format(valor_crc, '032b')
    print("CRC-32 calculado: " + str(crc_binario))
    return crc_binario

def construir_trama_completa(mensaje_binario, crc_binario):
    trama = mensaje_binario + crc_binario
    print("Trama con bits de control añadidos: " + str(trama))
    return trama

# CAPA 4: RUIDO
def aplicar_ruido(trama_original, probabilidad_error):
    print("\n--- CAPA DE RUIDO ---")
    trama_modificada = ""
    for bit in trama_original:
        numero_aleatorio = random.random()
        if numero_aleatorio < probabilidad_error:
            if bit == '0':
                trama_modificada += '1'
            else:
                trama_modificada += '0'
        else:
            trama_modificada += bit
    print("Trama después de aplicar ruido: " + str(trama_modificada))
    return trama_modificada

# CAPA 5: TRANSMISIÓN
def enviar_trama(trama_final, host='localhost', puerto=5000):
    print("\n--- CAPA DE TRANSMISIÓN ---")
    print("Conectando con el receptor...")
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((host, puerto))
        cliente.sendall(trama_final.encode())
        cliente.close()
        print("OK Trama enviada con éxito.")
    except Exception as error:
        print("NO Error al enviar la trama: " + str(error))

# EJECUCIÓN DIRECTA DEL PROGRAMA (SIN if __name__)
print("--- EMISOR INICIADO ---")

mensaje, tasa_error = solicitar_mensaje()
binario = codificar_ascii_binario(mensaje)
crc = calcular_crc32(binario)
trama_sin_ruido = construir_trama_completa(binario, crc)
trama_con_ruido = aplicar_ruido(trama_sin_ruido, tasa_error)

print("\n--- RESUMEN ---")
print("Mensaje original: " + mensaje)
print("Trama lista para enviar: " + trama_con_ruido)

enviar_trama(trama_con_ruido)
