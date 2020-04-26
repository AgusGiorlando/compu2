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


class Empleado:

    def selectAll(self,):
        """
        Devuelve todos los empleados en la DB
        """
        query = 'SELECT * FROM empleados'
        cursor.execute(query)
        empleados = cursor.fetchall()
        db.commit()
        logging.info(str(cursor.rowcount) + " Empleados encontrados")
        return empleados
        # TODO: Manejo de excepciones

    def selectByDni(self, dni):
        """
        Devuelve un empleado de la DB
        """
        query = """SELECT * FROM empleados WHERE dni = %s"""
        values = (str(dni), )
        cursor.execute(query, values)
        empleado = cursor.fetchone()
        return empleado
