import streamlit as st
from src.backend.service import create_event
import datetime

def render_admin():
    st.title("Admin: Nieuw Event (Draft)")

    # 1. State Management (Draft variabelen initialiseren)
    if 'draft_date' not in st.session_state: st.session_state.draft_date = datetime.date.today()
    
    # Sector variabelen (per taal)
    if 'draft_sector_nl' not in st.session_state: st.session_state.draft_sector_nl = ""
    if 'draft_sector_fr' not in st.session_state: st.session_state.draft_sector_fr = ""
    if 'draft_sector_en' not in st.session_state: st.session_state.draft_sector_en = ""
    
    # Titel variabelen
    if 'draft_title_nl' not in st.session_state: st.session_state.draft_title_nl = ""
    if 'draft_title_fr' not in st.session_state: st.session_state.draft_title_fr = ""
    if 'draft_title_en' not in st.session_state: st.session_state.draft_title_en = ""
    
    # Beschrijving variabelen
    if 'draft_desc_nl' not in st.session_state: st.session_state.draft_desc_nl = ""
    if 'draft_desc_fr' not in st.session_state: st.session_state.draft_desc_fr = ""
    if 'draft_desc_en' not in st.session_state: st.session_state.draft_desc_en = ""

    # 2. Terug knop
    if st.button("← Terug naar Home"):
        _clear_draft() # Optioneel: draft wissen bij weggaan
        st.session_state.page = 'home'
        st.rerun()

    # 3. AI Placeholder (Toekomst)
    with st.expander("✨ AI Assistent (Toekomst)"):
        st.info("Hier komt functionaliteit om velden automatisch te vullen op basis van een URL.")

    # 4. Het Formulier
    with st.form("draft_form"):
        st.subheader("Details")
        # Datum
        date = st.date_input("Datum", value=st.session_state.draft_date)
        
        # Sector (3 kolommen)
        st.markdown("**Sector**")
        c1, c2, c3 = st.columns(3)
        with c1: sec_nl = st.text_input("NL", value=st.session_state.draft_sector_nl, key="in_sec_nl")
        with c2: sec_fr = st.text_input("FR", value=st.session_state.draft_sector_fr, key="in_sec_fr")
        with c3: sec_en = st.text_input("EN", value=st.session_state.draft_sector_en, key="in_sec_en")
        
        # Titels
        st.subheader("Titels")
        t_nl = st.text_input("Titel NL", value=st.session_state.draft_title_nl)
        t_fr = st.text_input("Titel FR", value=st.session_state.draft_title_fr)
        t_en = st.text_input("Titel EN", value=st.session_state.draft_title_en)
        
        # Beschrijvingen
        st.subheader("Beschrijving")
        d_nl = st.text_area("Beschrijving NL", value=st.session_state.draft_desc_nl)
        d_fr = st.text_area("Beschrijving FR", value=st.session_state.draft_desc_fr)
        d_en = st.text_area("Beschrijving EN", value=st.session_state.draft_desc_en)
        
        # 5. Opslaan
        submitted = st.form_submit_button("Event Aanmaken & Publiceren")
        
        if submitted:
            # JSON objecten bouwen
            sector_json = {"nl": sec_nl, "fr": sec_fr, "en": sec_en}
            title_json = {"nl": t_nl, "fr": t_fr, "en": t_en}
            desc_json = {"nl": d_nl, "fr": d_fr, "en": d_en}
            
            try:
                # Opslaan in DB
                create_event(date, sector_json, title_json, desc_json)
                st.success("Event succesvol aangemaakt!")
                
                # Opruimen en redirecten
                _clear_draft()
                st.session_state.page = 'home'
                st.rerun()
                
            except Exception as e:
                st.error(f"Fout bij opslaan: {e}")

def _clear_draft():
    """Hulpfunctie om de session state leeg te maken"""
    keys_to_clear = [
        'draft_sector_nl', 'draft_sector_fr', 'draft_sector_en',
        'draft_title_nl', 'draft_title_fr', 'draft_title_en', 
        'draft_desc_nl', 'draft_desc_fr', 'draft_desc_en'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]