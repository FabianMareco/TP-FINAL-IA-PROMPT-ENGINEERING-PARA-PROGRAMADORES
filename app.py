import streamlit as st
from utils.gemini_api import get_response
import os
from dotenv import load_dotenv

load_dotenv()
# Configuración inicial con spinner
with st.spinner('Inicializando aplicación...'):
    try:
        from utils.gemini_api import get_response
    except Exception as e:
        st.error(f"Error crítico al cargar dependencias: {str(e)}")
        st.stop()
st.write("Gemini API Key cargada:", os.getenv("GEMINI_API_KEY") is not None)

st.title("Happblemos - Tu espacio de escucha")

st.markdown("Escribí lo que quieras compartir acerca de como te sentís o como estuvo tu día:")

user_input = st.text_area("Tu mensaje", height=150)

if st.button("Happblemos"):
    if user_input:
        try:
            ai_response = get_response(user_input)
            st.markdown("**IA responde:**")
            st.success(ai_response)
        except ValueError as e:
            st.error(f"Error de configuración: {str(e)}")
        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")
    else:
        st.warning("Por favor, escribí un mensaje antes de enviar.")