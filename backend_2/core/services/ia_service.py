"""
Servicio para análisis de fallos judiciales con Claude API
Solo se encarga de procesar texto con IA, no maneja archivos
"""
import json
import os
import anthropic
from typing import Optional

from core.prompts import SYSTEM_PROMPT, generar_prompt_usuario

# Modelo de Claude a usar
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")


class IAService:
    """Servicio que conecta con Claude para analizar fallos judiciales."""
    
    def __init__(self):
        # Verificar que existe la API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no está configurada en las variables de entorno")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = CLAUDE_MODEL
    
    def analizar_fallo(self, texto_fallo: str, etiquetas: Optional[list[str]] = None) -> dict:
        """
        Analiza un fallo judicial usando Claude y devuelve el análisis estructurado
        
        Args:
            texto_fallo: Texto completo del fallo judicial a analizar
            etiquetas: Lista opcional de etiquetas oficiales. Si es None, usa las bases
        
        Returns:
            Dict con el análisis estructurado:
            {
                "resumen": str,
                "materia": str,
                "tipo_proceso": str,
                "resultado": str,
                "etiquetas": list[dict],
                "normativa_clave": list[str],
                "partes": dict
            }
            
        Raises:
            ValueError: Si el texto está vacío o hay error al procesar
        """
        # Validar que el texto no esté vacío
        if not texto_fallo or not texto_fallo.strip():
            raise ValueError("El texto del fallo está vacío")
        
        # Generar el prompt del usuario con el texto del fallo
        prompt_usuario = generar_prompt_usuario(texto_fallo, etiquetas)
        
        # Llamar a Claude con el system prompt y el prompt del usuario
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_usuario
                    }
                ]
            )
            
            # Extraer el texto de la respuesta
            respuesta_texto = response.content[0].text
            
            # Parsear el JSON de la respuesta
            return self._parsear_respuesta_json(respuesta_texto)
            
        except anthropic.APIError as e:
            raise ValueError(f"Error de la API de Claude: {e}")
        except Exception as e:
            raise ValueError(f"Error al procesar el fallo: {e}")
    
    def _parsear_respuesta_json(self, respuesta: str) -> dict:
        """
        Extrae y parsea el JSON de la respuesta de Claude.
        Maneja casos donde Claude envuelve el JSON en markdown.
        
        Args:
            respuesta: Texto de respuesta de Claude
            
        Returns:
            Dict parseado del JSON
            
        Raises:
            ValueError: Si no se puede parsear el JSON
        """
        # Limpiar posibles markdown
        limpio = respuesta.replace("", "").replace("```", "").strip()
        
        try:
            return json.loads(limpio)
        except json.JSONDecodeError:
            # Si falla, intentar extraer solo el JSON del texto
            inicio = limpio.find("{")
            fin = limpio.rfind("}") + 1
            if inicio >= 0 and fin > inicio:
                try:
                    return json.loads(limpio[inicio:fin])
                except json.JSONDecodeError:
                    pass
            
            raise ValueError("No se pudo parsear la respuesta de Claude como JSON")
    
    def etiquetar_fallo(self, texto_fallo: str, etiquetas: Optional[list[str]] = None) -> dict:
        """
        Alias para analizar_fallo (mantiene compatibilidad con código anterior)
        
        Args:
            texto_fallo: Texto completo del fallo judicial
            etiquetas: Lista opcional de etiquetas oficiales
            
        Returns:
            Dict con el análisis estructurado
        """
        return self.analizar_fallo(texto_fallo, etiquetas)