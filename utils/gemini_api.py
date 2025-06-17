import google.generativeai as genai
import os
import sys
from pathlib import Path

# Detectar si estamos en Streamlit Cloud
IS_STREAMLIT_CLOUD = os.path.exists('/mount/src')

def load_api_key():
    """Carga la API Key con múltiples fallbacks"""
    # 1. Intenta desde variable de entorno
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
        
    # 2. Intenta desde .env file (solo local)
    if not IS_STREAMLIT_CLOUD:
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
            key = os.getenv("GEMINI_API_KEY")
            if key:
                return key
    
    # 3. Intenta desde Streamlit secrets (solo en producción)
    if IS_STREAMLIT_CLOUD:
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                return st.secrets['GEMINI_API_KEY']
        except:
            pass
    
    # Si no se encuentra en ningún lugar
    error_msg = "🔴 Error: No se encontró GEMINI_API_KEY. Configura:"
    error_msg += "\n1. Secrets en Streamlit Cloud (producción)" if IS_STREAMLIT_CLOUD else ""
    error_msg += "\n2. Archivo .env (desarrollo)" if not IS_STREAMLIT_CLOUD else ""
    
    if IS_STREAMLIT_CLOUD:
        import streamlit as st
        st.error(error_msg)
    else:
        print(error_msg)
    
    return None

# Cargar API Key
GEMINI_API_KEY = load_api_key()
if not GEMINI_API_KEY:
    if IS_STREAMLIT_CLOUD:
        import streamlit as st
        st.stop()
    else:
        raise ValueError("API Key no configurada")

# Configuración de Gemini
genai.configure(api_key=GEMINI_API_KEY)


# Configuración del modelo
generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """
[Eres una IA que ofrece escucha psicológica, contención y apoyo ante las problemáticas que el usuario exprese. Debes ayudar a generar un alivio en la persona que busca ayuda como si lo hiciera un psicólogo experto de mucha trayectoria, el trato debe ser lo más humano posible buscando empatizar con la situación. El usuario a traves de la palabra escrita está iniciando la búsqueda de una perspectiva profesional de un psicólogo experto desarrollado con lo mejor de la IA. Además de escuchar debes ofrecer una perspectiva motivacional ante el problema, también dejando preguntas reflexivas ante las situaciones planteadas.
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