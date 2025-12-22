import streamlit as st
from src.utils.text import get_text
from src.backend.service import get_live_events, get_user_votes
from src.utils.ui import load_custom_css
from PIL import Image # <--- VOEG DIT TOE bovenaan bij je imports


def render_home():
    # --- SIDEBAR ---
    st.sidebar.markdown(f"**{get_text('sidebar_lang')}**")
    lang_options = ["nl", "fr", "en"]
    
    # Veilige index lookup
    current_index = 0
    if st.session_state.language in lang_options:
        current_index = lang_options.index(st.session_state.language)
    
    lang = st.sidebar.selectbox("Language", lang_options, index=current_index)
    st.session_state.language = lang
    
    # Logout knop
    if st.sidebar.button(get_text("btn_logout")):
        if 'session' in st.session_state: del st.session_state.session
        if 'user' in st.session_state: del st.session_state.user
        st.session_state.page = 'login'
        st.rerun()

    # --- MAIN CONTENT ---
    st.title(get_text("header_events"))
    st.write(get_text("sub_events"))

    # 1. Config
    # Laad het logo in het geheugen
    logo_img = Image.open("src/assets/logo.png")

    st.set_page_config(
    page_title="De Staak Barometer", 
    page_icon=logo_img,  # <--- HIER GEBRUIK JE DE AFBEELDING
    layout="centered"
    )
    # 2. Data ophalen
    events = get_live_events()
    
    # 3. Checken of er user votes zijn (zodat we kunnen zien of je al gestemd hebt)
    # We halen de user uit de sessie als die bestaat
    user_votes = []
    if 'user' in st.session_state:
        user_votes = get_user_votes(st.session_state.user.id)
    
    voted_event_ids = [v['event_id'] for v in user_votes]

    # Melding als er geen events zijn
    if not events:
        st.info("Er zijn momenteel geen actieve stakingsevenementen gevonden in de database.")

    # 4. De Loop (Hier worden de blokjes getekend)
    for event in events:
        # JSONB parsen: haal de juiste taal op, of fallback naar NL
        title = event['title'].get(lang, event['title'].get('nl', 'Geen titel'))
        desc = event['description'].get(lang, event['description'].get('nl', ''))
        
        has_voted = event['id'] in voted_event_ids
        status_label = get_text("status_voted") if has_voted else get_text("status_not_voted")
        
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"{event['date']} - {title}")
                st.caption(f"{get_text('lbl_sector')}: {event['sector']}")
                st.write(desc)
            with col2:
                st.write(f"**{status_label}**")
                # Knop om naar detail te gaan
                if st.button(get_text("btn_view_vote"), key=f"btn_{event['id']}", use_container_width=True):
                    st.session_state.selected_event = event
                    st.session_state.page = 'detail'
                    st.rerun()