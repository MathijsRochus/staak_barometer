# Bestandsnaam: main.py
import streamlit as st
from PIL import Image
from src.backend.client import supabase

# Importeer de pagina functies
from src.views.login import render_login
from src.views.home import render_home
from src.views.detail import render_detail
from src.views.admin import render_admin

# Importeer je UI functie
from src.utils.ui import render_header

# --- 1. Config & Logo Laden ---
# We proberen het logo te vinden in de assets map voor de favicon
try:
    # Zorg dat dit pad klopt met waar je bestand staat
    icon_image = Image.open("src/assets/logo.png") 
except FileNotFoundError:
    # Fallback als het bestand niet gevonden wordt (bv. emoji)
    icon_image = "📊"

st.set_page_config(
    page_title="De Staakbarometer-de-grève", 
    page_icon=icon_image, 
    layout="centered"
)

# 2. Global State Init
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'language' not in st.session_state: st.session_state.language = 'nl'

# 3. UI styling & Logo header (behalve op login scherm)
if st.session_state.page != 'login':
    render_header()

# 4. Session Check (Auth Guard)
if "session" in st.session_state:
    try:
        supabase.auth.set_session(
            st.session_state.session.access_token, 
            st.session_state.session.refresh_token
        )
    except Exception:
        st.session_state.page = 'login'
        if 'user' in st.session_state: del st.session_state.user

# 5. Routing
if st.session_state.page == 'login':
    render_login()
    
elif st.session_state.page == 'home':
    render_home()
    
elif st.session_state.page == 'detail':
    render_detail()
    
elif st.session_state.page == 'admin':
    # Eenvoudige admin check
    user_email = st.session_state.user.email if 'user' in st.session_state else ""
    
    # Pas dit emailadres aan naar jouw admin email
    if user_email != "mathijs.rochus@outlook.com": 
        st.error("Geen toegang.")
        st.session_state.page = 'home'
        st.rerun()
    else:
        render_admin()