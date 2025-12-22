# Bestandsnaam: src/utils/ui.py
import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    """Leest een binair bestand (plaatje) en zet het om naar base64 string."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def load_local_css(file_name):
    """Leest CSS bestand in met een robuust pad."""
    # Bepaal de map waar DIT bestand (ui.py) staat
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Ga één map omhoog (naar src) en dan naar assets
    file_path = os.path.join(current_dir, "..", "assets", file_name)
    
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"⚠️ CSS bestand niet gevonden: {file_path}")
        return ""

def render_header():
    # 1. Laad de CSS (style.css)
    css_content = load_local_css("style.css")
    
    # 2. Bepaal pad naar logo voor de HTML (ook robuust)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "..", "assets", "logo.png")
    logo_b64 = get_base64_of_bin_file(logo_path)

    # 3. Bouw de style string en injecteer deze
    custom_css = f"""
    <style>
        {css_content}
        
        /* Specifieke CSS voor de logo container (python-logica) */
        .logo-container {{
            position: fixed;
            top: 2.5rem;
            right: 2rem;
            z-index: 999;
            width: 80px;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # 4. Toon het logo in de HTML container
    if logo_b64:
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_b64}" style="width: 100%;">
            </div>
            """,
            unsafe_allow_html=True
        )