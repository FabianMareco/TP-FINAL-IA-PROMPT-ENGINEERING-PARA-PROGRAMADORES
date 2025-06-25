import os
import sys
from pathlib import Path

# Librerías externas
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Detección del entorno (ej. Streamlit Cloud)
IS_STREAMLIT_CLOUD = 'streamlit' in sys.modules and os.path.exists('/mount/src')

# Constante para evitar hardcodear el nombre de la variable
GEMINI_KEY_NAME = "GEMINI_API_KEY"


def load_api_key():
    """Carga la API Key desde secrets, variables de entorno o .env"""
    try:
        # 1. Intenta desde Streamlit Secrets (producción)
        if IS_STREAMLIT_CLOUD and hasattr(st, 'secrets') and GEMINI_KEY_NAME in st.secrets:
            api_key = st.secrets[GEMINI_KEY_NAME]
            if api_key and api_key.startswith('AIza'):
                return api_key

        # 2. Intenta desde variables de entorno
        api_key = os.environ.get(GEMINI_KEY_NAME)
        if api_key and api_key.startswith('AIza'):
            return api_key

        # 3. Intenta desde .env (modo desarrollo local)
        load_dotenv()  # ← Más flexible: busca automáticamente en el directorio actual
        api_key = os.environ.get(GEMINI_KEY_NAME)
        if api_key and api_key.startswith('AIza'):
            if not IS_STREAMLIT_CLOUD:
                print(f"🔑 DEBUG: Clave cargada desde .env: {api_key[:10]}...")
            return api_key

        # Si no se encuentra ninguna clave válida
        error_msg = """\
🔴 Error: No se encontró una API Key válida.

Para producción (Streamlit Cloud):
1. Ve a Settings > Secrets
2. Agrega: [secrets]
   GEMINI_API_KEY = "tu_clave_aqui"

Para desarrollo local:
1. Crea un archivo .env en la raíz del proyecto
2. Agrega: GEMINI_API_KEY=tu_clave_aqui
"""
        if IS_STREAMLIT_CLOUD:
            st.error(error_msg)
        else:
            print(error_msg)
        return None

    except Exception as e:
        error_msg = f"Error cargando API Key: {str(e)}"
        if IS_STREAMLIT_CLOUD:
            st.error(error_msg)
        else:
            print(error_msg)
        return None


# Cargar y validar API Key
GEMINI_API_KEY = load_api_key()
if not GEMINI_API_KEY:
    if IS_STREAMLIT_CLOUD:
        st.stop()
    else:
        raise ValueError("API Key no configurada correctamente")

# Configurar Gemini antes de usar la API
genai.configure(api_key=GEMINI_API_KEY)

# Configuración del modelo
generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
# Configuración del modelo
generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """
[Eres una IA que ofrece escucha psicológica, contención y apoyo ante las problemáticas que el usuario exprese. Debes ayudar a generar un alivio en la persona que busca ayuda como si lo hiciera un psicólogo experto de mucha trayectoria, el trato debe ser lo más humano posible buscando empatizar con la situación. El usuario a través de la palabra escrita está iniciando la búsqueda de una perspectiva profesional de un psicólogo experto desarrollado con lo mejor de la IA. Además de escuchar debes ofrecer una perspectiva motivacional ante el problema, también dejando preguntas reflexivas ante las situaciones planteadas.
No debes ofrecer diagnósticos ni medicación, solo escucha y apoyo emocional. No debes ofrecer consejos médicos ni psiquiátricos, solo apoyo emocional y escucha activa.]
"""

def get_response(user_message):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=system_prompt
        )
        chat = model.start_chat()
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"Error al comunicarse con Gemini API: {str(e)}"
