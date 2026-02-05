"""
Ejemplo de cómo usar utils.py e ia_service.py juntos
"""
from pathlib import Path
from core.utils import leer_archivo, descargar_y_leer_pdf, validar_archivo
from core.services.ia_service import IAService


def ejemplo_procesar_archivo_local():
    """Ejemplo: Procesar un archivo local"""
    print("📄 Ejemplo 1: Procesar archivo local")
    print("-" * 60)
    
    # 1. Leer el archivo usando utils
    ruta_archivo = "fallos/fallo1.pdf"
    
    try:
        # Validar primero
        info = validar_archivo(ruta_archivo)
        if not info["es_valido"]:
            print(f"❌ Archivo no válido: {ruta_archivo}")
            return
        
        # Leer el contenido
        texto = leer_archivo(ruta_archivo)
        print(f"✅ Archivo leído: {len(texto)} caracteres")
        
        # 2. Procesar con IA
        servicio_ia = IAService()
        resultado = servicio_ia.analizar_fallo(texto)
        
        print(f"✅ Análisis completado")
        print(f"   Materia: {resultado.get('materia')}")
        print(f"   Etiquetas: {len(resultado.get('etiquetas', []))}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_procesar_pdf_local():
    """Ejemplo: Procesar un PDF local"""
    print("\n📄 Ejemplo 2: Procesar PDF local")
    print("-" * 60)
    
    ruta_pdf = "fallo_ejemplo.pdf"
    
    try:
        # Leer PDF
        texto = leer_archivo(ruta_pdf)
        print(f"✅ PDF leído: {len(texto)} caracteres")
        
        # Procesar con IA
        servicio_ia = IAService()
        resultado = servicio_ia.analizar_fallo(texto)
        
        print(f"✅ Análisis completado")
        print(f"   Materia: {resultado.get('materia')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_descargar_y_procesar():
    """Ejemplo: Descargar PDF desde URL y procesarlo"""
    print("\n📄 Ejemplo 3: Descargar y procesar desde URL")
    print("-" * 60)
    
    url_pdf = "https://ejemplo.com/fallo.pdf"
    
    try:
        # Descargar y leer PDF directamente
        texto = descargar_y_leer_pdf(url_pdf, guardar_local=False)
        print(f"✅ PDF descargado y leído: {len(texto)} caracteres")
        
        # Procesar con IA
        servicio_ia = IAService()
        resultado = servicio_ia.analizar_fallo(texto)
        
        print(f"✅ Análisis completado")
        print(f"   Materia: {resultado.get('materia')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_flujo_completo(ruta_o_url: str):
    """
    Flujo completo: validar -> leer -> procesar
    
    Args:
        ruta_o_url: Puede ser una ruta local o una URL
    """
    print(f"\n🔄 Flujo completo: {ruta_o_url}")
    print("-" * 60)
    
    try:
        # 1. Determinar si es URL o archivo local
        es_url = ruta_o_url.startswith(('http://', 'https://'))
        
        # 2. Obtener texto
        if es_url:
            print("📥 Descargando desde URL...")
            texto = descargar_y_leer_pdf(ruta_o_url)
        else:
            print("📖 Leyendo archivo local...")
            texto = leer_archivo(ruta_o_url)
        
        print(f"✅ Texto obtenido: {len(texto)} caracteres")
        
        # 3. Procesar con IA
        print("🤖 Procesando con Claude...")
        servicio_ia = IAService()
        resultado = servicio_ia.analizar_fallo(texto)
        
        # 4. Mostrar resultados
        print("\n📊 RESULTADOS:")
        print(f"   Materia: {resultado.get('materia')}")
        print(f"   Tipo: {resultado.get('tipo_proceso')}")
        print(f"   Resultado: {resultado.get('resultado')}")
        print(f"   Etiquetas: {len(resultado.get('etiquetas', []))}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    # Ejecutar ejemplos
    ejemplo_procesar_archivo_local()
    # ejemplo_procesar_pdf_local()
    # ejemplo_descargar_y_procesar()
    
    # Ejemplo de uso práctico
    # resultado = ejemplo_flujo_completo("fallo.txt")
    # resultado = ejemplo_flujo_completo("https://ejemplo.com/fallo.pdf")