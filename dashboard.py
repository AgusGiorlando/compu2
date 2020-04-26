#!/usr/bin/python3
import logging
import os
import socket
import pickle

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
SERVER_IP = 'localhost'
SERVER_PORT = 5000
CLOCK_PORT = 5001
LOGGER_PORT = 5003


def sendLog(nivel, accion):
    # Generacion del mensaje
    msg = (os.getppid(), 'Dashboard', nivel, accion)
    msg = pickle.dumps(msg)

    # Envio
    loggerConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    loggerConnection.connect((SERVER_IP, LOGGER_PORT))
    loggerConnection.send(msg)
    loggerConnection.close()


def main():
    logging.info('process id: %s', str(os.getpid()))
    while True:
        # Conexion con el server
        desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        desc.connect((SERVER_IP, SERVER_PORT))

        # Menu y generacion de la peticion
        peticion = menu()

        # Si viene false (salir) termina el bucle
        if not peticion:
            # Termina la conexion
            desc.close()
            break

        # Formatea y envia la Peticion
        response = pickle.dumps(peticion)
        desc.send(response)
        sendLog('info', 'Envio de peticion')

        # Muestra la respuesta recibida
        leido = desc.recv(2048)
        sendLog('info', 'Respuesta recibida')
        oLeido = pickle.loads(leido)
        print(oLeido)
        
        # Termina la conexion
        desc.close()
    print("Hasta luego")
    logging.info('Fin del dashboard')


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
        print("1. Ver empleados")
        print("2. Ver movimientos")
        print("3. Salir")
        opcion = pedirOpcion()
        if opcion == 1:
            return (1, "getEmpleados")
        elif opcion == 2:
            return (1, "getMovimientos")
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


    # Solicitud al clock de horario
    clockConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    clockConnection.connect((SERVER_IP, CLOCK_PORT))
    clockConnection.send(str(1))
    response = clockConnection.recv(2048)
    time = pickle.loads(response)
    clockConnection.close()
    return (dni, clave, tipo, time)


if __name__ == "__main__":
    main()
