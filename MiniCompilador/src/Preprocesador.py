import re

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
        
        # 5. Para remover la llave de cierre externa '}' del main() sin alterar su línea,
        # buscamos la última llave de cierre no vacía y la reemplazamos por un espacio en blanco.
        pos_ultima_llave = codigo_limpio.rfind('}')
        if pos_ultima_llave != -1:
            # Reemplazar únicamente el carácter '}' por un espacio en blanco ' '
            codigo_limpio = codigo_limpio[:pos_ultima_llave] + " " + codigo_limpio[pos_ultima_llave+1:]
            
        return codigo_limpio
