#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from database import Database

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')


class Movimiento:
    def insert(self, id_empleado, tipo, fecha, hora):
        """
        Agrega un movimento en la DB
        Recibe id_empleado, tipo, fecha, hora
        Devuelve True si fue realizado con exito
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = 'INSERT INTO movimientos (empleado_id, tipo, fecha, hora) VALUES (%s, %s, %s, %s)'
            values = (id_empleado, tipo, fecha, hora)
            connection['cursor'].execute(query, values)
            connection['db'].commit()
            logging.info(str(connection['cursor'].rowcount) + " Movimiento registrado")
            return True
        finally:
            database.closeConnection()

            
        # TODO: Manejo de excepciones

    def selectAll(self,):
        """
        Devuelve todos los movimientos en la DB
        """
        try:
            database = Database()
            connection = database.getConnection()            
            query = 'SELECT * FROM movimientos'
            connection['cursor'].execute(query)
            movimientos = connection['cursor'].fetchall()
            connection['db'].commit()
            logging.info(str(connection['cursor'].rowcount) + " Movimientos encontrados")
            return movimientos
        finally:
            database.closeConnection()
            # TODO: Manejo de excepciones

    def selectByFechaAndEmpleado(self, fecha, id_empleado):
        """
        Devuelve los movimientos de un empleado en una fecha determinada
        """
        try:
            database = Database()
            connection = database.getConnection()
            query = """SELECT * FROM movimientos WHERE (fecha = %s) AND (empleado_id = %s)"""
            values = (str(fecha), str(id_empleado),)
            connection['cursor'].execute(query, values)
            movimientos = connection['cursor'].fetchall()
            return movimientos
        finally:
            database.closeConnection()
