#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
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

    """
    Crea un nuevo empleado
    """

    def createEmpleado(self, dni, nombre, apellido, clave):
        try:
            if empleado.insert(dni, nombre, apellido, clave) != True:
                logging.error("Error al registrar el empleado")
                return 'No se pudo registrar el empleado'
            return 'Empleado registrado correctamente'
        except Exception as ex:
            return str(ex)

    """
    Elimina un empleado por su dni
    """
    def deleteEmpleadoByDni(self, dni):
        try:
            if empleado.deleteByDni(dni) != True:
                logging.error("Error al registrar el empleado")
                return 'No se pudo registrar el empleado'
            return 'Empleado eliminado correctamente'
        except Exception as ex:
            return str(ex)

