### Documento 2: `CORE.md` (Arquitectura del Sistema)
*Este explica el "Cómo". Es el manual técnico del procesamiento.*

```markdown
# Arquitectura del Core: JurisAR

Este documento describe el pipeline de procesamiento de datos que convierte un documento judicial crudo en un objeto de conocimiento estructurado.

## ⚙️ El Pipeline de Procesamiento (6 Etapas)

### 1. Ingesta (Scraping)
El sistema extrae el texto crudo de las fuentes oficiales. Se realiza una limpieza inicial para eliminar ruidos (firmas digitales, encabezados repetitivos, metadatos de impresión).

### 2. Clasificación y Etiquetado (Claude 3.5)
Se envía el texto limpio a Claude 3.5 Sonnet con un **Prompt Híbrido**. 
* **Taxonomía Fija:** El sistema inyecta las etiquetas más frecuentes del Tesauro de SAIJ para forzar la normalización.
* **Descubrimiento:** Si el modelo detecta un concepto nuevo relevante, lo propone como etiqueta "generada".

### 3. Generación de Embeddings (OpenAI)
Para permitir la búsqueda semántica, el sistema genera un vector numérico. No se vectoriza el fallo completo, sino un **"Documento de Búsqueda"** compuesto por:
> `Carátula + Resumen IA + Etiquetas Seleccionadas + Normativa Clave`

### 4. Almacenamiento Vectorial
El vector (1536 dimensiones) se almacena en PostgreSQL usando la extensión `pgvector`. Esto permite realizar búsquedas de **Distancia Coseno** a gran escala.

### 5. Búsqueda Híbrida
El motor de búsqueda de JurisAR combina dos mundos:
* **Filtros SQL:** Para buscar por etiquetas exactas (ej: `materia = 'LABORAL'`).
* **Similitud Vectorial:** Para ordenar los resultados según la relevancia del concepto buscado por el usuario.

### 6. Mantenimiento de Taxonomía
Las etiquetas marcadas como "generadas" por la IA entran en una cola de revisión. Una vez validadas, se integran a la **Taxonomía Oficial**, permitiendo que el sistema aprenda nuevos términos jurídicos automáticamente.

## 🧠 Lógica del Prompt
El sistema utiliza **System Prompting** para garantizar que la respuesta sea un JSON puro, eliminando alucinaciones y asegurando que los nombres de las etiquetas coincidan exactamente con la base de datos de SAIJ.