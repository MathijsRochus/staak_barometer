# Bestandsnaam: src/utils/ui.py
import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    """Hulpfunctie om een afbeelding om te zetten naar base64 voor HTML."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def render_header():
    """
    Deze functie zorgt voor de globale styling en toont het logo
    rechtsboven op de pagina via CSS.
    """
    
    # 1. Probeer het logo te laden
    logo_file = "logo.png"
    logo_base64 = get_base64_of_bin_file(logo_file)

    # 2. CSS Styling
    # We voegen een container toe met 'position: fixed' om het rechtsboven te pinnen.
    css_code = """
    <style>
        /* Algemene styling voor knoppen en titels */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Logo container styling */
        .logo-container {
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 9999;
            width: 80px;  /* Pas de grootte hier aan */
        }
        
        /* Zorg dat de header van Streamlit niet overlapt */
        header[data-testid="stHeader"] {
            z-index: 1;
        }
    </style>
    """
    
    # 3. HTML voor het logo (alleen als het bestand bestaat)
    if logo_base64:
        logo_html = f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" style="width: 100%;">
        </div>
        """
        st.markdown(css_code + logo_html, unsafe_allow_html=True)
    else:
        # Als er geen logo is, laden we alleen de CSS
        st.markdown(css_code, unsafe_allow_html=True)