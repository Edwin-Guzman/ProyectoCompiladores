class ValidadorTipado:
    """Ecpasula las reglas semanticas de validacion de tipos del compilador"""
    @staticmethod
    def verificar_compatibilidad_asignacion(tipo_variable: str, tipo_literal: str) -> bool:
        """Determinar si un literal puede ser asignado a una variable de cierto tipo."""
        #Mapeamos los tokens lexicos a tipos de datos
        mapeo_literales ={
            'LITERAL_ENTERO': 'int',
            'LITERAL_FLOTANTE': 'float',
            'LITERAL_STRING': 'string',
            'LITERAL_CHAR': 'char',
            'LITERAL_BOOLEANO': 'bool'
        }
        tipo_evaluado = mapeo_literales.get(tipo_literal, tipo_literal)
        #Regla estricta: Coincidencia exacta de tipos
        if tipo_variable == tipo_evaluado:
            return True
        #Regla felxible: Permitir asignar int dentro de una variable double/float. Eje. promocion
        if tipo_variable in ['float', 'double'] and tipo_evaluado == 'int':
            return True
        return False
    @staticmethod
    def inferir_tipo_operacion(tipo_izq: str, tipo_der: str, operador: str)-> str:
        """Evalua semanticamente el tipo resultante de unna operacion aritemetica o relacional"""
        #Operaciones entre numericos
        tipos_numericos = {'int', 'float', 'double'}

        if tipo_izq in tipos_numericos and tipo_der in tipos_numericos:
            if operador in ['>=', '<=', '==', '!=', '>', '<']:
                return 'bool' #Operacion relacional genera boolenao
            
            #Promocion aritmetica 
            if tipo_izq == 'double' or tipo_der == 'double':
                return 'double'
            if tipo_izq == 'float' or tipo_der == 'float':
                return 'float'
            return 'int'
        return 'error_semantico'