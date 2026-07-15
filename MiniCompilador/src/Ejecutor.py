class EjecutorSimulado:
    """Ejecuta de manera lógica el AST simplificado o las instrucciones del parser
    para generar la salida de consola en caso de éxito."""
    
    @staticmethod
    def ejecutar(tokens: list, tabla_simbolos, reglas_lenguaje) -> str:
        salida = []
        indice = 0
        
        # Buscamos de manera secuencial instrucciones de impresión
        while indice < len(tokens):
            tok = tokens[indice]
            
            # Si encontramos una instrucción de impresión
            if tok.lexema == reglas_lenguaje.PRINT:
                # Buscamos el argumento dentro de los paréntesis
                # print( argumento ) -> avanzar hasta encontrar el valor
                arg_tokens = []
                indice += 2  # Saltar 'print' y '('
                
                while indice < len(tokens) and tokens[indice].lexema != ')':
                    arg_tokens.append(tokens[indice])
                    indice += 1
                
                # Procesar el argumento de la impresión
                for arg in arg_tokens:
                    if arg.tipo_token == 'IDENTIFICADOR':
                        # Buscar en tabla de símbolos
                        simbolo = tabla_simbolos.buscar(arg.lexema)
                        if simbolo:
                            # Quitar comillas si es un texto literal guardado
                            valor = str(simbolo.valor_inicial).strip('"').strip("'")
                            salida.append(valor)
                        else:
                            salida.append(f"<Error: {arg.lexema} no definido>")
                    elif arg.tipo_token in ['LITERAL_STRING', 'LITERAL_ENTERO', 'LITERAL_FLOTANTE', 'LITERAL_BOOLEANO', 'LITERAL_CHAR']:
                        valor = arg.lexema.strip('"').strip("'")
                        salida.append(valor)
            indice += 1
            
        return "\n".join(salida) if salida else "Compilación exitosa. El programa finalizó sin salidas a consola (Código de salida: 0)."
