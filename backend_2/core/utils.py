"""
Utilidades para manejo de archivos y descargas
- Lectura de archivos PDF y texto
- Descarga de archivos desde URLs
- Conversión de formatos
"""
import os
import requests
from pathlib import Path
from typing import Union, Optional
from urllib.parse import urlparse


def leer_archivo_texto(ruta_archivo: Union[str, Path]) -> str:
    """
    Lee el contenido de un archivo de texto (.txt)
    
    Args:
        ruta_archivo: Ruta al archivo de texto
        
    Returns:
        Contenido del archivo como string
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no es de tipo texto o está vacío
    """
    ruta = Path(ruta_archivo)
    
    if not ruta.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")
    
    # Verificar extensión
    extension = ruta.suffix.lower()
    if extension not in ['.txt', '.text']:
        raise ValueError(f"Formato no soportado: {extension}. Solo se soportan archivos .txt")
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        if not contenido.strip():
            raise ValueError(f"El archivo está vacío: {ruta_archivo}")
        
        return contenido
    except UnicodeDecodeError:
        raise ValueError(f"Error al leer el archivo. Asegúrate de que esté en formato UTF-8: {ruta_archivo}")


def leer_archivo_pdf(ruta_archivo: Union[str, Path]) -> str:
    """
    Lee el contenido de un archivo PDF y extrae el texto
    
    Args:
        ruta_archivo: Ruta al archivo PDF
        
    Returns:
        Texto extraído del PDF
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ImportError: Si no están instaladas las librerías necesarias
        ValueError: Si el PDF está vacío o no se puede leer
    """
    ruta = Path(ruta_archivo)
    
    if not ruta.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")
    
    # Intentar con pdfplumber primero (mejor calidad de extracción)
    try:
        import pdfplumber
        texto_completo = []
        with pdfplumber.open(ruta) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo.append(texto)
        
        texto_final = "\n".join(texto_completo)
        if not texto_final.strip():
            raise ValueError(f"No se pudo extraer texto del PDF: {ruta_archivo}")
        
        return texto_final
        
    except ImportError:
        # Fallback a PyPDF2
        try:
            import PyPDF2
            texto_completo = []
            with open(ruta, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for pagina in pdf_reader.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(texto)
            
            texto_final = "\n".join(texto_completo)
            if not texto_final.strip():
                raise ValueError(f"No se pudo extraer texto del PDF: {ruta_archivo}")
            
            return texto_final
            
        except ImportError:
            raise ImportError(
                "Para leer PDFs necesitas instalar una de estas librerías:\n"
                "  pip install pdfplumber  (recomendado)\n"
                "  o\n"
                "  pip install PyPDF2"
            )


def leer_archivo(ruta_archivo: Union[str, Path]) -> str:
    """
    Lee un archivo y extrae su contenido según su formato
    
    Soporta:
    - Archivos de texto: .txt, .text
    - Archivos PDF: .pdf
    
    Args:
        ruta_archivo: Ruta al archivo
        
    Returns:
        Contenido del archivo como texto
        
    Raises:
        ValueError: Si el formato no está soportado
    """
    ruta = Path(ruta_archivo)
    extension = ruta.suffix.lower()
    
    if extension == '.pdf':
        return leer_archivo_pdf(ruta)
    elif extension in ['.txt', '.text']:
        return leer_archivo_texto(ruta)
    else:
        raise ValueError(
            f"Formato no soportado: {extension}\n"
            f"Formatos soportados: .txt, .pdf"
        )


def descargar_pdf_desde_url(url: str, ruta_destino: Optional[Union[str, Path]] = None) -> str:
    """
    Descarga un archivo PDF desde una URL y lo guarda localmente
    
    Args:
        url: URL del archivo PDF a descargar
        ruta_destino: Ruta donde guardar el archivo. Si es None, se guarda en /tmp
        
    Returns:
        Ruta al archivo descargado
        
    Raises:
        ValueError: Si la URL no es válida o no apunta a un PDF
        requests.RequestException: Si hay error al descargar
    """
    # Validar URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"URL inválida: {url}")
    
    # Verificar que sea PDF (por extensión o Content-Type)
    es_pdf = url.lower().endswith('.pdf')
    
    # Descargar el archivo
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Verificar Content-Type si no es obvio por la URL
        content_type = response.headers.get('Content-Type', '').lower()
        if not es_pdf and 'pdf' not in content_type:
            raise ValueError(f"La URL no apunta a un archivo PDF: {url}")
        
        # Determinar ruta de destino
        if ruta_destino is None:
            # Extraer nombre del archivo de la URL o generar uno
            nombre_archivo = os.path.basename(parsed.path) or "descargado.pdf"
            if not nombre_archivo.endswith('.pdf'):
                nombre_archivo += '.pdf'
            ruta_destino = Path("/tmp") / nombre_archivo
        else:
            ruta_destino = Path(ruta_destino)
        
        # Crear directorio si no existe
        ruta_destino.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar el archivo
        with open(ruta_destino, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return str(ruta_destino)
        
    except requests.RequestException as e:
        raise ValueError(f"Error al descargar el archivo desde {url}: {e}")


def descargar_y_leer_pdf(url: str, guardar_local: bool = False) -> str:
    """
    Descarga un PDF desde URL y extrae su texto directamente
    
    Args:
        url: URL del archivo PDF
        guardar_local: Si True, guarda el archivo localmente. Si False, lo descarga temporalmente
        
    Returns:
        Texto extraído del PDF
        
    Raises:
        ValueError: Si hay error al descargar o leer el PDF
    """
    # Descargar el PDF
    if guardar_local:
        # Guardar en directorio actual
        nombre_archivo = os.path.basename(urlparse(url).path) or "descargado.pdf"
        ruta_archivo = descargar_pdf_desde_url(url, nombre_archivo)
    else:
        # Guardar temporalmente
        ruta_archivo = descargar_pdf_desde_url(url)
    
    try:
        # Leer el PDF
        texto = leer_archivo_pdf(ruta_archivo)
        
        # Si no se guardó localmente, eliminar el archivo temporal
        if not guardar_local:
            Path(ruta_archivo).unlink()
        
        return texto
    except Exception as e:
        # Si falla, intentar limpiar el archivo temporal
        if not guardar_local and Path(ruta_archivo).exists():
            Path(ruta_archivo).unlink()
        raise


def validar_archivo(ruta_archivo: Union[str, Path]) -> dict:
    """
    Valida que un archivo exista y sea del formato correcto
    
    Args:
        ruta_archivo: Ruta al archivo a validar
        
    Returns:
        Dict con información del archivo:
        {
            "existe": bool,
            "formato": str,
            "tamaño": int (bytes),
            "es_valido": bool
        }
    """
    ruta = Path(ruta_archivo)
    
    resultado = {
        "existe": ruta.exists(),
        "formato": ruta.suffix.lower() if ruta.exists() else None,
        "tamaño": ruta.stat().st_size if ruta.exists() else 0,
        "es_valido": False
    }
    
    if resultado["existe"]:
        formato = resultado["formato"]
        resultado["es_valido"] = formato in ['.txt', '.text', '.pdf']
    
    return resultado