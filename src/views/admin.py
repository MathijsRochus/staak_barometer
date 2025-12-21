import streamlit as st
import json
from src.backend.service import create_event

def render_admin():
    st.title("Admin: Nieuw Event")
    
    if st.button("Terug"):
        st.session_state.page = 'home'
        st.rerun()

    with st.form("new_event"):
        date = st.date_input("Datum")
        sector = st.text_input("Sector (bv. Zorg)")
        
        st.subheader("Titels")
        t_nl = st.text_input("Titel NL")
        t_fr = st.text_input("Titel FR")
        t_en = st.text_input("Titel EN")
        
        st.subheader("Beschrijving")
        d_nl = st.text_area("Beschrijving NL")
        d_fr = st.text_area("Beschrijving FR")
        d_en = st.text_area("Beschrijving EN")
        
        submitted = st.form_submit_button("Aanmaken")
        
        if submitted:
            # Maak de JSON objecten voor de database
            title_json = {"nl": t_nl, "fr": t_fr, "en": t_en}
            desc_json = {"nl": d_nl, "fr": d_fr, "en": d_en}
            
            try:
                create_event(date, sector, title_json, desc_json)
                st.success("Event aangemaakt!")
            except Exception as e:
                st.error(f"Fout: {e}")