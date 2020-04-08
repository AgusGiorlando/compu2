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

        #TODO: eliminar
        print(peticion)

        # Formatea y envia la Peticion
        response = pickle.dumps(peticion)
        desc.send(response)

        # Muestra la respuesta recibida
        leido = desc.recv(2048)
        print(leido)

        # Termina la conexion
        desc.close()
    print("Hasta luego")
    logging.info('Fin del lector')


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

    # Solicitud al clock de horario
    clockConnection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    clockConnection.connect((SERVER_IP, CLOCK_PORT))
    clockConnection.send(str(1))
    response = clockConnection.recv(2048)
    time = pickle.loads(response)
    clockConnection.close()

    return (dni, clave, tipo, time)


if __name__ == "__main__":
    main()
