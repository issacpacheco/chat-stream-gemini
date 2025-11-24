# gemini-chat-backend/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from google import genai
from google.genai import types

# --- Módulos de Soporte ---
from dotenv import load_dotenv

# Cargar el archivo .env para acceder a la GEMINI_API_KEY
load_dotenv() 

# --- 1. CONFIGURACIÓN DE FASTAPI ---
app = FastAPI(
    title="Gemini Chat API",
    description="API de backend para el chat en tiempo real con WebSockets.",
)

# Configuración de CORS: Permite la comunicación con el frontend de React.
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- 2. CONEXIÓN Y CONFIGURACIÓN DE GEMINI ---

client = None
try:
    client = genai.Client()
    print("Cliente de Gemini inicializado correctamente.")
except Exception as e:
    print(f"Error al inicializar el cliente de Gemini. Revisa tu archivo .env: {e}")

# Diccionario para almacenar las sesiones de chat de Gemini (historial)
chat_sessions = {}


# --- 3. ENDPOINTS REST ---

@app.get("/")
def health_check():
    """Endpoint simple para verificar que la API esté funcionando."""
    return {"status": "ok", "message": "FastAPI y Uvicorn están listos."}

@app.delete("/api/sessions/{client_id}")
def clear_session_history(client_id: str):
    """
    Elimina la sesión de chat de Gemini asociada al client_id (borra el historial).
    """
    if client_id in chat_sessions:
        del chat_sessions[client_id]
        print(f"Historial de chat borrado para el cliente {client_id}.")
        return JSONResponse(status_code=200, content={"message": "Historial borrado exitosamente"})
    else:
        return JSONResponse(status_code=404, content={"message": "Sesión de cliente no encontrada o ya borrada"})


# --- 4. ENDPOINT DE WEBSOCKET (Comunicación en tiempo real) ---

@app.websocket("/ws/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    Maneja la conexión WebSocket para el chat.
    """
    await websocket.accept()
    print(f"Cliente conectado: {client_id}")

    # Inicializar o recuperar la Sesión de Chat de Gemini
    if client_id not in chat_sessions:
        if client:
            try:
                # INSTRUCCIÓN DE SISTEMA 
                system_instruction = (
                    "Eres el Profesor Oak, un venerable y sabio maestro Pokémon. "
                    "Tu tono es siempre entusiasta, inspirador y de un experto con profundo conocimiento. "
                    "Tu tarea es educar al usuario sobre los Pokémon, sus características y la historia del mundo Pokémon. "
                    "Cuando el usuario pregunte por un Pokémon, proporciona una ficha detallada que debe incluir: "
                    "1. Nombre y Número de la Pokédex. "
                    "2. Tipo(s) y Especie. "
                    "3. Datos sobre su primera aparición (juego o región) y curiosidades. "
                    "4. Habilidades clave, estadísticas básicas y la cadena evolutiva. "
                    "5. Una sección de **Debilidades y Fortalezas** clara para el combate. "
                    "Mantén el contexto de la conversación. ¡Usa siempre emojis para añadir emoción! ⚡️"
                )
                
                # Definir la configuración para incluir system_instruction y la temperatura
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction, 
                    temperature=0.2, 
                    stop_sequences=[], 
                )

                # Crear la sesión de chat, pasando el config
                chat_sessions[client_id] = client.chats.create(
                    model="gemini-2.5-flash",
                    config=config
                )

                print(f"Nueva sesión de chat de Gemini iniciada con rol de Asistente de maestro pokémon para {client_id}")
            except Exception as e:
                await websocket.send_json({"error": f"Error al crear sesión con Gemini: {e}"})
                await websocket.close()
                return
        else:
            await websocket.send_json({"error": "El servidor no pudo conectar con Gemini. Revisa tu GEMINI_API_KEY."})
            await websocket.close()
            return

    chat_session = chat_sessions[client_id]

    try:
        while True:
            # 1. Recibir mensaje del cliente
            data = await websocket.receive_text()
            print(f"Mensaje de {client_id}: {data}")

            # 2. Enviar a Gemini y obtener el stream
            response_stream = chat_session.send_message_stream(data)
            
            # 3. Enviar el stream de respuesta de vuelta al cliente
            
            await websocket.send_json({"type": "start"}) 
            
            # Variable para acumular la respuesta
            full_response = ""
            
            for chunk in response_stream:
                text = chunk.text
                if text:
                    # Acumular el texto
                    full_response += text 
                    await websocket.send_json({"type": "chunk", "content": text})
            
            await websocket.send_json({"type": "end"}) 
            
            print(f"Respuesta completa enviada a {client_id}.")
            print(f"La respuesta completa generada por Gemini fue:\n--- INICIO DE RESPUESTA ---\n{full_response}\n--- FIN DE RESPUESTA ---")


    except WebSocketDisconnect:
        print(f"Cliente desconectado: {client_id}")
    except Exception as e:
        print(f"Error inesperado en WebSocket con {client_id}: {e}")
        await websocket.send_json({"error": f"Error interno del servidor: {e}"})
        await websocket.close()