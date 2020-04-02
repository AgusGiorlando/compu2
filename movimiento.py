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
    """
    Agrega un movimento en la DB
    Recibe id_empleado, tipo, fecha, hora
    Devuelve True si fue realizado con exito
    """
    def insert(self, id_empleado, tipo, fecha, hora):
        query = 'INSERT INTO movimientos (empleado_id, tipo, fecha, hora) VALUES (%s, %s, %s, %s)'
        values = (id_empleado, tipo, fecha, hora)
        cursor.execute(query, values)
        db.commit()
        logging.info(str(cursor.rowcount) + " Movimiento registrado")
        return True
        # TODO: Manejo de excepciones
