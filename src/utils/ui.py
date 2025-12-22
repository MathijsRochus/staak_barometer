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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "assets", file_name)
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"⚠️ CSS bestand niet gevonden: {file_path}")
        return ""

def render_header():
    """Renders de globale header styling en het logo."""
    # 1. Laad de CSS (style.css)
    css_content = load_local_css("style.css")
    
    # 2. Bepaal pad naar logo 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "..", "assets", "logo.png")
    logo_b64 = get_base64_of_bin_file(logo_path)

    # 3. Bouw de style string en injecteer deze
    # We voegen hier de @import voor de fonts toe!
    custom_css = f"""
    <style>
        /* Import Google Fonts: Inter & Poppins */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;700;800&display=swap');

        {css_content}
        
        /* Logo Container (Links) */
        .logo-container {{
            position: fixed;
            top: 2.5rem;
            left: 2rem;
            z-index: 999;
            width: 80px;
        }}

        /* Responsive padding */
        @media (min-width: 800px) {{
            .main .block-container {{
                padding-left: 5rem; 
            }}
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # 4. Toon het logo
    if logo_b64:
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_b64}" style="width: 100%;">
            </div>
            """,
            unsafe_allow_html=True
        )