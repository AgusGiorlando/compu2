#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from movimiento import Movimiento
from empleadoController import EmpleadoController


# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
movimiento = Movimiento()
empleadoController = EmpleadoController()


class MovimientoController:

    """
    Recibe dni, clave y tipo de movimiento
    Busca al empleado correspondiente al dni, valida que la clave sea correcta
    Setea fecha y hora del movimiento
    Inserta en DB el movimiento
    Devuelve un mensaje al lector sobre el estado de la operacion
    """

    def agregarMovimiento(self, dni, clave, tipo):
        # SELECT de Empleado
        resultado = empleadoController.buscarPorDni(dni)
        if type(resultado) == str:
            return resultado
        id_empleado = resultado[0]
        clave_empleado = resultado[4]

        # Verificacion de clave
        if str(clave_empleado) != str(clave):
            return 'La clave ingresada es incorrecta'

        # GET de Fecha y Hora
        # TODO: Pasar a lector
        now = datetime.now()
        fecha = now.date()
        hora = now.time()

        # INSERT movimiento
        if movimiento.insert(id_empleado, tipo, fecha, hora) != True:
            logging.info("Error al registrar el movimiento")
            return 'No se pudo registrar el movimiento'

        return 'Movimiento registrado correctamente'
