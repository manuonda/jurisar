# Backend JurisAR - Guía de Inicio

## 🚀 Primeros Pasos

### 1. Crear un entorno virtual (recomendado)

Un entorno virtual aísla las dependencias de Python de tu proyecto. Es como tener una "caja" separada para cada proyecto.

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```bash
# Opción 1: Usando Python directamente
python main.py

# Opción 2: Usando uvicorn directamente (más control)
uvicorn main:app --reload

# El flag --reload hace que el servidor se reinicie automáticamente 
# cuando cambias el código (útil para desarrollo)
```

### 4. Probar la API

Una vez que el servidor esté corriendo, puedes:

1. **Visitar en el navegador:**
   - http://localhost:8000/ - Verás el mensaje de bienvenida
   - http://localhost:8000/health - Verás el estado del servidor

2. **Ver la documentación automática:**
   - http://localhost:8000/docs - Interfaz interactiva (Swagger UI)
   - http://localhost:8000/redoc - Documentación alternativa

## 📚 Conceptos Importantes

### ¿Qué es FastAPI?
FastAPI es un framework moderno de Python para crear APIs REST. Es rápido, fácil de usar y genera documentación automática.

### ¿Qué es un endpoint?
Un endpoint es una URL que responde a peticiones HTTP. Por ejemplo:
- `GET /` - Obtiene información
- `POST /fallos` - Crea un nuevo fallo
- `GET /fallos/{id}` - Obtiene un fallo específico

### ¿Qué es CORS?
CORS (Cross-Origin Resource Sharing) permite que tu frontend Angular (que corre en otro puerto) pueda hacer peticiones a tu backend sin problemas de seguridad del navegador.

## 🔄 Próximos Pasos

1. Crear estructura de carpetas (core, api, database)
2. Configurar base de datos PostgreSQL
3. Crear modelos de datos
4. Implementar endpoints de búsqueda
5. Integrar servicios de IA
