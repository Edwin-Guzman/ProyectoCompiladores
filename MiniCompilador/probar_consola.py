from Lenguajes.Lenguaje_Propio import ReglasLenguajePropio
from src.Analizador_Lexico import AnalizadorLexico
from src.Analizador_Sintactico import AnalizadorSintactico
from src.Tabla_simbolos import TablaSimbolos

def ejecutar_prueba():
    print("=== TEST DE CONTROL LOCAL DEL MINI COMPILADOR ===")
    
    # 1. Definir un código de prueba en tu Lenguaje Propio
    codigo_fuente = (
        'int edad = 20;\n'
        'precio = 100;\n'  # <-- Error Semántico: 'precio' no ha sido declarado
        'if (edad > 18) {\n'
        '    print(edad);\n'
        '}'
    )
    
    print("\n[1] Código fuente a procesar:")
    print("-" * 40)
    print(codigo_fuente)
    print("-" * 40)

    # 2. Instanciar los módulos lógicos (POO)
    reglas = ReglasLenguajePropio()
    tabla_simbolos = TablaSimbolos()
    lexer = AnalizadorLexico(reglas)
    
    # 3. Fase 1: Análisis Léxico
    print("\n[2] Ejecutando Analizador Léxico...")
    tokens = lexer.tokenizar(codigo_fuente)
    
    # 4. Fase 2 y 3: Análisis Sintáctico y Semántico
    print("[3] Ejecutando Analizador Sintáctico y Semántico...")
    parser = AnalizadorSintactico(tokens, tabla_simbolos, reglas)
    parser.analizar()
    
    # 5. Recopilar Errores
    todos_los_errores = lexer.errores + parser.errores
    
    # --- DESPLEGAR RESULTADOS EN CONSOLA ---
    
    print("\n" + "="*20 + " REPORTE FINAL " + "="*20)
    
    # Mostrar Lista de Tokens
    print(f"\n✔️ Tokens identificados ({len(tokens)}):")
    for tok in tokens:
        print(f"   Línea {tok.linea} | Tipo: {tok.tipo_token:<20} | Lexema: '{tok.lexema}'")
        
    # Mostrar Tabla de Símbolos (Memoria)
    print("\n🗂️ Tabla de Símbolos Registrada:")
    if tabla_simbolos.simbolos:
        for nombre, sim in tabla_simbolos.simbolos.items():
            info = sim.a_diccionario()
            print(f"   • Variable: {info['Símbolo']:<8} | Tipo: {info['Tipo de dato']:<6} | "
                  f"Valor Inicial: {info['Valor inicial']:<8} | ¿Se modifica?: {info['¿Se modifica posteriormente?']}")
    else:
        print("   (Vacía - No hay variables declaradas con éxito)")

    # Mostrar Diagnóstico de Errores
    print("\n🛡️ Diagnóstico de Errores:")
    if not todos_los_errores:
        print("   🎉 ¡ÉXITO! El código no presenta errores léxicos, sintácticos ni semánticos.")
    else:
        print(f"   ❌ Se detectaron {len(todos_los_errores)} anomalías:")
        for err in todos_los_errores:
            info_err = err.a_fila_tabla()
            print(f"     - [{info_err['Fase / Tipo']}] Línea {err.linea}: {info_err['Mensaje de Error']}")
            print(f"       Sugerencia: {info_err['Solucion Sugerida']}")
            
    print("\n" + "=" * 55)

if __name__ == "__main__":
    ejecutar_prueba()