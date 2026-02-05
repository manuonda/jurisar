"""
Script para procesar un fallo judicial con Anthropic (Haiku 3.5), OpenAI (GPT-4o mini) y Kimi 2.5
y comparar las salidas JSON de los proveedores.

Uso:
    .venv/bin/python procesar_fallo.py fallos/fallo1.pdf
"""
import sys
import json
import time
import pypdf
from dotenv import load_dotenv

load_dotenv()

from core.services.ia_service import IAService


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """Extrae texto de un PDF."""
    reader = pypdf.PdfReader(ruta_pdf)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"
    return texto


def mostrar_resultado(datos: dict):
    """Muestra el resultado de un proveedor de forma legible."""
    print(f"  Modelo:        {datos['modelo']}")
    print(f"  Input tokens:  {datos['uso']['input_tokens']:,}")
    print(f"  Output tokens: {datos['uso']['output_tokens']:,}")
    print()
    print(json.dumps(datos["resultado"], indent=2, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        print("Uso: .venv/bin/python procesar_fallo.py <ruta_pdf>")
        sys.exit(1)

    ruta_pdf = sys.argv[1]

    # 1. Extraer texto
    print(f"Extrayendo texto de: {ruta_pdf}")
    texto = extraer_texto_pdf(ruta_pdf)
    print(f"  Caracteres: {len(texto):,}")
    print(f"  Palabras:   {len(texto.split()):,}")
    print()

    # 2. Inicializar servicio
    servicio = IAService()

    # 3. Procesar con Anthropic
    print("=" * 60)
    print("ANTHROPIC - Claude Haiku 3.5")
    print("=" * 60)
    inicio = time.time()
    try:
        res_anthropic = servicio.analizar_fallo_anthropic(texto)
        tiempo_anthropic = time.time() - inicio
        print(f"  Tiempo:        {tiempo_anthropic:.2f}s")
        mostrar_resultado(res_anthropic)
    except Exception as e:
        print(f"  ERROR: {e}")
        res_anthropic = None
        tiempo_anthropic = 0

    print()

    # 4. Procesar con OpenAI
    print("=" * 60)
    print("OPENAI - GPT-4o mini")
    print("=" * 60)
    inicio = time.time()
    try:
        res_openai = servicio.analizar_fallo_openai(texto)
        tiempo_openai = time.time() - inicio
        print(f"  Tiempo:        {tiempo_openai:.2f}s")
        mostrar_resultado(res_openai)
    except Exception as e:
        print(f"  ERROR: {e}")
        res_openai = None
        tiempo_openai = 0

    print()

    # 5. Procesar con Kimi (Moonshot)
    print("=" * 60)
    print("MOONSHOT - Kimi 2.5")
    print("=" * 60)
    inicio = time.time()
    try:
        res_kimi = servicio.analizar_fallo_kimi(texto)
        tiempo_kimi = time.time() - inicio
        print(f"  Tiempo:        {tiempo_kimi:.2f}s")
        mostrar_resultado(res_kimi)
    except Exception as e:
        print(f"  ERROR: {e}")
        res_kimi = None
        tiempo_kimi = 0

    # 6. Comparativa
    resultados = []
    if res_anthropic:
        resultados.append(("Anthropic", res_anthropic, tiempo_anthropic))
    if res_openai:
        resultados.append(("OpenAI", res_openai, tiempo_openai))
    if res_kimi:
        resultados.append(("Kimi", res_kimi, tiempo_kimi))

    if len(resultados) >= 2:
        print()
        print("=" * 60)
        print("COMPARATIVA")
        print("=" * 60)

        # Precios por MTok (input/output):
        # Haiku 3.5 = $0.80/$4.00
        # GPT-4o mini = $0.15/$0.60
        # Kimi 2.5 (moonshot-v1-8k) = $0.012/$0.012 (aprox, verificar precios actuales)
        precios = {
            "Anthropic": {"input": 0.80, "output": 4.00},
            "OpenAI": {"input": 0.15, "output": 0.60},
            "Kimi": {"input": 0.012, "output": 0.012},  # Precios aproximados, verificar
        }

        # Calcular costos
        costos = {}
        for nombre, res, tiempo in resultados:
            precio = precios.get(nombre, {"input": 0, "output": 0})
            costo = (
                (res["uso"]["input_tokens"] / 1_000_000) * precio["input"]
                + (res["uso"]["output_tokens"] / 1_000_000) * precio["output"]
            )
            costos[nombre] = costo

        # Encabezado de tabla
        headers = [nombre for nombre, _, _ in resultados]
        header_line = f"{'':>20}"
        separator_line = f"{'-'*20}"
        for h in headers:
            header_line += f" {h:>15}"
            separator_line += f" {'-'*15}"
        print(header_line)
        print(separator_line)

        # Modelo
        modelo_line = f"{'Modelo':>20}"
        for nombre, res, _ in resultados:
            modelo = res['modelo'][:15] if len(res['modelo']) <= 15 else res['modelo'][:12] + "..."
            modelo_line += f" {modelo:>15}"
        print(modelo_line)

        # Input tokens
        tokens_in_line = f"{'Input tokens':>20}"
        for nombre, res, _ in resultados:
            tokens_in_line += f" {res['uso']['input_tokens']:>15,}"
        print(tokens_in_line)

        # Output tokens
        tokens_out_line = f"{'Output tokens':>20}"
        for nombre, res, _ in resultados:
            tokens_out_line += f" {res['uso']['output_tokens']:>15,}"
        print(tokens_out_line)

        # Tiempo
        tiempo_line = f"{'Tiempo':>20}"
        for nombre, res, tiempo in resultados:
            tiempo_line += f" {tiempo:>14.2f}s"
        print(tiempo_line)

        # Costo por fallo
        costo_line = f"{'Costo/fallo':>20}"
        for nombre, res, _ in resultados:
            costo_line += f" ${costos[nombre]:>13.6f}"
        print(costo_line)

        # Costo x 300K
        costo_300k_line = f"{'Costo x 300K':>20}"
        for nombre, res, _ in resultados:
            costo_300k_line += f" ${costos[nombre] * 300_000:>12,.2f}"
        print(costo_300k_line)

        # Costo x 300K Batch (solo Anthropic tiene descuento batch)
        if res_anthropic:
            costo_batch_line = f"{'Costo x 300K Batch':>20}"
            for nombre, res, _ in resultados:
                if nombre == "Anthropic":
                    costo_batch_line += f" ${costos[nombre] * 300_000 * 0.5:>12,.2f}"
                else:
                    costo_batch_line += f" {'N/A':>14}"
            print(costo_batch_line)


if __name__ == "__main__":
    main()
