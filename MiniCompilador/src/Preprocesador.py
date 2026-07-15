import re

class Preprocesador:
    """Clase encargada de limpiar cabeceras, imports y envolturas de funciones principales 
    para dejar únicamente el cuerpo de instrucciones ejecutable."""
    
    @staticmethod
    def preprocesar(codigo: str, nombre_lenguaje: str) -> str:
        lineas = codigo.split('\n')
        lineas_filtradas = []
        
        # Patrones para ignorar directivas de importación, paquetes y namespaces
        patrones_ignorar = [
            r'^\s*#include',
            r'^\s*using\s+namespace',
            r'^\s*package\s+',
            r'^\s*import\s+'
        ]
        
        for linea in lineas:
            # 1. Omitir líneas vacías o de comentarios simples
            if not linea.strip() or linea.strip().startswith('//'):
                continue
            
            # 2. Omitir directivas de preprocesador e importaciones
            if any(re.match(patron, linea) for patron in patrones_ignorar):
                continue
                
            # 3. Omitir las declaraciones de función principal (main)
            if 'main()' in linea or 'func main()' in linea:
                continue
                
            lineas_filtradas.append(linea)
            
        codigo_limpio = '\n'.join(lineas_filtradas)
        
        # 4. Quitar llaves de cierre huérfanas al final del archivo que pertenecían al main()
        # Buscamos la última llave de cierre '}' que queda tras remover el main
        codigo_limpio = codigo_limpio.strip()
        if codigo_limpio.endswith('}'):
            # Quitamos la última llave de cierre correspondiente a la envoltura del main
            codigo_limpio = codigo_limpio[:-1].strip()
            
        return codigo_limpio
