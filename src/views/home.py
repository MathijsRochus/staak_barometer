import streamlit as st
from src.utils.text import get_text
from src.backend.service import get_live_events, get_user_votes

def render_home():
    # --- SIDEBAR ---
    st.sidebar.markdown(f"**{get_text('sidebar_lang')}**")
    lang_options = ["nl", "fr", "en"]
    
    # Huidige taal selecteren
    current_index = 0
    if st.session_state.language in lang_options:
        current_index = lang_options.index(st.session_state.language)
    
    lang = st.sidebar.selectbox("Language", lang_options, index=current_index)
    st.session_state.language = lang
    
    # --- ADMIN CHECK ---
    # Haal de ingelogde gebruiker op
    user_email = ""
    if 'user' in st.session_state and st.session_state.user:
        user_email = st.session_state.user.email
    
    # Als het emailadres klopt, toon de knop
    if user_email == "mathijs.rochus@outlook.com":
        st.sidebar.divider()
        if st.sidebar.button("⚙️ Admin Panel", use_container_width=True):
            st.session_state.page = 'admin'
            st.rerun()
    
    st.sidebar.divider()

    # Logout knop
    if st.sidebar.button(get_text("btn_logout"), use_container_width=True):
        if 'session' in st.session_state: del st.session_state.session
        if 'user' in st.session_state: del st.session_state.user
        st.session_state.page = 'login'
        st.rerun()

    # --- MAIN CONTENT ---
    st.title(get_text("header_events"))
    st.write(get_text("sub_events"))

    # 1. Data ophalen (Events & Votes)
    events = get_live_events()
    
    user_votes = []
    if 'user' in st.session_state:
        # We halen de votes op van de gebruiker om de status te tonen
        user_votes = get_user_votes(st.session_state.user.id)
    
    # Maak een lijstje van ID's waar al op gestemd is
    voted_event_ids = [v['event_id'] for v in user_votes]

    # 2. Check of er events zijn
    if not events:
        st.info("Er zijn momenteel geen actieve stakingsevenementen gevonden in de database.")

    # 3. Render de Event Cards
    for event in events:
        # JSONB parsen: haal de juiste taal op, of fallback naar NL
        title = event['title'].get(lang, event['title'].get('nl', 'Geen titel'))
        desc = event['description'].get(lang, event['description'].get('nl', ''))
        
        # Sector logica: check of het JSON is of oude text
        raw_sector = event['sector']
        if isinstance(raw_sector, dict):
            sector_display = raw_sector.get(lang, raw_sector.get('nl', 'Onbekend'))
        else:
            sector_display = str(raw_sector)
        
        # Stemstatus bepalen
        has_voted = event['id'] in voted_event_ids
        status_label = get_text("status_voted") if has_voted else get_text("status_not_voted")
        
        # De kaart (Container)
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"{event['date']} - {title}")
                st.caption(f"{get_text('lbl_sector')}: {sector_display}")
                st.write(desc)
            with col2:
                # Status indicatie
                if has_voted:
                    st.success(status_label)
                else:
                    st.write(f"**{status_label}**")
                
                # De actieknop
                if st.button(get_text("btn_view_vote"), key=f"btn_{event['id']}", use_container_width=True):
                    st.session_state.selected_event = event
                    st.session_state.page = 'detail'
                    st.rerun()