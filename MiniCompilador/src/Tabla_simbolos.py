class FilaSimbolo:
    """Modela los atributos obligatorios de una variable dentro de la Tabla de Símbolos."""
    def __init__(self, nombre: str, tipo_dato: str, categoria: str, valor_inicial: str, linea: int):
        self.nombre = nombre
        self.tipo_dato = tipo_dato
        self.categoria = categoria
        self.valor_inicial = valor_inicial
        self.linea_declaracion = linea
        self.se_modifica = "No"  #Este campo lo controla el Parser

    def a_diccionario(self) -> dict:
        return {
            "Símbolo": self.nombre,
            "Tipo de dato": self.tipo_dato,
            "Categoría": self.categoria,
            "Valor inicial": self.valor_inicial,
            "Línea de declaración": self.linea_declaracion,
            "¿Se modifica posteriormente?": self.se_modifica
        }

class TablaSimbolos:
    """Gestor de la memoria en tiempo de compilación utilizando tablas Hash O(1)."""
    def __init__(self):
        self.simbolos = {}

    def insertar(self, nombre: str, tipo_dato: str, categoria: str, valor_inicial: str, linea: int) -> bool:
            """
            Inserta un nuevo símbolo en la tabla. 
            Retorna False si el identificador ya existe (Error Semántico de redefinición).
            """
            if nombre in self.simbolos:
                return False
            
            self.simbolos[nombre] = FilaSimbolo(nombre, tipo_dato, categoria, valor_inicial, linea)
            return True

    def buscar(self, nombre: str) -> FilaSimbolo:
            """Recupera la información de un símbolo por su nombre."""
            return self.simbolos.get(nombre, None)
    
    def marcar_como_modificado(self, nombre: str):
        """Cambia de estado de la variable a "si" cuando es el destino de una asignacion"""
        if nombre in self.simbolos:
             self.simbolos[nombre].se_modifica = "Si"
    
    def limpiar(self):
        """Reinicia la tabla para nuevas ejecuciones de codigo"""
        self.simbolos.clear()