"""
Prompts para el análisis de fallos judiciales con Claude.

SYSTEM_PROMPT: Configura el comportamiento y reglas de la IA.
generar_prompt_usuario: Construye el prompt dinámico con el texto del fallo.
"""

SYSTEM_PROMPT = """
Eres un Secretario Judicial experto en el sistema jurídico argentino y la jurisprudencia de la Provincia de Jujuy.
Tu tarea es realizar un ANALISIS ESTRUCTURADO de fallos judiciales para un motor de búsqueda semántica.

### REGLAS DE ETIQUETADO
1. **Prioridad de Taxonomía:** Se te proporcionará una lista de 'ETIQUETAS OFICIALES'. Debes usarlas siempre que el concepto esté presente, incluso si el fallo usa sinónimos (Ej: Si el fallo dice 'finalización del contrato' y tienes 'DESPIDO', usa 'DESPIDO').
2. **Generación Controlada:** Si encuentras un concepto jurídico CLAVE que no está en la lista oficial, crea una etiqueta nueva en MAYÚSCULAS, SINGULAR y sin artículos.
3. **Cantidad:** Selecciona entre 4 y 7 etiquetas por fallo.
4. **Fidelidad:** No inventes hechos. Si el dato no está claro (ej. el DNI), marca como 'No especificado'.

### FORMATO DE SALIDA (JSON ESTRICTO)
Responde exclusivamente en formato JSON con esta estructura:
{
  "resumen": "Máx 150 palabras. Hechos, conflicto y decisión.",
  "materia": "LABORAL | CIVIL | PENAL | FAMILIA | CONTENCIOSO",
  "tipo_proceso": "Ej: ACCION DE AMPARO",
  "resultado": "SE HACE LUGAR | RECHAZO | NULIDAD | PARCIAL",
  "etiquetas": [
    {"nombre": "ETIQUETA", "tipo": "oficial | generada", "relevancia": "alta | media"}
  ],
  "normativa_clave": ["Ley 20744 Art 245", "CPCC Jujuy Art 100"],
  "partes": {"actor": "", "demandado": ""}
}
"""

# Etiquetas base de la taxonomía SAIJ (ejemplo inicial)
ETIQUETAS_SAIJ_BASE = [
    "DESPIDO",
    "INDEMNIZACION",
    "ACCIDENTE DE TRANSITO",
    "DAÑOS Y PERJUICIOS",
    "RESPONSABILIDAD OBJETIVA",
    "RESPONSABILIDAD SUBJETIVA",
    "SEGURO DE RESPONSABILIDAD CIVIL",
    "ACCION DE AMPARO",
    "RECURSO DE APELACION",
    "RECURSO DE INCONSTITUCIONALIDAD",
    "NULIDAD",
    "CONTRATO DE TRABAJO",
    "PREAVISO",
    "ANTIGÜEDAD",
    "HORAS EXTRAS",
    "ALIMENTOS",
    "TENENCIA",
    "REGIMEN DE VISITAS",
    "DIVORCIO",
    "SUCESION",
    "HOMICIDIO",
    "LESIONES",
    "ROBO",
    "HURTO",
    "ESTAFA",
    "PRESCRIPCION",
    "CADUCIDAD",
    "COSTAS",
    "HONORARIOS",
    "MEDIDA CAUTELAR",
    "EMBARGO",
    "INHIBICION",
    "EJECUCION DE SENTENCIA",
    "COSA JUZGADA",
    "DEBIDO PROCESO",
    "DERECHO DE DEFENSA",
    "PRUEBA",
    "PERICIA",
    "TESTIGO",
    "COMPETENCIA",
]


def generar_prompt_usuario(texto_del_fallo: str, etiquetas: list[str] | None = None) -> str:
    """
    Construye el prompt de usuario inyectando las etiquetas oficiales
    y el texto del fallo a analizar.

    Args:
        texto_del_fallo: Texto completo o fragmento del fallo judicial.
        etiquetas: Lista de etiquetas oficiales. Si es None, usa las base.

    Returns:
        El prompt completo listo para enviar a Claude.
    """
    lista_etiquetas = etiquetas or ETIQUETAS_SAIJ_BASE
    etiquetas_formateadas = "\n".join(f"- {e}" for e in lista_etiquetas)

    return f"""
A continuación, procesa el siguiente fallo judicial.

### ETIQUETAS OFICIALES DISPONIBLES (Taxonomía SAIJ):
{etiquetas_formateadas}

### TEXTO DEL FALLO A ANALIZAR:
-----------------------------------------
{texto_del_fallo}
-----------------------------------------

Genera el JSON siguiendo las instrucciones del sistema.
"""
