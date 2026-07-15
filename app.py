import streamlit as st
import pandas as pd
import re
from streamlit_ace import st_ace  # Editor con números de línea
from MiniCompilador.Lenguajes.Lenguaje_Propio import ReglasLenguajePropio
from MiniCompilador.Lenguajes.cpp import ReglasCpp
from MiniCompilador.Lenguajes.c_puro import ReglasC
from MiniCompilador.Lenguajes.go_lang import ReglasGo
from MiniCompilador.src.Analizador_Lexico import AnalizadorLexico
from MiniCompilador.src.Analizador_Sintactico import AnalizadorSintactico
from MiniCompilador.src.Tabla_simbolos import TablaSimbolos
from MiniCompilador.src.Ejecutor import EjecutorSimulado  # <--- NUEVA IMPORTACIÓN DE TU MÓDULO

# --- CLASE AUXILIAR: PREPROCESADOR ---
class Preprocesador:
    """Clase encargada de limpiar cabeceras, imports y envolturas de funciones principales
    manteniendo la consistencia de los números de línea reales."""
    @staticmethod
    def preprocesar(codigo: str, nombre_lenguaje: str) -> str:
        lineas = codigo.split('\n')
        lineas_filtradas = []
        
        # Patrones para identificar directivas de importación, paquetes, namespaces e includes
        patrones_ignorar = [
            r'^\s*#include',
            r'^\s*using\s+namespace',
            r'^\s*package\s+',
            r'^\s*import\s+'
        ]
        
        for linea in lineas:
            linea_strip = linea.strip()
            
            # 1. Conservar comentarios vacíos o líneas vacías como saltos de línea para no perder el índice
            if not linea_strip:
                lineas_filtradas.append("")
                continue
            
            # 2. Comentarios de línea completa (se reemplazan por vacío para mantener la línea)
            if linea_strip.startswith('//') or linea_strip.startswith('#'):
                lineas_filtradas.append("")
                continue
            
            # 3. Omitir directivas reemplazándolas por una línea vacía
            if any(re.match(patron, linea) for patron in patrones_ignorar):
                lineas_filtradas.append("")
                continue
                
            # 4. Omitir cabecera de función main()
            if 'main()' in linea or 'func main()' in linea:
                lineas_filtradas.append("")
                continue
                
            lineas_filtradas.append(linea)
            
        # Reconstruir el código temporalmente
        codigo_limpio = '\n'.join(lineas_filtradas)
        
        # 5. Remover llave de cierre externa '}' de funciones principales sin alterar el contador de líneas
        pos_ultima_llave = codigo_limpio.rfind('}')
        if pos_ultima_llave != -1:
            codigo_limpio = codigo_limpio[:pos_ultima_llave] + " " + codigo_limpio[pos_ultima_llave+1:]
            
        return codigo_limpio


# Configuración del entorno e interfaz
st.set_page_config(page_title="Mini Compilador Académico", layout="wide", page_icon="🎛️")
st.title("🎛️ Mini Compilador - IS913")
st.subheader("Diseño de Compiladores | Ingeniería en Sistemas")

# Barra lateral para seleccionar el Lenguaje
st.sidebar.header("Configuración del Sistema")
opcion_lenguaje = st.sidebar.selectbox(
    "Seleccione el Lenguaje a Compilar:",
    ["Lenguaje Propio", "Subconjunto C++", "Subconjunto C", "Subconjunto Go"]
)

# Inyección dinámica de reglas y código de ejemplo (Hola Mundo real) según la selección
if opcion_lenguaje == "Lenguaje Propio":
    reglas = ReglasLenguajePropio()
    codigo_ejemplo = (
        '// Mi primer programa en Lenguaje Propio\n'
        'texto saludo = "¡Hola Mundo!";\n'
        'mostrar(saludo);\n'
    )
elif opcion_lenguaje == "Subconjunto C++":
    reglas = ReglasCpp()
    codigo_ejemplo = (
        '#include <iostream>\n'
        '#include <string>\n'
        'using namespace std;\n\n'
        'int main() {\n'
        '    // Mi primer programa en C++\n'
        '    string saludo = "¡Hola Mundo!";\n'
        '    print(saludo);\n'
        '}'
    )
elif opcion_lenguaje == "Subconjunto C":
    reglas = ReglasC()
    codigo_ejemplo = (
        '#include <stdio.h>\n\n'
        'int main() {\n'
        '    // Mi primer programa en C\n'
        '    string saludo = "¡Hola Mundo!";\n'
        '    printf(saludo);\n'
        '}'
    )
else:  # Subconjunto Go
    reglas = ReglasGo()
    codigo_ejemplo = (
        'package main\n'
        'import "fmt"\n\n'
        'func main() {\n'
        '    // Mi primer programa en Go\n'
        '    string saludo = "¡Hola Mundo!";\n'
        '    fmt.Println(saludo);\n'
        '}'
    )

st.sidebar.info(f"⚙️ **Modo Activo:** {reglas.NOMBRE}")

# Área de entrada para el código fuente con editor profesional
st.markdown("### Código Fuente de Entrada")

codigo_usuario = st_ace(
    value=codigo_ejemplo,
    language="c_cpp" if opcion_lenguaje != "Subconjunto Go" else "golang",
    theme="monokai",
    height=320,
    font_size=14,
    tab_size=4,
    show_gutter=True,      # Muestra los números de línea reales
    show_print_margin=False,
    wrap=True,
    key=f"editor_compilador_{opcion_lenguaje}" 
)

# Botón principal de compilación
if st.button("🚀 Ejecutar Análisis Multilenguaje"):
    if not codigo_usuario.strip():
        st.warning("Por favor, ingrese algún código antes de compilar.")
    else:
        # FASE 0: Preprocesar conservando la concordancia de líneas
        codigo_preprocesado = Preprocesador.preprocesar(codigo_usuario, reglas.NOMBRE)
        
        # 1. Inicializar componentes lógicos (POO)
        tabla_simbolos = TablaSimbolos()
        lexer = AnalizadorLexico(reglas)
        
        # 2. Fase 1: Análisis Léxico sobre el código preprocesado
        tokens = lexer.tokenizar(codigo_preprocesado)
        
        # 3. Fase 2 y 3: Análisis Sintáctico y Semántico Integrado
        parser = AnalizadorSintactico(tokens, tabla_simbolos, reglas)
        parser.analizar()
        
        # Consolidación total de errores de todas las fases (Léxico + Sintáctico/Semántico)
        todos_los_errores = lexer.errores + parser.errores
        
        # Creación de pestañas ordenadas para el reporte académico
        tab_lexico, tab_simbolos, tab_diagnostico = st.tabs([
            "📊 Analizador Léxico (Tokens)", 
            "🗂️ Tabla de Símbolos", 
            "🛡️ Asistente de Errores y Diagnóstico"
        ])
        
        # PESTAÑA 1: TOKENS
        with tab_lexico:
            st.markdown("#### Componentes Léxicos Identificados")
            if tokens:
                filas_tokens = [t.a_fila_tabla() for t in tokens]
                st.dataframe(pd.DataFrame(filas_tokens), use_container_width=True)
            else:
                st.info("No se generaron tokens válidos.")
                
        # PESTAÑA 2: TABLA DE SÍMBOLOS
        with tab_simbolos:
            st.markdown("#### Registro de Variables en Memoria")
            if tabla_simbolos.simbolos:
                filas_simbolos = [s.a_diccionario() for s in tabla_simbolos.simbolos.values()]
                st.dataframe(pd.DataFrame(filas_simbolos), use_container_width=True)
            else:
                st.info("La tabla de símbolos está vacía (no hay declaraciones válidas correctas).")
                
        # PESTAÑA 3: DIAGNÓSTICO
        with tab_diagnostico:
            st.markdown("#### Reporte de Estado Final")
            if not todos_los_errores:
                st.success("🎉 ¡Compilación Exitosa! El código fuente no presenta anomalías léxicas, sintácticas ni semánticas.")
                
                # SIMULACIÓN DE CONSOLA DE SALIDA (Uso de la clase externa importada)
                st.markdown("### 🖥️ Consola de Salida")
                consola_output = EjecutorSimulado.ejecutar(tokens, tabla_simbolos, reglas)
                st.code(consola_output, language="text")
            else:
                st.error(f"❌ Se detectaron {len(todos_los_errores)} errores en el código fuente:")
                filas_errores = [e.a_fila_tabla() for e in todos_los_errores]
                st.table(pd.DataFrame(filas_errores))
