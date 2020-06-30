#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
import pickle
import multiprocessing
import os
from utils.loggerHelper import LoggerHelper
from utils.clockHelper import ClockHelper
from logger import Logger
from controllers.movimientoController import MovimientoController
from controllers.empleadoController import EmpleadoController
import settings
import argparse

# Declaracion de variables
movimiento_controller = MovimientoController()
empleado_controller = EmpleadoController()
logger_helper = LoggerHelper()
clock_helper = ClockHelper()
terminate = False
port = int(os.getenv('CLOCK_PORT'))


def processPeticion(oLeido, newdesc):
    """
    Recibe una peticion
    Identifica a que controller debe llamar y devuelve una respuesta
    """
    try:
        # Peticion de un Lector
        if oLeido[0] == 0:
            # Llamada al controller
            response = movimiento_controller.agregarMovimiento(
                oLeido[1], oLeido[2], oLeido[3], oLeido[4])
        # Peticion de un Dashboard
        elif oLeido[0] == 1:
            if oLeido[1] == "getEmpleados":
                response = empleado_controller.getEmpleados()
            elif oLeido[1] == "getMovimientos":
                response = movimiento_controller.getMovimientos()
            elif oLeido[1] == "addEmpleado":
                response = empleado_controller.createEmpleado(
                    oLeido[2], oLeido[3], oLeido[4], oLeido[5])
            elif oLeido[1] == "deleteEmpleado":
                response = empleado_controller.deleteEmpleadoByDni(
                    oLeido[2])
            else:
                print('No se reconoce la operacion solicitada')
                print(oLeido)
        # Envio de respuesta
        oResponse = pickle.dumps(response)
        newdesc.send(oResponse)
    except Exception as ex:
        print(ex)


def service():
    global terminate
    # Nuevo Socket
    try:
        desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        desc.settimeout(3.0)
        # para que no diga address already in use ...
        desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as err:
        logger_helper.sendLog(
            'server', 'error', 'Error al crear socket: ' + str(err))
        print('Error al crear socket: ' + str(err))
        try:
            input("Presiona enter para volver a intentar\n")
        except SyntaxError:
            return

    desc.bind((os.getenv("SERVER_IP"), int(os.getenv("SERVER_PORT"))))
    desc.listen(100)

    # Espera infinita de nuevos lectores
    while True:
        try:
            newdesc, cli = desc.accept()
            try:
                leido = newdesc.recv(2048)
            except socket.error as e:
                logger_helper.sendLog(
                    'server', 'error', 'Error al recibir: ' + str(e))
                pass
            oLeido = pickle.loads(leido)
            # Nuevo hilo
            threading.Thread(
                target=processPeticion, args=(oLeido, newdesc)).start()

        except EOFError:
            pass
        except socket.timeout:
            if terminate:
                break


def client():
    while True:
        try:
            # Menu y generacion de la peticion
            peticion = menu()

            # Si viene false (salir) termina el bucle
            if not peticion:
                break

        except Exception as ex:
            print(ex)
            try:
                input("Presiona enter para volver a intentar")
            except SyntaxError:
                pass


def pedirOpcion():
    correcto = False
    num = 0
    while(not correcto):
        try:
            num = input("Elige una opcion: \n")
            correcto = True
        except ValueError:
            print('Error, la opcion ingresada no es valida')
    return int(num)


def menu():
    salir = False
    opcion = 0
    while not salir:
        print("1. Consultar Hora")
        print("0. Salir")
        opcion = pedirOpcion()
        if opcion == 1:
            getHora()
            return True
        elif opcion == 0:
            salir = True
            return False
        else:
            print("Ingrese un numero\n")


def getHora():
    global args, port
    try:
        time = clock_helper.getHora(port)
        print(str(time[0]) + '/' + str(time[1]) +
              ' - ' + str(time[2]) + ':' + str(time[3]))
    except Exception as ex:
        logger_helper.sendLog('Server', 'Error', 'Clock - ' + str(ex))


def main():
    global port
    print(os.getpid())
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-cp', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator', default=0)
    args = parser.parse_args()
    
    #print(type(args.cp))
    if args.cp != 0:
        port = args.cp[0]


    global terminate
    print('Iniciando servidor...')
    # Inicio del logger
    logger = Logger()
    loggerProcess = multiprocessing.Process(target=logger.connect, args=())
    loggerProcess.start()

    try:
        # Inicializa los hilos
        serviceThread = threading.Thread(name='service', target=service)
        clientThread = threading.Thread(name='client', target=client)

        serviceThread.start()
        clientThread.start()
        clientThread.join()

        # Terminacion de hilos
        print('Cliente terminado')

        # Modifica el flag y espera a que termine el servicio
        terminate = True
        serviceThread.join()
        print('Servicio terminado')

        # Manda señal al logger para que se termine y espera
        logger_helper.sendLog('server', 'info', 'terminate')
        loggerProcess.join()
        print('Logger terminado')

        print('Hasta luego')
    except Exception as ex:
        print(str(ex))


if __name__ == "__main__":
    main()
