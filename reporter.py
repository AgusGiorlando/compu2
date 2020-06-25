#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import socket
import threading
import pickle
import multiprocessing
import settings

from movimientoController import MovimientoController
from empleadoController import EmpleadoController

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
movimiento_controller = MovimientoController()
empleado_controller = EmpleadoController()

def sendLog(nivel, accion):
    # Generacion del mensaje
    msg = (os.getppid(), 'Reporter', nivel, accion)
    msg = pickle.dumps(msg)

    # Envio
    loggerConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    loggerConnection.connect((os.getenv("SERVER_IP"), int(os.getenv("LOGGER_PORT"))))
    loggerConnection.send(msg)
    loggerConnection.close()

def createReport(mes, dia):
    sendLog('info', 'Iniciando reporter')
    fecha = str(dia).zfill(2)+ '/' + str(mes).zfill(2)
    file_name = str(dia).zfill(2)+ '-' + str(mes).zfill(2)
    file_path = 'reports/' + file_name + '.txt'
    file = open(file_path, 'a')
    file.write('\tREPORTE DEL DIA ' + fecha + '\n\n')
    file.write('EMPLEADO\t\t\t\tHORAS TRABAJADAS\n')
    empleados = empleado_controller.getEmpleados()
    for empleado in empleados:
        movimientos = movimiento_controller.getMovimientosByFechaAndEmpleado(fecha, empleado[0])
        if len(movimientos) < 1:
            registro = empleado[3] + ', ' + empleado[2] + '\t\t\t\tAUSENTE\n'
        else:
            for i in range(len(movimientos)):    
                if movimientos[i][2] == '1':
                    entrada = movimientos[i][4].split(':')
                    salida = movimientos[i+1][4].split(':')
                    total_horas = int(salida[0]) - int(entrada[0])
                    total_minutos = int(salida[1]) - int(entrada[1])
                    if total_minutos < 0:
                        total_minutos += 60
                        total_horas -= 1
            registro = empleado[3] + ', ' + empleado[2] + '\t\t' + str(total_horas).zfill(2) + ':' + str(total_minutos).zfill(2) + '\n'
        file.write(registro)
    file.close()
    sendLog('info', 'Reporte Completo')

if __name__ == "__main__":
    createReport(str(1).zfill(2), str(1).zfill(2))