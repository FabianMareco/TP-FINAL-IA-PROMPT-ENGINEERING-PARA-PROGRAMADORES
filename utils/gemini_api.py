import google.generativeai as genai
import os
from pathlib import Path
import sys

# Configuración para Streamlit
IN_STREAMLIT = "streamlit" in sys.modules

if IN_STREAMLIT:
    import streamlit as st

def load_api_key():
    """Carga la API Key con manejo robusto de errores"""
    try:
        # 1. Intenta desde variable de entorno
        if os.getenv("GEMINI_API_KEY"):
            return os.getenv("GEMINI_API_KEY")
            
        # 2. Intenta desde .env file
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
            if os.getenv("GEMINI_API_KEY"):
                return os.getenv("GEMINI_API_KEY")
        
        # 3. Intenta desde Streamlit secrets (solo en producción)
        if IN_STREAMLIT:
            try:
                if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                    return st.secrets['GEMINI_API_KEY']
            except Exception:
                pass
        
        # Si no encuentra en ningún lugar
        error_msg = "🔴 Error: No se encontró GEMINI_API_KEY en:"
        error_msg += "\n1. Variables de entorno"
        error_msg += "\n2. Archivo .env"
        if IN_STREAMLIT:
            error_msg += "\n3. Streamlit secrets"
        
        if IN_STREAMLIT:
            st.error(error_msg)
        else:
            print(error_msg)
        
        return None
        
    except Exception as e:
        error_msg = f"Error cargando API Key: {str(e)}"
        if IN_STREAMLIT:
            st.error(error_msg)
        else:
            print(error_msg)
        return None

# Cargar API Key
GEMINI_API_KEY = load_api_key()
if not GEMINI_API_KEY:
    if IN_STREAMLIT:
        st.stop()
    else:
        raise ValueError("API Key no configurada")

# Resto de tu configuración...
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