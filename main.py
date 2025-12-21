import streamlit as st
from src.backend.client import supabase

# Importeer de pagina functies
from src.views.login import render_login
from src.views.home import render_home
from src.views.detail import render_detail
from src.views.admin import render_admin

# 1. Config
st.set_page_config(page_title="De Staak Barometer", page_icon="📊", layout="centered")

# 2. Global State Init
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'language' not in st.session_state: st.session_state.language = 'nl'

# 3. Session Check (Auth Guard)
if "session" in st.session_state:
    try:
        supabase.auth.set_session(
            st.session_state.session.access_token, 
            st.session_state.session.refresh_token
        )
    except Exception:
        st.session_state.page = 'login'
        if 'user' in st.session_state: del st.session_state.user

# ... (imports en setup)

# Haal de email op van de ingelogde gebruiker (als die er is)
user_email = st.session_state.user.email if 'user' in st.session_state else ""
ADMIN_EMAIL = "mathijs@qargo.com"  # Moet matchen met je SQL policy!

# ...

# 4. Routing
if st.session_state.page == 'login':
    render_login()
elif st.session_state.page == 'home':
    render_home()
    # Toon een extra knopje op home alleen voor de admin
    if user_email == ADMIN_EMAIL:
        if st.sidebar.button("Admin Panel"):
            st.session_state.page = 'admin'
            st.rerun()

elif st.session_state.page == 'detail':
    render_detail()
    
elif st.session_state.page == 'admin':
    # Extra veiligheidscheck: stuur weg als ze niet de admin zijn
    if user_email != ADMIN_EMAIL:
        st.error("Geen toegang.")
        st.session_state.page = 'home'
        st.rerun()
    else:
        render_admin()