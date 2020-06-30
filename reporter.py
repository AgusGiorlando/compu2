#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import socket
import threading
import pickle
import multiprocessing
import settings
from utils.loggerHelper import LoggerHelper

from controllers.movimientoController import MovimientoController
from controllers.empleadoController import EmpleadoController

# Declaracion de variables
movimiento_controller = MovimientoController()
empleado_controller = EmpleadoController()
logger_helper = LoggerHelper()

def createReport(mes, dia):
    logger_helper.sendLog('Reporter', 'info', 'Iniciando reporter')
    # Seteo del archivo de reporte
    fecha = str(dia).zfill(2)+ '/' + str(mes).zfill(2)
    file_name = str(dia).zfill(2)+ '-' + str(mes).zfill(2)
    file_path = 'reports/' + file_name + '.txt'
    try:
        file = open(file_path, 'a')
        file.write('\tREPORTE DEL DIA ' + fecha + '\n\n')
        file.write('EMPLEADO\t\t\t\tHORAS TRABAJADAS\n')
    except Exception  as err:
        logger_helper.sendLog('Reporter', 'error', 'Generacion de reporte - ' + str(err))
    
    # Busca todos los empleados
    empleados = empleado_controller.getEmpleados()
    for empleado in empleados:
        # Busca los movimientos de cada empleado en la fecha
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
            # Registro completo
            registro = empleado[3] + ', ' + empleado[2] + '\t\t' + str(total_horas).zfill(2) + ':' + str(total_minutos).zfill(2) + '\n'
        try:
            # Escritura
            file.write(registro)
        except Exception as err:
            logger_helper.sendLog('Reporter', 'error', 'Escritura de registro - ' + str(err))
    file.close()
    logger_helper.sendLog('reporter','info', 'Reporte Completo')

if __name__ == "__main__":
    createReport(str(1).zfill(2), str(1).zfill(2))