#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from models.movimiento import Movimiento
from empleadoController import EmpleadoController

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
movimiento = Movimiento()
empleadoController = EmpleadoController()


class MovimientoController:

    def agregarMovimiento(self, dni, clave, tipo, time):
        """
        Recibe dni, clave y tipo de movimiento
        Busca al empleado correspondiente al dni, valida que la clave sea correcta
        Setea fecha y hora del movimiento
        Inserta en DB el movimiento
        Devuelve un mensaje al lector sobre el estado de la operacion
        """
        try:
            # SELECT de Empleado
            resultado = empleadoController.buscarPorDni(dni)
            if type(resultado) == str:
                return resultado
            id_empleado = resultado[0]
            clave_empleado = resultado[4]

            # Verificacion de clave
            if str(clave_empleado) != str(clave):
                return 'La clave ingresada es incorrecta'

            # Fecha y Hora
            fecha = str(time[0]).zfill(2) + '/' + str(time[1]).zfill(2)
            hora = str(time[2]) + ':' + str(time[3])

            # INSERT movimiento
            if movimiento.insert(id_empleado, tipo, fecha, hora) != True:
                logging.info("Error al registrar el movimiento")
                return 'No se pudo registrar el movimiento'
            
            return 'Movimiento registrado correctamente'
        except Exception as ex:
            print(ex)

    def getMovimientos(self, ):
        """
        Devuelve todos los movimientos
        """
        try:
            # SELECT
            movimientos = movimiento.selectAll()
            return movimientos
        except Exception as ex:
            print(ex)

    def getMovimientosByFechaAndEmpleado(self, fecha, id_empleado):
        """
        Devuelve los movimientos de una fecha determinada
        """
        try:
            movimientos = movimiento.selectByFechaAndEmpleado(
                fecha, id_empleado)
            return movimientos
        except Exception as ex:
            print(ex)
