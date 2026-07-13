import re
from .modelos import Token, ErrorCompilador

class AnalizadorLexico:
    """Analizador lexico (lexer), se configura mediante inyeccion de reglas."""
    def __init__(self, reglas_lenguaje):
        self.reglas = reglas_lenguaje
        self.errores = []
        #Construccion del patro Regex Maestro uniendo las especifiaciones
        self._regex_maestro = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.reglas.ESPECIFICACION_TOKENS)
    
    def tokenizar(self, codigo_fuente: str)-> list:
        """Divide el codigo fuente en una lista secuencial de objetos Token"""
        self.errores.clear()
        lista_tokens = []
        lineas = codigo_fuente.split('\n')

        for num_linea, contenido_linea in enumerate(lineas, start=1):
            # Ignorar comentarios de una sola línea (//)
            if contenido_linea.strip().startswith('//'):
                continue
                
            posicion = 0
            while posicion < len(contenido_linea):
                # Omitir espacios en blanco y tabulaciones
                espacio_match = re.match(r'[ \t\r]+', contenido_linea[posicion:])
                if espacio_match:
                    posicion += espacio_match.end()
                    continue

                match = re.match(self._regex_maestro, contenido_linea[posicion:])
                if match:
                    tipo_token = match.lastgroup
                    lexema = match.group(tipo_token)

                    lista_tokens.append(Token(lexema, tipo_token, num_linea))
                    posicion += match.end()
                else:
                    #Captura del Error Lexico (Carcater que no se encuentre mapeado en las expresiones regulares)
                    caracter_invalido = contenido_linea[posicion]
                    self.errores.append(ErrorCompilador(
                    tipo_error="Léxico",
                    linea=num_linea,
                    mensaje=f"Carácter ilegal '{caracter_invalido}' detectado en el flujo de entrada.",
                    sugerencia=f"Elimine el carácter '{caracter_invalido}' de la línea o corrija su escritura." # <-- Corregido a 'sugerencia'
                ))
                    posicion += 1 #Sincronizacion por panico incremental para continuar analizando
        return lista_tokens
        