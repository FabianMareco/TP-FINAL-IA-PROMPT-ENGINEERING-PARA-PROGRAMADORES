import google.generativeai as genai
import os
import streamlit as st
from pathlib import Path

def get_api_key():
    """Obtiene la API Key con verificación robusta"""
    # 1. Intenta desde Secrets de Streamlit (producción)
    try:
        if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            key = st.secrets['GEMINI_API_KEY']
            if key and key.startswith('AIza'):
                st.success("✅ API Key cargada desde Secrets")
                return key
    except:
        pass
    
    # 2. Intenta desde .env (desarrollo local)
    try:
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
            key = os.getenv("GEMINI_API_KEY")
            if key and key.startswith('AIza'):
                print("✅ API Key cargada desde .env")
                return key
    except:
        pass
    
    # Si falla todo
    error_msg = """
    🔴 Error: No se encontró API Key válida.
    Configuración requerida:
    
    Para producción (Streamlit Cloud):
    1. Ve a Settings > Secrets
    2. Agrega exactamente:
       [secrets]
       GEMINI_API_KEY = "tu_clave_aqui"
    
    Para desarrollo local:
    1. Crea archivo .env en la raíz
    2. Agrega: GEMINI_API_KEY=tu_clave_aqui
    """
    st.error(error_msg)
    st.stop()

# Configuración global
GEMINI_API_KEY = get_api_key()
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