"""
Script de prueba para procesar fallo1.pdf con Claude 3.5 Haiku
Objetivo: Validar etiquetado de fallos con el modelo más económico
"""
import os
import time
import json
from pathlib import Path

# Configurar modelo ANTES de importar IAService
os.environ["CLAUDE_MODEL"] = "claude-3-5-haiku-20241022"

from core.utils import leer_archivo, validar_archivo
from core.services.ia_service import IAService


# Precios de Claude (USD por millón de tokens) - Enero 2025
PRECIOS = {
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
}


def estimar_tokens(texto: str) -> int:
    """Estimación aproximada de tokens (1 token ~ 4 caracteres en español)"""
    return len(texto) // 4


def calcular_costo(modelo: str, tokens_input: int, tokens_output: int) -> float:
    """Calcula el costo aproximado en USD"""
    precios = PRECIOS.get(modelo, PRECIOS["claude-3-5-haiku-20241022"])
    costo_input = (tokens_input / 1_000_000) * precios["input"]
    costo_output = (tokens_output / 1_000_000) * precios["output"]
    return costo_input + costo_output


def test_procesar_fallo_haiku():
    """
    Prueba el procesamiento de fallo1.pdf con Haiku
    Basado en ejemplo_procesar_archivo_local() de ejemplo_uso.py
    """
    print("=" * 70)
    print("TEST: Procesamiento de Fallo Judicial con Claude 3.5 Haiku")
    print("=" * 70)

    modelo = os.environ.get("CLAUDE_MODEL", "no configurado")
    print(f"\n[CONFIG] Modelo: {modelo}")

    ruta_archivo = "fallos/fallo1.pdf"

    # 1. Validar archivo
    print(f"\n[1/4] Validando archivo: {ruta_archivo}")
    info = validar_archivo(ruta_archivo)

    if not info["es_valido"]:
        print(f"   ERROR: Archivo no válido")
        return None

    print(f"   Formato: {info['formato']}")
    print(f"   Tamaño: {info['tamaño']:,} bytes")

    # 2. Leer contenido
    print(f"\n[2/4] Leyendo contenido del PDF...")
    try:
        texto = leer_archivo(ruta_archivo)
        tokens_input_estimados = estimar_tokens(texto)
        print(f"   Caracteres: {len(texto):,}")
        print(f"   Tokens estimados (input): ~{tokens_input_estimados:,}")
    except Exception as e:
        print(f"   ERROR al leer: {e}")
        return None

    # 3. Procesar con IA
    print(f"\n[3/4] Procesando con Claude 3.5 Haiku...")
    print("   Enviando solicitud a la API...")

    try:
        inicio = time.time()
        servicio_ia = IAService()
        resultado = servicio_ia.analizar_fallo(texto)
        tiempo_total = time.time() - inicio

        print(f"   Tiempo de respuesta: {tiempo_total:.2f} segundos")
    except Exception as e:
        print(f"   ERROR al procesar: {e}")
        return None

    # 4. Mostrar resultados
    print(f"\n[4/4] RESULTADOS DEL ANALISIS")
    print("-" * 70)

    # Información básica
    print(f"\n   MATERIA: {resultado.get('materia', 'N/A')}")
    print(f"   TIPO PROCESO: {resultado.get('tipo_proceso', 'N/A')}")
    print(f"   RESULTADO: {resultado.get('resultado', 'N/A')}")

    # Partes
    partes = resultado.get('partes', {})
    print(f"\n   PARTES:")
    print(f"     Actor: {partes.get('actor', 'N/A')}")
    print(f"     Demandado: {partes.get('demandado', 'N/A')}")

    # Resumen
    print(f"\n   RESUMEN:")
    resumen = resultado.get('resumen', 'N/A')
    # Dividir en líneas de 70 caracteres
    palabras = resumen.split()
    linea = "     "
    for palabra in palabras:
        if len(linea) + len(palabra) > 70:
            print(linea)
            linea = "     " + palabra
        else:
            linea += " " + palabra if linea.strip() else palabra
    if linea.strip():
        print(linea)

    # Etiquetas
    etiquetas = resultado.get('etiquetas', [])
    print(f"\n   ETIQUETAS ({len(etiquetas)}):")
    for et in etiquetas:
        nombre = et.get('nombre', 'N/A')
        tipo = et.get('tipo', 'N/A')
        relevancia = et.get('relevancia', 'N/A')
        print(f"     - {nombre} [{tipo}] ({relevancia})")

    # Normativa
    normativa = resultado.get('normativa_clave', [])
    print(f"\n   NORMATIVA CLAVE ({len(normativa)}):")
    for norma in normativa:
        print(f"     - {norma}")

    # Estimación de costos
    tokens_output_estimados = estimar_tokens(json.dumps(resultado))
    costo_estimado = calcular_costo(modelo, tokens_input_estimados, tokens_output_estimados)

    print(f"\n" + "=" * 70)
    print("ESTIMACION DE COSTOS")
    print("=" * 70)
    print(f"   Modelo usado: {modelo}")
    print(f"   Tokens input (estimado): ~{tokens_input_estimados:,}")
    print(f"   Tokens output (estimado): ~{tokens_output_estimados:,}")
    print(f"   Costo estimado: ${costo_estimado:.6f} USD")
    print(f"   Costo por 100 fallos: ~${costo_estimado * 100:.4f} USD")
    print(f"   Costo por 1000 fallos: ~${costo_estimado * 1000:.2f} USD")

    # Comparación con otros modelos
    print(f"\n   COMPARACION (mismo fallo con otros modelos):")
    for modelo_comp, precios in PRECIOS.items():
        costo_comp = calcular_costo(modelo_comp, tokens_input_estimados, tokens_output_estimados)
        ahorro = ((costo_comp - costo_estimado) / costo_comp * 100) if modelo_comp != modelo else 0
        marca = " <-- USADO" if modelo_comp == modelo else ""
        print(f"     {modelo_comp}: ${costo_comp:.6f} USD{marca}")

    # Guardar resultado en JSON
    output_file = "resultado_fallo1_haiku.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\n   Resultado guardado en: {output_file}")

    return resultado


def comparar_con_sonnet():
    """
    Opcional: Comparar resultado de Haiku vs Sonnet
    (Descomentar para ejecutar - aumenta costos)
    """
    print("\n" + "=" * 70)
    print("COMPARACION HAIKU vs SONNET")
    print("=" * 70)

    ruta_archivo = "fallos/fallo1.pdf"
    texto = leer_archivo(ruta_archivo)

    resultados = {}

    for modelo in ["claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022"]:
        print(f"\n[Procesando con {modelo}...]")
        os.environ["CLAUDE_MODEL"] = modelo

        inicio = time.time()
        servicio_ia = IAService()
        resultado = servicio_ia.analizar_fallo(texto)
        tiempo = time.time() - inicio

        resultados[modelo] = {
            "resultado": resultado,
            "tiempo": tiempo
        }
        print(f"   Tiempo: {tiempo:.2f}s")
        print(f"   Materia: {resultado.get('materia')}")
        print(f"   Etiquetas: {len(resultado.get('etiquetas', []))}")

    return resultados


if __name__ == "__main__":
    # Test principal con Haiku
    resultado = test_procesar_fallo_haiku()

    # Descomentar para comparar con Sonnet (aumenta costos)
    # comparar_con_sonnet()
