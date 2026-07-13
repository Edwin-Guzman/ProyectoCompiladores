from .Reglas_Base import ReglasBase

class ReglasCpp(ReglasBase):
    """Reglas lexicas y gramaticales para el subconjunto del lenguaje C++."""
    NOMBRE = "Subconjunto C++"
    
    ESPECIFICACION_TOKENS = [
        ('PALABRA_RESERVADA', r'\b(int|float|double|char|bool|if|else|while|return|using|namespace|std)\b'),
        ('OPERADOR_FLUJO',    r'<<|>>'),
        ('ELEMENTO_STREAM',   r'\b(cout|cin|endl)\b'),
        ('LITERAL_BOOLEANO',  r'\b(true|false)\b'),
        ('IDENTIFICADOR',     r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('LITERAL_FLOTANTE',  r'\b\d+\.\d+\b'),
        ('LITERAL_ENTERO',    r'\b\d+\b'),
        ('OPERADOR_RELACIONAL', r'>=|<=|==|!=|>|<'),
        ('OPERADOR_ASIGNACION', r'='),
        ('OPERADOR_ARITMETICO', r'\+|-|\*|/'),
        ('DELIMITADOR_P_COMA', r';'),
        ('DELIMITADOR_PARENT', r'\(|\)'),
        ('DELIMITADOR_LLAVE',  r'\{|\}'),
    ]
    
    TIPOS_DATOS = {'int', 'float', 'double', 'char', 'bool'}