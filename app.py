import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from utils.gemini_api import get_response
from utils.gemini_api import GEMINI_API_KEY
st.sidebar.write("🔐 Key cargada:", GEMINI_API_KEY[:10] + "...")  # Muestra solo parte


# --- Configuración inicial mejorada ---
is_production = os.path.exists('/mount/src')

if not is_production:  # Solo en desarrollo
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        st.sidebar.success("✅ Modo desarrollo - .env cargado")
    else:
        st.sidebar.warning("⚠️ .env no encontrado (solo desarrollo)")

# --- Diagnóstico profesional ---
with st.expander("🔍 Diagnóstico Técnico", expanded=False):
    st.write(f"""
    **Entorno:** {"Producción (Streamlit Cloud)" if is_production else "Desarrollo local"}
    
    **Configuración detectada:**
    - Secrets disponibles: {list(getattr(st, 'secrets', {}).keys())}
    - Key en variables entorno: {'Sí' if os.getenv("GEMINI_API_KEY") else 'No'}
    - Key en secrets: {'Sí' if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets else 'No'}
    """)

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