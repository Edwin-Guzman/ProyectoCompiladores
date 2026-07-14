from .Reglas_Base import ReglasBase

class ReglasGo(ReglasBase):
    """Reglas léxicas y gramaticales para el subconjunto del lenguaje Go."""
    NOMBRE = "Subconjunto Go"
    
    ESPECIFICACION_TOKENS = [
        # 'fmt.Println' es tratado de manera léxica como palabra reservada o identificador especial
        ('PALABRA_RESERVADA', r'\b(int|float64|float32|string|bool|if|else)\b|fmt\.Println'),
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
    
    # En Go se usa 'int', 'float64', 'string', 'bool'
    TIPOS_DATOS = {'int', 'float64', 'float32', 'string', 'bool'}
    
    IF = "if"
    PRINT = "fmt.Println"
