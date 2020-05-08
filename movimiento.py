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


class Movimiento:
    def insert(self, id_empleado, tipo, fecha, hora):
        """
        Agrega un movimento en la DB
        Recibe id_empleado, tipo, fecha, hora
        Devuelve True si fue realizado con exito
        """
        query = 'INSERT INTO movimientos (empleado_id, tipo, fecha, hora) VALUES (%s, %s, %s, %s)'
        values = (id_empleado, tipo, fecha, hora)
        cursor.execute(query, values)
        db.commit()
        logging.info(str(cursor.rowcount) + " Movimiento registrado")
        return True
        # TODO: Manejo de excepciones

    def selectAll(self,):
        """
        Devuelve todos los movimientos en la DB
        """
        query = 'SELECT * FROM movimientos'
        cursor.execute(query)
        movimientos = cursor.fetchall()
        db.commit()
        logging.info(str(cursor.rowcount) + " Movimientos encontrados")
        return movimientos
        # TODO: Manejo de excepciones

    def selectByFechaAndEmpleado(self, fecha, id_empleado):
        """
        Devuelve los movimientos de un empleado en una fecha determinada
        """
        query = """SELECT * FROM movimientos WHERE (fecha = %s) AND (empleado_id = %s)"""
        values = (str(fecha), str(id_empleado),)
        cursor.execute(query, values)
        movimientos = cursor.fetchall()
        return movimientos
