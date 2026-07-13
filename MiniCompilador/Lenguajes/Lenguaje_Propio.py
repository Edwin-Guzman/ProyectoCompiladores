from .Reglas_Base import ReglasBase

class ReglasLenguajePropio(ReglasBase):
    """Reglas léxicas y gramaticales específicas del Lenguaje Propio."""
    NOMBRE = "Lenguaje Propio"
    
    # Especificación de tokens detallada mediante expresiones regulares
    ESPECIFICACION_TOKENS = [
        ('PALABRA_RESERVADA', r'\b(int|float|double|char|string|bool|if|else|print)\b'),
        ('LITERAL_BOOLEANO',  r'\b(true|false)\b'),
        ('IDENTIFICADOR',     r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('LITERAL_FLOTANTE',  r'\b\d+\.\d+\b'),
        ('LITERAL_ENTERO',    r'\b\d+\b'),
        ('LITERAL_STRING',    r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ('LITERAL_CHAR',      r"'[^'\\]'"),
        ('OPERADOR_RELACIONAL', r'>=|<=|==|!=|>|<'),
        ('OPERADOR_ASIGNACION', r'='),
        ('OPERADOR_ARITMETICO', r'\+|-|\*|/'),
        ('DELIMITADOR_P_COMA', r';'),
        ('DELIMITADOR_PARENT', r'\(|\)'),
        ('DELIMITADOR_LLAVE',  r'\{|\}'),
    ]
    
    # Tipos de datos que el Analizador Sintactico reconocera para declaraciones
    TIPOS_DATOS = {'int', 'float', 'double', 'char', 'string', 'bool'}