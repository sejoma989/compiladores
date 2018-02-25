# errors.py
# coding: utf-8
'''
Soporte para el manejo de errores del compilador.

Una de las partes mas importantes (y molestas) de escribir un compilador
es el informe confiable de los mensajes de error al usuario. Este archivo
define algunas funcionalidades genericas para tratar los errores en todo
el proyecto del compilador. Es posible que desee expandir esto con
capacidades adicionales a los efectos de las pruebas unitarias.

Para reportar errores en su compilador, use la funcion error(). Por ejemplo:

       error(lineno, 'Algun tipo de mensaje de error del compilador')

donde lineno es el numero de linea en el que se produjo el error. Si su
compilador admite varios archivos de origen, agregue el argumento de palabra
clave de nombre de archivo.

       error(lineno, 'Algun tipo de mensaje de error', filename='foo.src')

La funcion de utilidad errors_reported() devuelve el numero total de
errores informados hasta el momento. Diferentes etapas del compilador
pueden usar esto para decidir si continuar o no procesando.

Use clear_errors() para borrar el numero total de errores.
'''

import sys

_num_errors = 0

def error(lineno, message, filename=None):
    '''
    Reporta un error de compilacion a todos los suscriptores
    '''
    global _num_errors
    if not filename:
        errmsg = "{}: {}".format(lineno, message)
    else:
        errmsg = "{}:{}: {}".format(filename,lineno,message)

    print(errmsg, file=sys.stderr)
    _num_errors += 1

def errors_reported():
    '''
    Retorna el numero de errores reportados
    '''
    return _num_errors

def clear_errors():
    '''
    Borre la cantidad total de errores reportados.
    '''
    global _num_errors
    _num_errors = 0
