import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

st.title("Happblemos - Tu espacio de escucha")

user_input = st.text_area("Escribe lo que quieras compartir acerca de como te sentís o como estuvo tu día:", height=150)

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
with st.expander("CÓMO FUNCIONA HAPPBLEMOS", expanded=False):
    st.markdown("""
    <div class='info-box'>
        <p>Happblemos es un espacio de escucha, co-creado con lo mejor de la IA, interactuarás de manera segura y podrás poner en palabras lo que te sucede, para luego recibir una devolución con la intención de ayudarte.</p>
        <p>Puedes escribir lo que te sucede, lo que sea, expresado de la manera que quieras, HAPPBLEMOS está para escucharte y brindarte su contención.</p>
    </div>
    """, unsafe_allow_html=True)