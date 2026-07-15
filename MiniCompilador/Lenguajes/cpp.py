from .Reglas_Base import ReglasBase

class ReglasCpp(ReglasBase):
    """Reglas léxicas y gramaticales para el subconjunto del lenguaje C++."""
    NOMBRE = "Subconjunto C++"
    
    ESPECIFICACION_TOKENS = [
        ('PALABRA_RESERVADA', r'\b(int|float|double|char|string|bool|if|else|cout)\b'),
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
    
    TIPOS_DATOS = {'int', 'float', 'double', 'char', 'string', 'bool'}
    
    IF = "if"
    PRINT = "cout"
