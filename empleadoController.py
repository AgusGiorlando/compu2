#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import mysql.connector as mysql
from empleado import Empleado


# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
empleado = Empleado()


class EmpleadoController:
    """
    Devuelve un empleado de la DB ubicandolo por DNI
    """

    def buscarPorDni(self, dni):
        try:
            # SELECT
            result = empleado.selectByDni(dni)

            # Verifica que se haya encontrado un empleado
            if len(result) < 1:
                return 'El DNI ingresado es incorrecto'
            return result
        except Exception as ex:
            print(ex)

    """
    Devuelve todos los empleados
    """

    def getEmpleados(self, ):
        try:
            # SELECT
            empleados = empleado.selectAll()
            return empleados
        except Exception as ex:
            print(ex)
