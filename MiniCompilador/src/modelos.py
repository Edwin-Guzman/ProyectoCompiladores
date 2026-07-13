class Token:
    """Representa un token identificado por el Lexer"""
    def __init__(self, lexema: str, tipo_token: str, linea: int):
        self.lexema = lexema
        self.tipo_token = tipo_token
        self.linea = linea
    
    def a_fila_tabla(self) -> dict:
        """Devuelve un diccionario con los datos del token para ser usado en la tabla de la interfaz"""
        return {
            "Token (Lexema)": self.lexema,
            "Tipo de Token": self.tipo_token,
            "Linea": self.linea
        }

class ErrorCompilador:
    """Estructura para almacenar errores lexicos, sintacticos y semanticos"""
    def __init__(self, tipo_error: str, linea: int, mensaje: str, sugerencia: str):
        self.tipo_error = tipo_error
        self.linea = linea
        self.mensaje = mensaje
        self.sugerencia = sugerencia
    
    # ¡Corregido aquí! Ahora está correctamente indentado dentro de la clase
    def a_fila_tabla(self) -> dict:
        """Formatea el error para el panel de diagnóstico tabular."""
        return {
            "Fase / Tipo": self.tipo_error,
            "Línea": self.linea,
            "Mensaje de Error": self.mensaje,
            "Solucion Sugerida": self.sugerencia
        }