from .modelos import ErrorCompilador
from .Tabla_simbolos import TablaSimbolos
from .Validador_Tipado import ValidadorTipado

class AnalizadorSintactico:
    """Parser por Descenso Recursivo con análisis semántico integrado y recuperación genérica."""
    def __init__(self, tokens: list, tabla_simbolos: TablaSimbolos, reglas_lenguaje):
        self.tokens = tokens
        self.tabla_simbolos = tabla_simbolos
        self.reglas = reglas_lenguaje
        self.indice_actual = 0
        self.errores = []

        # MAPEO GENERAL DE SUGERENCIAS Y EXPECTATIVAS POR TIPO (Español, Inglés y Go)
        self._MAPA_SUGERENCIAS = {
            # Estándar C / C++ / Go
            'int': ("un número entero válido (ej: 20).", 'LITERAL_ENTERO'),
            'float': ("un número decimal válido (ej: 19.5).", 'LITERAL_FLOTANTE'),
            'float32': ("un número decimal de 32 bits (ej: 19.5).", 'LITERAL_FLOTANTE'),
            'float64': ("un número decimal de 64 bits (ej: 19.5).", 'LITERAL_FLOTANTE'),
            'string': ('un texto encerrado entre comillas dobles (ej: "Edwin").', 'LITERAL_STRING'),
            'char': ("un carácter encerrado entre comillas simples (ej: 'A').", 'LITERAL_CHAR'),
            'bool': ("un valor booleano válido ('true' o 'false').", 'LITERAL_BOOLEANO'),
            
            # Estándar Lenguaje Propio (Español)
            'entero': ("un número entero válido (ej: 20).", 'LITERAL_ENTERO'),
            'decimal': ("un número decimal válido (ej: 19.5).", 'LITERAL_FLOTANTE'),
            'texto': ('un texto encerrado entre comillas dobles (ej: "Edwin").', 'LITERAL_STRING'),
            'booleano': ("un valor booleano válido ('verdadero' o 'falso').", 'LITERAL_BOOLEANO')
        }

    def _token_actual(self):
        if self.indice_actual < len(self.tokens):
            return self.tokens[self.indice_actual]
        return None

    def _token_anterior(self):
        if self.indice_actual > 0 and len(self.tokens) > 0:
            return self.tokens[self.indice_actual - 1]
        return None

    def _consumir(self, tipo_esperado: str, mensaje_error: str, sugerencia_error: str) -> bool:
        tok = self._token_actual()
        if tok and tok.tipo_token == tipo_esperado:
            self.indice_actual += 1
            return True
        
        # AJUSTE DE LÍNEA: Si falta un delimitador, la anomalía es de la instrucción anterior
        tok_ant = self._token_anterior()
        if tipo_esperado in ['DELIMITADOR_P_COMA', 'DELIMITADOR_PARENT', 'DELIMITADOR_LLAVE'] and tok_ant:
            linea = tok_ant.linea
        else:
            linea = tok.linea if tok else (self.tokens[-1].linea if self.tokens else 1)

        self.errores.append(ErrorCompilador("Sintáctico", linea, mensaje_error, sugerencia_error))
        return False

    def _sincronizar_modo_panico(self):
        """Avanza los tokens hasta encontrar un delimitador de cierre para contener el efecto dominó."""
        while self._token_actual() is not None:
            tok = self._token_actual()
            if tok.tipo_token == 'DELIMITADOR_P_COMA':
                self.indice_actual += 1  # Consumir el punto y coma y salir del pánico
                break
            if tok.lexema in self.reglas.TIPOS_DATOS or tok.lexema in [self.reglas.IF, self.reglas.PRINT]:
                break
            self.indice_actual += 1

    def analizar(self):
        """Punto de entrada principal para validar el flujo gramatical."""
        self.errores.clear()
        self.tabla_simbolos.limpiar()
        
        while self._token_actual() is not None:
            tok = self._token_actual()
            
            if tok.lexema in self.reglas.TIPOS_DATOS:
                self._analizar_declaracion()
            elif tok.tipo_token == 'IDENTIFICADOR':
                self._analizar_asignacion()
            elif tok.lexema == self.reglas.IF:
                self._analizar_condicional_if()
            elif tok.lexema == self.reglas.PRINT:
                self._analizar_impresion()
            else:
                self.errores.append(ErrorCompilador(
                    "Sintáctico", tok.linea,
                    f"Sentencia iniciada de manera inválida con '{tok.lexema}'",
                    f"Asegúrese de configurar una declaración, asignación, condicional '{self.reglas.IF}' o instrucción '{self.reglas.PRINT}'."
                ))
                self.indice_actual += 1

    def _analizar_declaracion(self):
        tok_tipo = self._token_actual()
        self.indice_actual += 1  # Consumir tipo de dato
        
        tok_id = self._token_actual()
        if not self._consumir('IDENTIFICADOR', "Se esperaba un nombre de variable (identificador).", "Escriba un nombre válido para la variable."):
            self._sincronizar_modo_panico()
            return

        valor_inicial = "N/A"
        tok_siguiente = self._token_actual()
        
        # Validar inicialización opcional inmediata (=)
        if tok_siguiente and tok_siguiente.lexema == '=':
            self.indice_actual += 1  # Consumir '='
            tok_valor = self._token_actual()
            
            literales_validos = ['LITERAL_ENTERO', 'LITERAL_FLOTANTE', 'LITERAL_STRING', 'LITERAL_CHAR', 'LITERAL_BOOLEANO']
            if tok_valor and tok_valor.tipo_token in literales_validos:
                valor_inicial = tok_valor.lexema
                
                # --- CONTROL SEMÁNTICO DE TIPOS ---
                es_compatible = ValidadorTipado.verificar_compatibilidad_asignacion(tok_tipo.lexema, tok_valor.tipo_token)
                if not es_compatible:
                    # Obtener la sugerencia exacta de lo que sí correspondía recibir
                    esperado_sug, _ = self._MAPA_SUGERENCIAS.get(tok_tipo.lexema, ("un valor compatible.", ""))
                    self.errores.append(ErrorCompilador(
                        "Semántico", tok_valor.linea,
                        f"Incompatibilidad de tipos: No se puede asignar el valor '{tok_valor.lexema}' a una variable de tipo '{tok_tipo.lexema}'.",
                        f"Cambie el valor asignado por {esperado_sug}"
                    ))
                self.indice_actual += 1
            else:
                # SOLUCIÓN GENERAL DE SUGERENCIAS SINTÁCTICAS FALTANTES
                esperado_sug, tipo_lit_esperado = self._MAPA_SUGERENCIAS.get(tok_tipo.lexema, ("un valor literal constante.", ""))
                
                # Si el usuario escribió un identificador en vez de un literal (ej: int edad = veinte)
                if tok_valor and tok_valor.tipo_token == 'IDENTIFICADOR':
                    msg = f"Se detectó el identificador '{tok_valor.lexema}' donde se requería un valor constante."
                else:
                    msg = "Se esperaba un valor literal válido tras el operador de asignación '='."

                self.errores.append(ErrorCompilador(
                    "Sintáctico", tok_id.linea, msg, f"Asigne {esperado_sug}"
                ))
                self._sincronizar_modo_panico()
                return

        # Fin de instrucción con punto y coma obligatorio
        if not self._consumir('DELIMITADOR_P_COMA', "Falta el punto y coma ';' al terminar la declaración.", "Agregue un ';' al final de la línea."):
            self._sincronizar_modo_panico()
            return
        
        # --- CONTROL SEMÁNTICO: Registrar en Tabla de Símbolos ---
        exito_insercion = self.tabla_simbolos.insertar(tok_id.lexema, tok_tipo.lexema, "Variable", valor_inicial, tok_tipo.linea)
        if not exito_insercion:
            self.errores.append(ErrorCompilador(
                "Semántico", tok_id.linea,
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
                f"Declare la variable asignándole un tipo (ej: {self.reglas.TIPOS_DATOS.copy().pop() if hasattr(self.reglas, 'TIPOS_DATOS') and self.reglas.TIPOS_DATOS else 'int'} {tok_id.lexema};) antes de usarla."
            ))

        if not self._consumir('OPERADOR_ASIGNACION', "Se esperaba el operador '=' para ejecutar la asignación.", "Inserte el signo '='."):
            self._sincronizar_modo_panico()
            return
            
        # Omitir expresión de manera controlada hasta el punto y coma
        while self._token_actual() and self._token_actual().tipo_token != 'DELIMITADOR_P_COMA':
            self.indice_actual += 1
            
        if not self._consumir('DELIMITADOR_P_COMA', "Falta el punto y coma ';' al finalizar la asignación.", "Coloque un ';' al terminar la expresión."):
            self._sincronizar_modo_panico()
            return
        
        if registro_simbolo:
            self.tabla_simbolos.marcar_como_modificado(tok_id.lexema)

    def _analizar_condicional_if(self):
        self.indice_actual += 1  # Consumir 'if' / 'si'
        
        tiene_parentesis = False
        tok_actual = self._token_actual()
        
        # Go no requiere obligatoriamente paréntesis en las condiciones
        if tok_actual and tok_actual.tipo_token == 'DELIMITADOR_PARENT':
            self.indice_actual += 1  # Consumir '('
            tiene_parentesis = True
        elif self.reglas.NOMBRE != "Subconjunto Go":
            # Si no es Go, los paréntesis son obligatorios
            self.errores.append(ErrorCompilador(
                "Sintáctico", tok_actual.linea if tok_actual else 1,
                "Falta el paréntesis de apertura '(' para encapsular la condición.",
                f"Inserte un '(' después del '{self.reglas.IF}'."
            ))
            return
        
        # Saltar la condición de forma segura hasta el inicio del bloque
        while self._token_actual() and self._token_actual().lexema != ')' and self._token_actual().lexema != '{':
            self.indice_actual += 1
            
        if tiene_parentesis:
            if not self._consumir('DELIMITADOR_PARENT', "Falta el paréntesis de cierre ')' para finalizar la condición.", "Cierre la condición con un ')'."): 
                return
            
        if not self._consumir('DELIMITADOR_LLAVE', f"Falta la llave de apertura '{{' para iniciar el bloque del '{self.reglas.IF}'.", "Abra las llaves '{' para el bloque de código."): 
            return
            
        while self._token_actual() and self._token_actual().lexema != '}':
            tok = self._token_actual()
            if tok.lexema == self.reglas.PRINT:
                self._analizar_impresion()
            elif tok.lexema in self.reglas.TIPOS_DATOS:
                self._analizar_declaracion()
            elif tok.tipo_token == 'IDENTIFICADOR':
                self._analizar_asignacion()
            else:
                self.indice_actual += 1
                
        self._consumir('DELIMITADOR_LLAVE', f"Falta la llave de cierre '}}' para dar fin al bloque condicional.", f"Cierre el bloque del '{self.reglas.IF}' agregando una llave '}}'.")

    def _analizar_impresion(self):
        self.indice_actual += 1  # Consumir print / printf / mostrar / fmt.Println
        if not self._consumir('DELIMITADOR_PARENT', f"Falta '(' en la instrucción '{self.reglas.PRINT}'.", f"Escriba '{self.reglas.PRINT}(' para iniciar."): 
            return
        
        while self._token_actual() and self._token_actual().lexema != ')':
            self.indice_actual += 1
            
        if not self._consumir('DELIMITADOR_PARENT', f"Falta ')' en la instrucción '{self.reglas.PRINT}'.", "Cierre los argumentos con ')'."): 
            return
            
        self._consumir('DELIMITADOR_P_COMA', f"Falta el ';' al concluir la instrucción '{self.reglas.PRINT}'.", "Termine la línea de impresión con un ';'.")
