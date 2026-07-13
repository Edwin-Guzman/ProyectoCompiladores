# Mini Compilador Académico con Arquitectura Multilenguaje - IS913

Este proyecto consiste en el diseño e implementación de un Mini Compilador modular desarrollado en Python utilizando el paradigma de Programación Orientada a Objetos (POO). Cuenta con una interfaz gráfica interactiva web construida con Streamlit.

##  Características del Proyecto
- **Análisis Léxico:** Reconocimiento preciso de componentes léxicos mediante Expresiones Regulares (RegEx).
- **Análisis Sintáctico:** Parser predictivo implementado mediante algoritmos de Descenso Recursivo.
- **Análisis Semántico Integrado:** Gestión estricta de Tipado Fuerte y control dinámico de mutabilidad en variables.
- **Arquitectura Multilenguaje:** Capacidad en tiempo real para cambiar las reglas del compilador entre un Lenguaje Propio y un Subconjunto de C++.
- **Asistente Inteligente de Errores:** Panel de diagnóstico que no solo detecta el error y la línea, sino que provee una sugerencia pragmática de solución.

##  Estructura del Ecosistema
MiniCompilador/
│
├── src/                      # Lógica nuclear del compilador
│   ├── modelos.py            # Esquemas de datos (Token, Error)
│   ├── Tabla_simbolos.py     # Gestión de memoria y mutabilidad
│   ├── Validador_Tipado.py   # Control semántico de tipos
│   ├── Analizador_Lexico.py  # Componente analizador léxico
│   └── Analizador_Sintactico.py # Parser por descenso recursivo
│
├── Lenguajes/                # Configuración de los Alfabetos (Extra)
│   ├── reglas_base.py        # Clase base abstracta
│   ├── lenguaje_propio.py    # Reglas del Lenguaje Nativo
│   └── cpp.py                # Reglas del Subconjunto de C++
│
└── README.md                 # Documentación técnica