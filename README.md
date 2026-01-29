# JurisAR ⚖️🤖

**Motor de Inteligencia Jurídica y Búsqueda Semántica para la Jurisprudencia Argentina.**

JurisAR es una plataforma de código abierto diseñada para transformar el acceso a la información judicial en Argentina. Utilizando Modelos de Lenguaje de Gran Escala (LLM), el sistema procesa fallos judiciales crudos y los convierte en datos estructurados, analizados y fáciles de buscar.

## 🚀 Características Principales

* **Búsqueda Semántica:** Encuentra fallos por concepto y contexto, no solo por palabras clave (ej: busca "accidente de trayecto" y encuentra "accidente in itinere").
* **Etiquetado Inteligente:** Clasificación automática basada en el **Tesauro Jurídico de SAIJ**.
* **Resúmenes Ejecutivos:** Resúmenes técnicos de 150 palabras que destacan hechos, conflicto y resolución.
* **Arquitectura Federal:** Diseñado para integrar fallos de cualquier provincia (iniciando con Jujuy) y tribunales nacionales.
* **Análisis de Normativa:** Extracción automática de leyes y artículos citados.

## 🛠️ Stack Tecnológico

* **IA (Procesamiento):** Anthropic Claude 3.5 Sonnet.
* **IA (Vectores):** OpenAI `text-embedding-3-small`.
* **Base de Datos:** PostgreSQL + `pgvector`.
* **Backend:** Python (FastAPI / LangChain).
* **Scraping:** Playwright / BeautifulSoup.

## 📁 Estructura del Proyecto

```bash
├── scrapers/          # Módulos de extracción por jurisdicción (Jujuy, Nación, etc.)
├── core/              # Lógica de procesamiento de IA y Embeddings
├── database/          # Esquemas SQL y migraciones
├── api/               # Endpoints del servicio
└── taxonomy/          # Diccionarios de etiquetas oficiales (SAIJ)