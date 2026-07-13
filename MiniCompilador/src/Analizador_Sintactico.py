from .modelos import ErrorCompilador
from .Tabla_simbolos import TablaSimbolos
from .Validador_Tipado import ValidadorTipado

class AnalizadorSintactico:
    """Parser por Descenso Recursivo con análisis semántico integrado."""
    def __init__(self, tokens: list, tabla_simbolos: TablaSimbolos, reglas_lenguaje):
        self.tokens = tokens
        self.tabla_simbolos = tabla_simbolos
        self.reglas = reglas_lenguaje
        self.indice_actual = 0
        self.errores = []

    def _token_actual(self):
        if self.indice_actual < len(self.tokens):
            return self.tokens[self.indice_actual]
        return None

    def _consumir(self, tipo_esperado: str, mensaje_error: str, sugerencia_error: str) -> bool:
        tok = self._token_actual()
        if tok and tok.tipo_token == tipo_esperado:
            self.indice_actual += 1
            return True
        
        # Si falla el emparejamiento sintáctico, registramos el error con sugerencia pragmática
        linea = tok.linea if tok else (self.tokens[-1].linea if self.tokens else 1)
        self.errores.append(ErrorCompilador("Sintáctico", linea, mensaje_error, sugerencia_error))
        return False

    def analizar(self):
        """Punto de entrada principal para validar el flujo gramatical."""
        self.errores.clear()
        self.tabla_simbolos.limpiar()
        
        while self._token_actual() is not None:
            tok = self._token_actual()
            
            # Enrutamiento sintáctico predictivo según el Lexema o Tipo
            if tok.lexema in self.reglas.TIPOS_DATOS:
                self._analizar_declaracion()
            elif tok.tipo_token == 'IDENTIFICADOR':
                self._analizar_asignacion()
            elif tok.lexema == 'if':
                self._analizar_condicional_if()
            elif tok.lexema == 'print':
                self._analizar_impresion()
            else:
                self.errores.append(ErrorCompilador(
                    "Sintáctico", tok.linea,
                    f"Sentencia iniciada de manera inválida con '{tok.lexema}'",
                    "Asegúrese de estructurar una declaración, asignación, condicional 'if' o instrucción 'print'."
                ))
                self.indice_actual += 1

    def _analizar_declaracion(self):
        tok_tipo = self._token_actual()
        self.indice_actual += 1  # Consumir el tipo de dato seguro
        
        tok_id = self._token_actual()
        if not self._consumir('IDENTIFICADOR', "Se esperaba un nombre de variable (identificador).", "Escriba un nombre válido para la variable."):
            return

        valor_inicial = "N/A"
        tok_siguiente = self._token_actual()
        
        # Validar inicialización opcional inmediata
        if tok_siguiente and tok_siguiente.lexema == '=':
            self.indice_actual += 1  # Consumir '='
            tok_valor = self._token_actual()
            
            literales_validos = ['LITERAL_ENTERO', 'LITERAL_FLOTANTE', 'LITERAL_STRING', 'LITERAL_CHAR', 'LITERAL_BOOLEANO']
            if tok_valor and tok_valor.tipo_token in literales_validos:
                valor_inicial = tok_valor.lexema
                
                # --- CONTROL SEMÁNTICO DE TIPOS ---
                es_compatible = ValidadorTipado.verificar_compatibilidad_asignacion(tok_tipo.lexema, tok_valor.tipo_token)
                if not es_compatible:
                    self.errores.append(ErrorCompilador(
                        "Semántico", tok_valor.linea,
                        f"Incompatibilidad de tipos: No se puede asignar '{tok_valor.lexema}' a una variable tipo '{tok_tipo.lexema}'.",
                        f"Asegúrese de proveer un valor compatible con el tipo '{tok_tipo.lexema}'."
                    ))
                self.indice_actual += 1
            else:
                self.errores.append(ErrorCompilador("Sintáctico", tok_id.linea, "Se esperaba un valor literal tras el operador de asignación '='.", "Asigne un número, texto, carácter o booleano válido."))
                return

        # Fin de instrucción con punto y coma obligatorio
        self._consumir('DELIMITADOR_P_COMA', "Falta el punto y coma ';' al terminar la declaración.", "Agregue un ';' al final de la línea.")
        
        # --- CONTROL SEMÁNTICO: Registrar en Tabla de Símbolos ---
        exito_insercion = self.tabla_simbolos.insertar(tok_id.lexema, tok_tipo.lexema, "Variable", valor_inicial, tok_tipo.linea)
        if not exito_insercion:
            self.errores.append(ErrorCompilador(
                "Semántico", tok_id.linea, # Corregido tok_id.linea
                f"Doble declaración: La variable '{tok_id.lexema}' ya existe en este contexto.",
                "Utilice un nombre único para declarar esta variable o elimine la duplicada."
            ))

    def _analizar_asignacion(self):
        tok_id = self._token_actual()
        self.indice_actual += 1
        
        # --- CONTROL SEMÁNTICO: Verificar existencia ---
        registro_simbolo = self.tabla_simbolos.buscar(tok_id.lexema)
        if not registro_simbolo:
            self.errores.append(ErrorCompilador(
                "Semántico", tok_id.linea,
                f"Variable no declarada: '{tok_id.lexema}' está siendo usada sin definición previa.",
                f"Declare la variable asignándole un tipo (ej: int {tok_id.lexema};) antes de usarla."
            ))

        # Cambiado de _consume a _consumir
        if not self._consumir('OPERADOR_ASIGNACION', "Se esperaba el operador '=' para ejecutar la asignación.", "Inserte el signo '='."):
            return
            
        # Omitir de forma controlada la expresión aritmética hasta el ; para este avance
        while self._token_actual() and self._token_actual().tipo_token != 'DELIMITADOR_P_COMA':
            self.indice_actual += 1
            
        # Cambiado de _consume a _consumir
        self._consumir('DELIMITADOR_P_COMA', "Falta el punto y coma ';' al finalizar la asignación.", "Coloque un ';' al terminar la expresión matemática.")
        
        # --- CONTROL SEMÁNTICO: Cambiar mutabilidad ---
        if registro_simbolo:
            self.tabla_simbolos.marcar_como_modificado(tok_id.lexema)

    def _analizar_condicional_if(self):
        self.indice_actual += 1  # Consumir 'if'
        
        # Cambiado de _consume a _consumir
        if not self._consumir('DELIMITADOR_PARENT', "Falta el paréntesis de apertura '(' para encapsular la condición.", "Inserte un '(' después del 'if'."): 
            return
        
        while self._token_actual() and self._token_actual().lexema != ')':
            self.indice_actual += 1
            
        # Cambiado de _consume a _consumir
        if not self._consumir('DELIMITADOR_PARENT', "Falta el paréntesis de cierre ')' para finalizar la condición.", "Cierre la condición con un ')'."): 
            return
        # Cambiado de _consume a _consumir
        if not self._consumir('DELIMITADOR_LLAVE', "Falta la llave de apertura '{' para iniciar el bloque del 'if'.", "Abra las llaves '{' para el bloque de código."): 
            return
            
        # Procesar de manera interna las sentencias del bloque recursivamente
        while self._token_actual() and self._token_actual().lexema != '}':
            tok = self._token_actual()
            if tok.lexema == 'print':
                self._analizar_impresion()
            else:
                self.indice_actual += 1
                
        # Cambiado de _consume a _consumir
        self._consumir('DELIMITADOR_LLAVE', "Falta la llave de cierre '}' para dar fin al bloque condicional.", "Cierre el bloque del 'if' agregando una llave '}'.")

    def _analizar_impresion(self):
        self.indice_actual += 1  # Consumir 'print'
        # Cambiado de _consume a _consumir
        if not self._consumir('DELIMITADOR_PARENT', "Falta '(' en la instrucción 'print'.", "Escriba 'print(' para iniciar."): return
        
        while self._token_actual() and self._token_actual().lexema != ')':
            self.indice_actual += 1
            
        # Cambiado de _consume a _consumir
        if not self._consumir('DELIMITADOR_PARENT', "Falta ')' en la instrucción 'print'.", "Cierre los argumentos con ')'."): return
        self._consumir('DELIMITADOR_P_COMA', "Falta el ';' al concluir la instrucción 'print'.", "Termine la línea de impresión con un ';'.")