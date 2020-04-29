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

    def insert(self, dni, nombre, apellido, clave):
        """
        Inserta un empleado de la DB
        """
        query = """INSERT INTO empleados VALUES (NULL, %s, %s, %s, %s)"""
        values = (str(dni), nombre, apellido, clave)
        cursor.execute(query, values)
        db.commit()
        logging.info(str(cursor.rowcount) + " Empleado registrado")
        return True

    def deleteByDni(self, dni):
        """
        Elimina un empleado de la DB seleccionado por DNI
        """
        query = """DELETE FROM empleados WHERE dni = %s"""
        values = (str(dni), )
        cursor.execute(query, values)
        db.commit()
        return True

    def updateByDni(self, dni, param, value):
        """
        Actualiza un empleado de la DB seleccionado por DNI
        """
        query = """UPDATE empleados SET %s=%s WHERE dni=%s"""
        values = (str(dni), )
        cursor.execute(query, values)
        db.commit()
        return True
