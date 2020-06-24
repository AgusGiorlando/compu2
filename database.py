#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector as mysql


class Database:
    def __init__(self, ):
        # Configuracion de DB
        self.db = mysql.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="mydatabase"
        )
        self.cursor = self.db.cursor() 
    
    def getConnection(self, ):
        connection = dict()
        connection = {
            'cursor': self.cursor,
            'db': self.db
        }

        return connection

    def closeConnection(self, ):
        # closing database connection.
        self.cursor.close()
        self.db.close()