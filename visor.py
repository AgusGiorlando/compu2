#!/usr/bin/python3
import logging
import os
import socket
import pickle
import settings
from utils.loggerHelper import LoggerHelper
from utils.clockHelper import ClockHelper

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
logger_helper = LoggerHelper()
clock_helper = ClockHelper()

def main():
    while True:
        try:
            
            # Menu y generacion de la peticion
            peticion = menu()

            # Si viene false (salir) termina el bucle
            if not peticion:
                break

            # Conexion con el server
            desc = socket.socket(family=socket.AF_INET,
                                 type=socket.SOCK_STREAM)
            desc.connect(
                (os.getenv("SERVER_IP"), int(os.getenv("SERVER_PORT"))))

            # Formatea y envia la Peticion
            response = pickle.dumps(peticion)
            desc.send(response)
            leido = desc.recv(2048)

            # Termina la conexion
            desc.close()

            # Muestra la respuesta recibida
            oLeido = pickle.loads(leido)
            print(oLeido)
        except Exception as ex:
            logger_helper.sendLog('Visor','error', 'Error: ' + str(ex))
            try:
                input("Presiona enter para volver a intentar")
            except SyntaxError:
                pass
    # Termina la conexion
    print("Hasta luego")

def pedirOpcion():
    correcto = False
    num = 0
    while(not correcto):
        try:
            num = input("Elige una opcion: ")
            correcto = True
        except ValueError:
            print('Error, la opcion ingresada no es valida')
    return int(num)


def menu():
    salir = False
    opcion = 0
    while not salir:
        print("1. Ingreso")
        print("2. Egreso")
        print("3. Salir")
        opcion = pedirOpcion()
        if opcion == 1:
            return setPeticion(1)
        elif opcion == 2:
            return setPeticion(2)
        elif opcion == 3:
            salir = True
            return False
        else:
            print("Ingrese un numero entre 1 y 3")


def setPeticion(tipo):
    print("Ingrese su DNI: ")
    dni = input()
    print("Ingrese su clave: ")
    clave = input()

    try:
        time = clock_helper.getHora()
        return (0, dni, clave, tipo, time)
    except Exception  as ex:
        logger_helper.sendLog('Visor', 'Error', 'Clock - ' + str(ex))
        print('No se pudo conectar al clock')



if __name__ == "__main__":
    main()
