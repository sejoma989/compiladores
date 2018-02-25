# ----------------------------------------------------------------------
# El siguiente import carga una función error(lineno,msg) que se debe
# utilizar para informar de todos los mensajes de error emitidos por su
# lexer. Las pruebas unitarias y otras caracteristicas del compilador
# confiarán en esta función. Ver el archivo errors.py para más documentación
# acerca del mecanismo de manejo de errores.
from errors import error

# ----------------------------------------------------------------------
# El paquete SLY. https://github.com/dabeaz/sly
from sly import Lexer

class HOCLexer(Lexer):

    # ----------------------------------------------------------------------
    # Conjunto de palabras reservadas. Este conjunto enumera todos los
    # nombres especiales utilizados en el lenguaje, como 'if', 'else',
    # 'while', 'return', etc.
    keywords = { 'var', 'const', 'print', 'func', 'proc', 'extern', 'if', 'while', 'for', 'else', 'return'}

    # ----------------------------------------------------------------------
    # Conjunto de token. Este conjunto identifica la lista completa de
    # nombres de tokens que reconocerá su lexer. No cambie ninguno de estos
    # nombres.
    tokens = {
        # keywords (incorpora versiones de mayúsculas y minúsculas de las palabras clave anteriores)
        * { kw.upper() for kw in keywords },

        # Identificadores
        'ID', 'FUNCTION', 'PROCEDURE',

        # Literales
        'INTEGER', 'FLOAT', 'STRING',

        # Operadores y delimitadores
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'BLTIN', 'UNDEF', 'READ', 'OR',
        'AND', 'LE', 'EQ', 'GE', 'NE', 'INC', 'DEC', 'POWER', 'LT', 'GT',

        # Delimitadores y otros símbolos
        'ASSIGN', 'LPAREN', 'RPAREN', 'SEMI', 'COMMA',
        'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'ADDEQ', 'SUBEQ', 'MULEQ',
        'DIVEQ', 'MODEQ', 'MODULE', 'ARG', 'NOT'
    }

    # ----------------------------------------------------------------------
    # Caracteres ignorados (whitespace)
    #
    # Los siguientes caracteres son ignorados completamente por el lexer.
    # No lo cambie.
    ignore = ' \t\r'

    # ----------------------------------------------------------------------
    # Patrones ignorados.  Complete las expresiones regulares a continuación
    # para ignorar los comentarios
    #

    # Comentario estilo-C (/* ... */)
    @_(r'/\*.*\*/')
    def COMMENT(self, t):
        self.lineno += t.value.count('\n')

    # Comentario estilo-C++ (//...)
    @_(r'//.*')
    def CPPCOMMENT(self, t):
        self.lineno += 1

    # Comentario sin terminar estilo-C. Este es un error que se debe reportar
    @_(r'/\*[^/\*]*')
    def COMMENT_UNTERM(self, t):
        error(self.lineno, "Comentario sin terminar")

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escriba las expresiones regulares que se indican a continuación.
    #
    # Tokens para símbolos simples: + - * / = ( ) ; < >, etc.
    #
    # Precaución: El orden de las definiciones es importante. Los símbolos
    # más largos deben aparecer antes de los símbolos más cortos que son
    # una subcadena (por ejemplo, el patrón para <= debe ir antes de <).

    ADDEQ    = r'\+='
    SUBEQ    = r'-='
    MULEQ    = r'\*='
    DIVEQ    = r'\/='
    MODEQ    = r'\%='
    OR       = r'\|\|'
    AND      = r'\&\&'
    LE       = r'<='
    EQ       = r'=='
    GE       = r'>='
    NE       = r'!='
    INC      = r'\+\+'
    DEC      = r'--'
    PLUS     = r'\+'
    MINUS    = r'-'
    TIMES    = r'\*'
    DIVIDE   = r'\/'
    SEMI     = r';'
    LPAREN   = r'\('
    RPAREN   = r'\)'
    COMMA    = r','
    LBRACKET = r'\{'
    RBRACKET = r'\}'
    ASSIGN   = r'='
    POWER    = r'\^'
    MODULE   = r'\%'
    ARG      = r'\?'
    LT       = r'<'
    GT       = r'>'
    NOT      = r'!'

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escriba las expresiones regulares y el código adicional a continuación
    #
    # Tokens para literales, INTEGER, FLOAT, STRING.

    # Constante de punto flotante. Debe reconocer los números de punto
    # flotante en los siguientes formatos:
    #
    #   1.23
    #   123.
    #   .123
    #
    # Bonificación: reconocer números flotantes en notación científica
    #
    #   1.23e1
    #   1.23e+1
    #   1.23e-1
    #   1e1
    #
    # El valor debe ser convertir en un float de Python cuando se lea

    @_(r'(\d*\.\d*)(e[-+]?\d+)?|([1-9]\d*)(e\d+)')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    # Constante entera
    #
    #     1234             (decimal)
    #
    # El valor debe ser convertido a un int de Python cuando se lea.
    #
    # Bonificación. Reconocer enteros en diferentes bases tales como 0x1a, 0o13 or 0b111011.
    @_(r'(\d+)|(0b[0-1]+)|(0o[0-7]+)|(0x[0-9a-f]+)')
    def INTEGER(self, t):
        # Conversion a int de Python
        t.value = int(t.value)
        return t

    # Constante de Cadena. Se debe reconocer texto encerrado entre comillas dobles.
    # Por ejemplo:
    #
    #     "Hola Mundo"
    #
    # Las comillas no son incluidas como parte de su valor.
    #
    # Bonificación: ¿Cómo reconocer secuencias de escape como \" o \ n?
    @_(r'(\".*\")')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    # Cadenas sin terminar (un error)
    @_(r'\"[^\"]*')
    def STRING_UNTERM(self, t):
        error(self.lineno, "Cadena sin terminar")
        self.lineno += 1

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escribir la expresión regular y agregar palabras reservadas
    #
    # Identificadores y palabras reservadas
    #
    # Concuerde con un identificador. Los identificadores siguen las mismas
    # reglas que Python. Es decir, comienzan con una letra o un guión bajo (_)
    # y pueden contener una cantidad arbitraria de letras, dígitos o guiones
    # bajos después de eso.
    # Las palabras reservadas del lenguaje como "if" y "while" también se
    # combinan como identificadores. Debe capturar estos y cambiar su tipo
    # de token para que coincida con la palabra clave adecuada.

    @_(r'[a-zA-Z][a-zA-Z]*\d*_*|[_][a-zA-Z]*\d*_*')
    def ID(self, t):
        if t.value == 'var':
            t.type = 'VAR'

        if t.value == 'const':
            t.type = 'CONST'

        if t.value == 'print':
            t.type = 'PRINT'

        if t.value == 'func':
            t.type = 'FUNC'

        if t.value == 'extern':
            t.type = 'EXTERN'
        # *** IMPLEMENTE ***
        # Agregar código para buscar palabras clave como 'var', 'const', 'print', etc.
        # Cambia el tipo de token según sea necesario. Por ejemplo:
        #
        # if t.value == 'var':
        #     t.type = 'VAR"

        return t

    # ----------------------------------------------------------------------
    # Método que ignora una o más líneas e incrementa el número de ellas
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # ----------------------------------------------------------------------
    # Manejo de errores de caracteres incorrectos
    def error(self, value):
        error(self.lineno,"Caracter ilegal %r" % value[0])
        self.index += 1

# ------------------------------------------------- ---------------------
#                   NO CAMBIE NADA POR DEBAJO DE ESTA PARTE
#
# Use este programa principal para probar/depurar su Lexer. Ejecutelo usando la opción -m
#
#    bash% python3 -m hoc.tokenizer filename.hoc
#
# ------------------------------------------------- ---------------------

def main():
    '''
    Programa principal. Para fines de depuración.
    '''
    import sys
    #sys.argv.append('test/test.bas')
    if len(sys.argv) != 2:
        sys.stderr.write("Uso: python3 -m hoc.tokenizer filename\n")
        raise SystemExit(1)

    lexer = HOCLexer()
    text = open(sys.argv[1]).read()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    main()
