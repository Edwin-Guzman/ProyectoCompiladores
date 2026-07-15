from .Reglas_Base import ReglasBase

class ReglasLenguajePropio(ReglasBase):
    """Reglas léxicas y gramaticales específicas del Lenguaje Propio."""
    NOMBRE = "Lenguaje Propio"
    
    # Especificacion de tokens detallada mediante expresiones regulares
    ESPECIFICACION_TOKENS = [
        # Las palabras reservadas del lenguaje adaptadas a español
        ('PALABRA_RESERVADA', r'\b(entero|decimal|texto|booleano|si|sino|mostrar)\b'),
        ('LITERAL_BOOLEANO',  r'\b(verdadero|falso)\b'),
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
    
    # --- LA CORRECCIÓN CLAVE ---
    # Ahora el Analizador Sintáctico sabrá que 'entero' y 'texto' son tipos de datos legítimos
    TIPOS_DATOS = {'entero', 'decimal', 'texto', 'booleano'}
    
    # Mapeo de enrutamiento para el Parser y el Ejecutor
    IF = "si"
    PRINT = "mostrar"
