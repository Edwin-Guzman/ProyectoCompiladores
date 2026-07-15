class ValidadorTipado:
    """Encapsula las reglas semánticas de validación de tipos del compilador de forma multilenguaje."""
    
    # Unificación de tipos equivalentes de todos los lenguajes soportados a un "tipo base unificado"
    _FAMILIAS_TIPOS = {
        # Familias de enteros
        'int': 'ENTERO_COMUN',
        'entero': 'ENTERO_COMUN',
        
        # Familias de decimales
        'float': 'DECIMAL_COMUN',
        'double': 'DECIMAL_COMUN',
        'float32': 'DECIMAL_COMUN',
        'float64': 'DECIMAL_COMUN',
        'decimal': 'DECIMAL_COMUN',
        
        # Familias de cadenas / texto
        'string': 'CADENA_COMUN',
        'texto': 'CADENA_COMUN',
        'char': 'CADENA_COMUN',  # Permitimos asignar caracteres sencillos a textos
        
        # Familias de booleanos
        'bool': 'BOOLEANO_COMUN',
        'booleano': 'BOOLEANO_COMUN'
    }

    @staticmethod
    def _normalizar_tipo(tipo: str) -> str:
        """Helper para traducir cualquier tipo sintáctico a su familia lógica base."""
        if not tipo:
            return 'DESCONOCIDO'
        tipo_limpio = tipo.lower().strip()
        return ValidadorTipado._FAMILIAS_TIPOS.get(tipo_limpio, tipo_limpio)

    @staticmethod
    def verificar_compatibilidad_asignacion(tipo_variable: str, tipo_literal: str) -> bool:
        """Determinar de manera general si un literal puede ser asignado a una variable de cierto tipo."""
        
        # Mapeamos los tokens léxicos a tipos de datos básicos
        mapeo_literales = {
            'LITERAL_ENTERO': 'int',
            'LITERAL_FLOTANTE': 'float',
            'LITERAL_STRING': 'string',
            'LITERAL_CHAR': 'char',
            'LITERAL_BOOLEANO': 'bool'
        }
        
        # 1. Obtener el tipo crudo que representa el token literal
        tipo_evaluado = mapeo_literales.get(tipo_literal, tipo_literal)
        
        # 2. Normalizar ambos a su familia lógica base
        familia_variable = ValidadorTipado._normalizar_tipo(tipo_variable)
        familia_evaluado = ValidadorTipado._normalizar_tipo(tipo_evaluado)
        
        # Regla estricta: Coincidencia de familias lógicas (ej: 'texto' y 'string' => 'CADENA_COMUN')
        if familia_variable == familia_evaluado:
            return True
            
        # Regla flexible: Permitir asignar enteros dentro de variables decimales (promoción/conversión)
        if familia_variable == 'DECIMAL_COMUN' and familia_evaluado == 'ENTERO_COMUN':
            return True
            
        return False

    @staticmethod
    def inferir_tipo_operacion(tipo_izq: str, tipo_der: str, operador: str) -> str:
        """Evalúa semánticamente el tipo resultante de una operación aritmética o relacional."""
        
        # Normalizamos los operandos de entrada para que el análisis sea agnóstico al lenguaje
        fam_izq = ValidadorTipado._normalizar_tipo(tipo_izq)
        fam_der = ValidadorTipado._normalizar_tipo(tipo_der)
        
        # Operaciones entre numéricos
        tipos_numericos = {'ENTERO_COMUN', 'DECIMAL_COMUN'}

        if fam_izq in tipos_numericos and fam_der in tipos_numericos:
            # Los operadores relacionales siempre resultan en un tipo Booleano nativo del lenguaje activo
            # Devolvemos el tipo base correspondiente para que sea procesado
            if operador in ['>=', '<=', '==', '!=', '>', '<']:
                return 'bool' if tipo_izq not in ['entero', 'decimal'] else 'booleano'
            
            # Promoción aritmética dinámica
            if fam_izq == 'DECIMAL_COMUN' or fam_der == 'DECIMAL_COMUN':
                return 'double' if 'double' in [tipo_izq, tipo_der] else ('decimal' if 'decimal' in [tipo_izq, tipo_der] else 'float')
                
            return 'int' if tipo_izq != 'entero' else 'entero'
            
        return 'error_semantico'
