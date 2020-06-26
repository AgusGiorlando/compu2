#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from config.database import Database

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')


class Empleado:

    def selectAll(self,):
        """
        Devuelve todos los empleados en la DB
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = 'SELECT id, dni, nombre, apellido FROM empleados'
            connection['cursor'].execute(query)
            empleados = connection['cursor'].fetchall()
            connection['db'].commit()
            logging.info(
                str(connection['cursor'].rowcount) + " Empleados encontrados")
            return empleados
        finally:
            database.closeConnection()
        # TODO: Manejo de excepciones

    def selectByDni(self, dni):
        """
        Devuelve un empleado de la DB
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = """SELECT * FROM empleados WHERE dni = %s"""
            values = (str(dni), )
            connection['cursor'].execute(query, values)
            empleado = connection['cursor'].fetchone()
            return empleado
        except Exception as ex:
            print(ex)
        finally:
            database.closeConnection()

    def insert(self, dni, nombre, apellido, clave):
        """
        Inserta un empleado de la DB
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = """INSERT INTO empleados VALUES (NULL, %s, %s, %s, %s)"""
            values = (str(dni), nombre, apellido, clave)
            connection['cursor'].execute(query, values)
            connection['db'].commit()
            logging.info(
                str(connection['cursor'].rowcount) + " Empleado registrado")
            return True
        except Exception as ex:
            print(ex)
        finally:
            database.closeConnection()

    def deleteByDni(self, dni):
        """
        Elimina un empleado de la DB seleccionado por DNI
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = """DELETE FROM empleados WHERE dni = %s"""
            values = (str(dni), )
            connection['cursor'].execute(query, values)
            connection['db'].commit()
            return True
        except Exception as ex:
            print(ex)
        finally:
            database.closeConnection()

    def updateByDni(self, dni, param, value):
        """
        Actualiza un empleado de la DB seleccionado por DNI
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = """UPDATE empleados SET %s=%s WHERE dni=%s"""
            values = (str(dni), )
            connection['cursor'].execute(query, values)
            connection['db'].commit()
            return True
        except Exception as ex:
            print(ex)
        finally:
            database.closeConnection()
