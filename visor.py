#!/usr/bin/python3
import logging
import os
import socket
import pickle
import settings

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

def sendLog(nivel, accion):
    # Generacion del mensaje
    msg = (os.getppid(), 'Visor', nivel, accion)
    msg = pickle.dumps(msg)

    # Envio
    loggerConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    loggerConnection.connect((os.getenv("SERVER_IP"), int(os.getenv("LOGGER_PORT"))))
    loggerConnection.send(msg)
    loggerConnection.close()


def main():
    logging.info('process id: %s', str(os.getpid()))
    while True:
        try:
            # Conexion con el server
            desc = socket.socket(family=socket.AF_INET,
                                 type=socket.SOCK_STREAM)
            desc.connect((os.getenv("SERVER_IP"), int(os.getenv("SERVER_PORT"))))

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
            oLeido = pickle.loads(leido)
            print(oLeido)
            sendLog('info', 'Respuesta recibida')
            # Termina la conexion
            desc.close()
        except Exception as ex:
            print(ex)
            try:
                input("Presiona enter para volver a intentar")
            except SyntaxError:
                pass
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
    try:
        clockConnection = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        clockConnection.connect((os.getenv("SERVER_IP"), int(os.getenv("CLOCK_PORT"))))
        clockConnection.send(str(1))
        response = clockConnection.recv(2048)
        time = pickle.loads(response)
        clockConnection.close()
        return (0, dni, clave, tipo, time)
    except Exception  as ex:
        print(ex)


if __name__ == "__main__":
    main()
