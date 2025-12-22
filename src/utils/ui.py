import streamlit as st
import os

def load_custom_css():
    """
    Laadt het CSS bestand uit src/assets/style.css
    en injecteert het in de Streamlit app.
    """
    # We zoeken het pad relatief aan dit bestand
    # Pad: src/utils/ui.py -> 1 omhoog (src) -> assets -> style.css
    css_file_path = os.path.join("src", "assets", "style.css")
    
    try:
        with open(css_file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Als het bestand niet gevonden wordt, printen we een stille warning in de console
        # zodat de app niet crasht.
        print(f"Let op: CSS bestand niet gevonden op: {css_file_path}")