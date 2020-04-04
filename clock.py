#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import logging

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

logging.info('Inicio del clock')


def run():
    # Declaracion de variables
    meses = dict()
    meses = {
        "enero": 31,
        "febrero": 27,
        "marzo": 31,
        "abril": 30,
        "mayo": 31,
        "junio": 30,
        "julio": 31,
        "agosto": 31,
        "septiembre": 30,
        "octubre": 31,
        "noviembre": 30,
        "diciembre": 31
    }
    hora = 0
    minuto = 0
    
    # Reloj
    while True:
        for mes, limitDia in meses.items():
            for dia in range(limitDia):
                dia += 1
                while hora < 24:
                    while minuto < 60:
                        os.system('clear')
                        print(mes + ' ' + str(dia) + ' - ' +
                              str(hora) + ':' + str(minuto))
                        time.sleep(1)
                        minuto += 10
                    hora += 1
                    minuto = 0
                hora = 0


def main():
    run()


if __name__ == "__main__":
    main()
