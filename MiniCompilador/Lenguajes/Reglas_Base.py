class ReglasBase:
    """Clase abstarcta de base para definir las especificicaciones de un lenguaje"""
    NOMBRE = "Base"

    #Lista de tuplas (TIPO_TOKEN, REGEX)
    ESPECIFICACION_TOKENS = []

    #Conjunto de tipos de datos permitidos
    TIPOS_DATOS = set()
    