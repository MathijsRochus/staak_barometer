# Bestandsnaam: main.py
import streamlit as st
from src.backend.client import supabase

# Importeer de pagina functies
from src.views.login import render_login
from src.views.home import render_home
from src.views.detail import render_detail
from src.views.admin import render_admin

# NIEUW: Importeer je UI functie
from src.utils.ui import render_header

# 1. Config
st.set_page_config(page_title="De Staak Barometer", page_icon="📊", layout="centered")

# 2. Global State Init
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'language' not in st.session_state: st.session_state.language = 'nl'

# 3. UI styling & Logo (behalve op login scherm)
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
    # Eenvoudige admin check (in productie best via RLS of custom claim doen)
    user_email = st.session_state.user.email if 'user' in st.session_state else ""
    # Pas dit emailadres aan naar jouw admin email
    if user_email != "mathijs@qargo.com": 
        st.error("Geen toegang.")
        st.session_state.page = 'home'
        st.rerun()
    else:
        render_admin()