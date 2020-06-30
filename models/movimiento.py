#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config.database import Database

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
            return True
        except Exception as ex:
            print(str(ex))
        finally:
            database.closeConnection()

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
            return movimientos
        except Exception as ex:
            print(str(ex))            
        finally:
            database.closeConnection()

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
        except Exception as ex:
            print(str(ex))
        finally:
            database.closeConnection()
