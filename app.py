import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

st.title("Verificación de Secrets")

# Verifica si está cargando correctamente
if 'GEMINI_API_KEY' in st.secrets:
    st.success(f"✅ Key cargada correctamente (longitud: {len(st.secrets['GEMINI_API_KEY'])})")
    st.code(f"Prefijo: {st.secrets['GEMINI_API_KEY'][:10]}...")
else:
    st.error("❌ No se encontró GEMINI_API_KEY en secrets")

st.write("Ruta actual:", os.getcwd())
st.write("Contenido de .streamlit:", os.listdir(".streamlit"))

# --- Tu aplicación normal ---
st.title("Happblemos - Tu espacio de escucha")

# Resto de tu interfaz...
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