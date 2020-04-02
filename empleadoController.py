#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import mysql.connector as mysql


# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Configuracion de DB
db = mysql.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="mydatabase"
)
cursor = db.cursor()


class EmpleadoController:
    """
    Devuelve un empleado de la DB ubicandolo por DNI
    """
    def buscarPorDni(self, dni):
        try:
            #SELECT
            query = """SELECT * FROM empleados WHERE dni = %s"""
            values = (str(dni), )
            cursor.execute(query, values)
            empleado = cursor.fetchone()

            # Verifica que se haya encontrado un empleado
            if cursor.rowcount < 1:
                return 'El DNI ingresado es incorrecto'
            return empleado
        except Exception as ex:
            print(ex)
