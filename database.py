#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector as mysql
import os


class Database:
    def __init__(self, ):
        # Configuracion de DB
        self.db = mysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWD"),
            database=os.getenv("DATABASE")
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