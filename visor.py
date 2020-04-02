#!/usr/bin/python3
import logging
import os
import socket
import json

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
SERVER_IP = 'localhost'
VISOR_PORT = 5000


def main():
    logging.info('process id: %s', str(os.getpid()))
    while True:
        # Conexion con el server
        desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        desc.connect((SERVER_IP, VISOR_PORT))

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
        json_peticion = json.dumps(peticion)
        desc.send(json_peticion+"\n")

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

    return (dni, clave, tipo)


if __name__ == "__main__":
    main()
