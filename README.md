# 🤖 Gemini Chat: Asistente de Programación en Tiempo Real

Este proyecto implementa un asistente de chat en tiempo real utilizando la **API de Google Gemini** y una arquitectura **Full-Stack** moderna.

El asistente está configurado con instrucciones de sistema para actuar como un tutor de código, proporcionando explicaciones, *snippets* y documentación.

## 🧱 Arquitectura del Proyecto

La aplicación se divide en dos servicios principales que se comunican a través de WebSockets y API REST:

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Backend (Servidor)** | **Python (FastAPI)** | Gestiona la conexión segura con la API de Gemini, mantiene el historial de las sesiones de chat, y maneja la comunicación en tiempo real mediante **WebSockets**. |
| **Frontend (Cliente)** | **React.js (Vite)** | Proporciona una interfaz de usuario moderna con estilo de editor de código, consume el stream de WebSockets para respuestas en tiempo real y renderiza el contenido en **Markdown**. |

## 🚀 Requisitos Previos

Asegúrate de tener instalado lo siguiente:

* **Python 3.10+**
* **Node.js 18+** (con `npm` o `yarn`)
* Una clave de **API de Gemini** (obtenida de Google AI Studio).

## 🔑 Configuración de la Clave API

Para que el *backend* pueda comunicarse con Gemini, necesitas configurar tu clave de API:

1.  Navega al directorio del backend:
    ```bash
    cd gemini-chat-backend
    ```
2.  Crea un archivo llamado **`.env`** en este directorio.
3.  Añade tu clave de la siguiente manera:

    ```env
    # gemini-chat-backend/.env
    GEMINI_API_KEY="TU_CLAVE_AQUI"
    ```

    > **⚠️ Seguridad:** Asegúrate de que este archivo **`.env`** esté incluido en tu `.gitignore` para no subir tu clave secreta al repositorio.

## ⚙️ Instalación y Ejecución

Sigue estos pasos para levantar la aplicación completa.

### 1. Instalación y Ejecución del Backend (FastAPI)

El *backend* de Python se encargará de gestionar las peticiones y el *streaming* de Gemini.

```bash
# 1. Navega al directorio del backend
cd gemini-chat-backend

# 2. Crea e inicia un entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate 

# 3. Instala las dependencias
pip install -r requirements.txt 
# NOTA: Si no tienes requirements.txt, usa: pip install fastapi uvicorn google-genai python-dotenv

# 4. Inicia el servidor
uvicorn main:app --reload
```
## El servidor estará corriendo en http://127.0.0.1:8000. Mantén esta terminal abierta.

# 2. Instalación y Ejecución del Frontend (React)
El frontend de React se encargará de la interfaz de usuario.

```Bash

# 1. Navega al directorio del frontend
cd ../gemini-chat-frontend 

# 2. Instala las dependencias de Node
npm install 
# NOTA: Asegúrate de tener instalado 'react-markdown' también.

# 3. Inicia la aplicación de React
npm run dev
```
## La aplicación se abrirá en tu navegador (generalmente en http://localhost:5173/).

# ✨ Características Principales
Respuestas en Streaming: Comunicación en tiempo real a través de WebSockets (FastAPI), haciendo que las respuestas aparezcan fragmento por fragmento.

Asistente de Código: Configurado para enfocarse solo en temas de programación y código.

Renderizado Markdown: Las respuestas de Gemini se renderizan limpiamente con formato (listas, negritas, bloques de código) en el frontend (React).

Limpieza de Sesión: El botón "Limpiar Historial" utiliza un endpoint REST (DELETE) para borrar el contexto de la conversación en el servidor.

Diagnóstico: Incluye un print en el backend (main.py) para diagnosticar la respuesta completa de Gemini antes de enviarla.

# 🛠️ Contribución
Siéntete libre de clonar este repositorio, explorar el código y proponer mejoras. Puedes contribuir con:

Funcionalidad de base de datos para persistir el historial.

Mejoras de estilo o adaptabilidad (responsiveness).

Implementación de autenticación de usuarios.


---

## ✅ Próximo Paso

Para asegurarte de que la sección de instalación de dependencias funcione perfectamente, solo te faltaría crear el archivo `requirements.txt` en tu carpeta `gemini-chat-backend`:

**Contenido de `gemini-chat-backend/requirements.txt`:**

fastapi uvicorn[standard] google-genai python-dotenv