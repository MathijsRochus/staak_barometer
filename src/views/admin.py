import streamlit as st
from src.backend.service import create_event
import datetime

def render_admin():
    st.title("Admin: Nieuw Event (Draft)")

    # 1. State Management (Voorbereiding op AI invullen)
    # We initialiseren de session_state variabelen als ze nog niet bestaan.
    # Dit zorgt ervoor dat een externe API (Gemini) deze variabelen kan vullen.
    if 'draft_date' not in st.session_state: st.session_state.draft_date = datetime.date.today()
    if 'draft_sector' not in st.session_state: st.session_state.draft_sector = ""
    if 'draft_title_nl' not in st.session_state: st.session_state.draft_title_nl = ""
    if 'draft_title_fr' not in st.session_state: st.session_state.draft_title_fr = ""
    if 'draft_title_en' not in st.session_state: st.session_state.draft_title_en = ""
    if 'draft_desc_nl' not in st.session_state: st.session_state.draft_desc_nl = ""
    if 'draft_desc_fr' not in st.session_state: st.session_state.draft_desc_fr = ""
    if 'draft_desc_en' not in st.session_state: st.session_state.draft_desc_en = ""

    # 2. Terug knop
    if st.button("← Terug naar Home"):
        _clear_draft() # Optioneel: draft wissen bij teruggaan?
        st.session_state.page = 'home'
        st.rerun()

    # 3. "Vul met AI" Placeholder (Toekomst)
    with st.expander("✨ AI Assistent (Toekomst)"):
        st.info("Hier komt een knop om op basis van een URL of nieuwsartikel de velden hieronder automatisch te vullen via Gemini.")
        # Voorbeeld hoe dit zou werken:
        if st.button("Simuleer Gemini Call (Test)"):
            st.session_state.draft_sector = "Openbaar Vervoer"
            st.session_state.draft_title_nl = "Landelijke Staking NMBS"
            st.session_state.draft_desc_nl = "Het treinverkeer zal zwaar verstoord zijn door een 24-uurs staking."
            st.rerun()

    # 4. Het Formulier
    with st.form("draft_form"):
        st.subheader("Details")
        # Belangrijk: gebruik 'value' gekoppeld aan session_state
        date = st.date_input("Datum", value=st.session_state.draft_date)
        sector = st.text_input("Sector", value=st.session_state.draft_sector)
        
        st.subheader("Titels")
        t_nl = st.text_input("Titel NL", value=st.session_state.draft_title_nl)
        t_fr = st.text_input("Titel FR", value=st.session_state.draft_title_fr)
        t_en = st.text_input("Titel EN", value=st.session_state.draft_title_en)
        
        st.subheader("Beschrijving")
        d_nl = st.text_area("Beschrijving NL", value=st.session_state.draft_desc_nl)
        d_fr = st.text_area("Beschrijving FR", value=st.session_state.draft_desc_fr)
        d_en = st.text_area("Beschrijving EN", value=st.session_state.draft_desc_en)
        
        # 5. Save & Redirect
        submitted = st.form_submit_button("Event Aanmaken & Publiceren")
        
        if submitted:
            # JSON objecten bouwen
            title_json = {"nl": t_nl, "fr": t_fr, "en": t_en}
            desc_json = {"nl": d_nl, "fr": d_fr, "en": d_en}
            
            try:
                create_event(date, sector, title_json, desc_json)
                st.success("Event succesvol aangemaakt!")
                
                # Draft opschonen
                _clear_draft()
                
                # Redirect
                st.session_state.page = 'home'
                st.rerun()
                
            except Exception as e:
                st.error(f"Fout bij opslaan: {e}")

def _clear_draft():
    """Hulpfunctie om de session state leeg te maken na opslaan"""
    keys_to_clear = [
        'draft_sector', 'draft_title_nl', 'draft_title_fr', 'draft_title_en', 
        'draft_desc_nl', 'draft_desc_fr', 'draft_desc_en'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]