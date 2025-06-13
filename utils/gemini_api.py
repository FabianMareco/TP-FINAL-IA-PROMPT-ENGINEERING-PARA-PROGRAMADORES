import google.generativeai as genai
import streamlit as st
import os

def load_api_key():
    """Carga la API Key con verificación explícita"""
    try:
        # 1. Intenta desde Secrets de Streamlit (producción)
        if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            st.success("✅ API Key cargada desde Secrets")
            return st.secrets['GEMINI_API_KEY']
        
        # 2. Intenta desde variable de entorno (desarrollo)
        key = os.getenv("GEMINI_API_KEY")
        if key:
            st.success("✅ API Key cargada desde variables de entorno")
            return key
            
        # Si no se encuentra
        st.error("""
        🔴 Configura la API Key en:
        1. Secrets de Streamlit (producción)
        2. Variables de entorno (desarrollo)
        """)
        return None
        
    except Exception as e:
        st.error(f"Error técnico: {str(e)}")
        return None

# Configuración
GEMINI_API_KEY = load_api_key()

if not GEMINI_API_KEY:
    st.warning("La aplicación se detendrá por falta de API Key")
    st.stop()  # Detiene completamente la aplicación

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