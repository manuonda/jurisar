"""
Servicio para análisis de fallos judiciales con IA (Anthropic y OpenAI)
Solo se encarga de procesar texto con IA, no maneja archivos
"""
import json
import os
import anthropic
import openai
from typing import Optional

from core.prompts import SYSTEM_PROMPT, generar_prompt_usuario

# Modelos
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class IAService:
    """Servicio que conecta con Anthropic y OpenAI para analizar fallos judiciales."""

    def __init__(self):
        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY no está configurada en las variables de entorno")
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        self.anthropic_model = ANTHROPIC_MODEL

        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno")
        self.openai_client = openai.OpenAI(api_key=openai_key)
        self.openai_model = OPENAI_MODEL

    def analizar_fallo_anthropic(self, texto_fallo: str, etiquetas: Optional[list[str]] = None) -> dict:
        """
        Analiza un fallo judicial usando Claude (Haiku 3.5)

        Args:
            texto_fallo: Texto completo del fallo judicial
            etiquetas: Lista opcional de etiquetas oficiales

        Returns:
            Dict con análisis estructurado y métricas de uso
        """
        if not texto_fallo or not texto_fallo.strip():
            raise ValueError("El texto del fallo está vacío")

        prompt_usuario = generar_prompt_usuario(texto_fallo, etiquetas)

        try:
            response = self.anthropic_client.messages.create(
                model=self.anthropic_model,
                max_tokens=2000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt_usuario}]
            )

            respuesta_texto = response.content[0].text
            resultado = self._parsear_respuesta_json(respuesta_texto)

            return {
                "provider": "anthropic",
                "modelo": response.model,
                "resultado": resultado,
                "uso": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                }
            }

        except anthropic.APIError as e:
            raise ValueError(f"Error de la API de Anthropic: {e}")

    def analizar_fallo_openai(self, texto_fallo: str, etiquetas: Optional[list[str]] = None) -> dict:
        """
        Analiza un fallo judicial usando OpenAI (GPT-4o mini)

        Args:
            texto_fallo: Texto completo del fallo judicial
            etiquetas: Lista opcional de etiquetas oficiales

        Returns:
            Dict con análisis estructurado y métricas de uso
        """
        if not texto_fallo or not texto_fallo.strip():
            raise ValueError("El texto del fallo está vacío")

        prompt_usuario = generar_prompt_usuario(texto_fallo, etiquetas)

        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_usuario}
                ]
            )

            respuesta_texto = response.choices[0].message.content
            resultado = self._parsear_respuesta_json(respuesta_texto)

            return {
                "provider": "openai",
                "modelo": response.model,
                "resultado": resultado,
                "uso": {
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens,
                }
            }

        except openai.APIError as e:
            raise ValueError(f"Error de la API de OpenAI: {e}")

    def _parsear_respuesta_json(self, respuesta: str) -> dict:
        """
        Extrae y parsea el JSON de la respuesta.
        Maneja casos donde la IA envuelve el JSON en markdown.
        """
        limpio = respuesta.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(limpio)
        except json.JSONDecodeError:
            inicio = limpio.find("{")
            fin = limpio.rfind("}") + 1
            if inicio >= 0 and fin > inicio:
                try:
                    return json.loads(limpio[inicio:fin])
                except json.JSONDecodeError:
                    pass

            raise ValueError(f"No se pudo parsear la respuesta como JSON: {respuesta[:200]}")

    # Alias de compatibilidad
    def analizar_fallo(self, texto_fallo: str, etiquetas: Optional[list[str]] = None) -> dict:
        """Alias para analizar_fallo_anthropic (compatibilidad)"""
        resp = self.analizar_fallo_anthropic(texto_fallo, etiquetas)
        return resp["resultado"]

    def etiquetar_fallo(self, texto_fallo: str, etiquetas: Optional[list[str]] = None) -> dict:
        """Alias para analizar_fallo (compatibilidad)"""
        return self.analizar_fallo(texto_fallo, etiquetas)
