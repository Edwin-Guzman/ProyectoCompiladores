import streamlit as st
import pandas as pd
from streamlit_ace import st_ace  # Nueva dependencia para el editor profesional
from MiniCompilador.Lenguajes.Lenguaje_Propio import ReglasLenguajePropio
from MiniCompilador.Lenguajes.cpp import ReglasCpp
from MiniCompilador.src.Analizador_Lexico import AnalizadorLexico
from MiniCompilador.src.Analizador_Sintactico import AnalizadorSintactico
from MiniCompilador.src.Tabla_simbolos import TablaSimbolos

# Configuración del entorno e interfaz
st.set_page_config(page_title="Mini Compilador Académico", layout="wide", page_icon="🎛️")
st.title("🎛️ Mini Compilador - IS913")
st.subheader("Diseño de Compiladores | Ingeniería en Sistemas")

# Barra lateral para seleccionar el Lenguaje
st.sidebar.header("Configuración del Sistema")
opcion_lenguaje = st.sidebar.selectbox(
    "Seleccione el Lenguaje a Compilar:",
    ["Lenguaje Propio", "Subconjunto C++"]
)

# Inyección dinámica de reglas según la selección del usuario
if opcion_lenguaje == "Lenguaje Propio":
    reglas = ReglasLenguajePropio()
else:
    reglas = ReglasCpp()

st.sidebar.info(f"⚙️ **Modo Activo:** {reglas.NOMBRE}")

# Área de entrada para el código fuente con editor profesional
st.markdown("### Código Fuente de Entrada")

codigo_ejemplo = (
    'int edad = 20;\n'
    'string nombre = "Edwin";\n'
    'if (edad > 18) {\n'
    '    print(nombre);\n'
    '}'
)

# Renderizado de Streamlit Ace (Gutter activa los números de línea automáticamente)
codigo_usuario = st_ace(
    value=codigo_ejemplo,
    language="c_cpp",
    theme="monokai",
    height=280,
    font_size=14,
    tab_size=4,
    show_gutter=True,      # Muestra los números de línea al lado izquierdo
    show_print_margin=False,
    wrap=True,
    key="editor_compilador"
)

# Botón principal de compilación
if st.button("🚀 Ejecutar Análisis Multilenguaje"):
    if not codigo_usuario.strip():
        st.warning("Por favor, ingrese algún código antes de compilar.")
    else:
        # 1. Inicializar componentes lógicos (POO)
        tabla_simbolos = TablaSimbolos()
        lexer = AnalizadorLexico(reglas)
        
        # 2. Fase 1: Análisis Léxico
        tokens = lexer.tokenizar(codigo_usuario)
        
        # 3. Fase 2 y 3: Análisis Sintáctico y Semántico Integrado
        parser = AnalizadorSintactico(tokens, tabla_simbolos, reglas)
        parser.analizar()
        
        # Consolidación total de errores de todas las fases
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
            else:
                st.error(f"❌ Se detectaron {len(todos_los_errores)} errores en el código fuente:")
                filas_errores = [e.a_fila_tabla() for e in todos_los_errores]
                st.table(pd.DataFrame(filas_errores))
