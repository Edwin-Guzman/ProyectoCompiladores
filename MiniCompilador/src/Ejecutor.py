class EjecutorSimulado:
    """Ejecuta las instrucciones del parser de manera secuencial para simular la consola."""
    @staticmethod
    def ejecutar(tokens: list, tabla_simbolos, reglas_lenguaje) -> str:
        salida = []
        indice = 0
        while indice < len(tokens):
            tok = tokens[indice]
            
            # Detectar la instrucción de impresión según las reglas del lenguaje activo
            if tok.lexema == reglas_lenguaje.PRINT:
                arg_tokens = []
                indice += 2  # Saltar el token de impresión y el paréntesis de apertura '('
                
                # Extraer todos los tokens que se encuentran dentro de los paréntesis
                while indice < len(tokens) and tokens[indice].lexema != ')':
                    arg_tokens.append(tokens[indice])
                    indice += 1
                
                # Procesar y traducir el contenido a imprimir
                for arg in arg_tokens:
                    if arg.tipo_token == 'IDENTIFICADOR':
                        simbolo = tabla_simbolos.buscar(arg.lexema)
                        if simbolo:
                            # Limpiar comillas del valor guardado en memoria
                            valor = str(simbolo.valor_inicial).strip('"').strip("'")
                            salida.append(valor)
                        else:
                            salida.append(f"<Error: Variable '{arg.lexema}' no inicializada>")
                    elif arg.tipo_token in ['LITERAL_STRING', 'LITERAL_ENTERO', 'LITERAL_FLOTANTE', 'LITERAL_BOOLEANO', 'LITERAL_CHAR']:
                        valor = arg.lexema.strip('"').strip("'")
                        salida.append(valor)
            indice += 1
            
        return "\n".join(salida) if salida else "Código ejecutado sin salidas a consola."
