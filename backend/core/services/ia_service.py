"""
Servicio para procesamiento con Claude API
"""
import json
import anthropic
from core.config import settings


PROMPT_ETIQUETADO = """
Analiza el siguiente fallo judicial de la Provincia de Jujuy y extrae:
1. **Resumen ejecutivo** (máximo 150 palabras): Describe los hechos principales, el conflicto legal y la resolución del tribunal.
2. **Palabras clave** (máximo 10): Términos jurídicos relevantes del caso.
3. **Categorías principales**:
   - Materia: (Ej: Civil, Penal, Laboral, Familia, Contencioso Administrativo)
   - Tipo de proceso: (Ej: Amparo, Recurso de Apelación, Juicio Ordinario)
   - Subtemas: (Ej: Despido, Daños y Perjuicios, Inconstitucionalidad)
4. **Resultado**: (Ej: Se hizo lugar, Se rechazó, Se confirmó, Se revocó)
5. **Partes**: Actor/Demandante y Demandado
6. **Normas citadas**: Leyes, artículos o códigos mencionados

Responde ÚNICAMENTE en formato JSON siguiendo esta estructura:
{{
    "resumen": "...",
    "palabras_clave": ["...", "..."],
    "materia": "...",
    "tipo_proceso": "...",
    "subtemas": ["...", "..."],
    "resultado": "...",
    "actor": "...",
    "demandado": "...",
    "normas_citadas": ["...", "..."]
}}

FALLO:
{texto_fallo}
"""


class IAService:
    """Servicio para procesamiento con IA"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def etiquetar_fallo(self, texto_fallo: str) -> dict:
        """
        Analiza un fallo y extrae información estructurada usando Claude
        """
        message = self.client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": PROMPT_ETIQUETADO.format(texto_fallo=texto_fallo)
            }]
        )
        
        # Extraer JSON de la respuesta
        respuesta = message.content[0].text
        
        # Limpiar posibles markdown
        respuesta = respuesta.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(respuesta)
        except json.JSONDecodeError:
            # Si falla, intentar extraer JSON del texto
            inicio = respuesta.find("{")
            fin = respuesta.rfind("}") + 1
            if inicio >= 0 and fin > inicio:
                return json.loads(respuesta[inicio:fin])
            raise ValueError("No se pudo parsear la respuesta de Claude como JSON")
