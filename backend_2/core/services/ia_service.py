"""
Servicio para analisis de fallos judiciales con Claude API
"""
import json 
import os 
import anthropic

from core.imports import SYSTEM_PROMPT, generar_prompt_usuario

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL","")

class IAService:
    """Servicio qu econecta con Claude para analizar fallos judiciales."""
    
    def __init__(self):
        #anthropic lee lae ANTHROPIC_KEY del entorno automaticamente
        self.client =  anthropic.Anthropic()
        
    
    def analizar_fallo(self, text_fallo :  str, etiquetas: list[str] | None = None) -> dict : 
       """ 
       Envia el texto de un fallo a Claude y devuelve el analisis estructurado
       
       Args:
           texto_fallo: Texto completo del fallo judicial a analizar
           etiquetas: Lista opcional de etiquetas oficiales. Si es None, usa las bases
        
       Returns:
           Dict con el analisis estructurado (resumen, materia, etiquetas, etc...)
           
       """"
       prompt_usuario = generar_prompt_usuario(text_fallo, etiquetas)
       response = self.client.messages.create(
           model=CLAUDE_MODEL,
           max_tokens=2000,
           messages=[
               {
                   "role": "user",
                   "content": prompt_usuario
               }
           ]
       )
       return json.loads(response.content[0].text)
       
    def etiquetar_fallo(self, text_fallo: str) -> dict:
       """Extrae y parsea el JSON de la respuesta de Claude."""
       limpio = text.replace("```json", "").replace("```", "").strip()
       
       try:
          return json.loads(limpio)
       except json.JSONDecodeError:
          inicio = limpio.find("{")
          fin = limpio.rfind("}") + 1
          if inicio >= 0 and fin > inicio:
             return json.loads(limpio[inicio:fin])
          raise ValueError("No se pudo parsear la respuesta de Claude como JSON")