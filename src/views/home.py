import streamlit as st
from datetime import datetime, date
from PIL import Image
from src.utils.text import get_text
# Make sure your service.py fetches ALL events for the archive to work
from src.backend.service import get_all_events, get_user_votes 

def render_home():
    # --- SIDEBAR ---
    st.sidebar.markdown(f"**{get_text('sidebar_lang')}**")
    lang_options = ["nl", "fr", "en"]
    
    # Safe index lookup
    current_index = 0
    if st.session_state.language in lang_options:
        current_index = lang_options.index(st.session_state.language)
    
    lang = st.sidebar.selectbox("Language", lang_options, index=current_index)
    st.session_state.language = lang
    
    # Logout button
    if st.sidebar.button(get_text("btn_logout")):
        if 'session' in st.session_state: del st.session_state.session
        if 'user' in st.session_state: del st.session_state.user
        st.session_state.page = 'login'
        st.rerun()

    # --- MAIN CONTENT ---
    try:
        logo_img = Image.open("src/assets/logo.png")
        st.set_page_config(page_title="De Staak Barometer", page_icon=logo_img, layout="centered")
    except Exception:
        pass # Fallback if config is already set

    st.title(get_text("header_events"))
    st.write(get_text("sub_events"))

    # 1. Fetch Data
    # Note: Ensure get_live_events() in service.py does NOT filter by date, 
    # otherwise the archive will be empty.
    all_events = get_all_events()
    
    user_votes = []
    if 'user' in st.session_state:
        user_votes = get_user_votes(st.session_state.user.id)
    
    voted_event_ids = [v['event_id'] for v in user_votes]

    # 2. Filter Events (Active vs Past)
    today = date.today()
    active_events = []
    past_events = []

    for e in all_events:
        try:
            # Parse date string "YYYY-MM-DD"
            e_date = datetime.strptime(e['date'], '%Y-%m-%d').date()
            if e_date >= today:
                active_events.append(e)
            else:
                past_events.append(e)
        except ValueError:
            # Fallback if date parsing fails, treat as active
            active_events.append(e)

    # 3. Render Tabs
    # Ensure you added 'tab_active' and 'tab_archive' to src/utils/text.py 
    # If not, these will fallback to the key names.
    tab_active, tab_archive = st.tabs([get_text("tab_active"), get_text("tab_archive")])

    def render_event_list(events_to_show, is_archive=False):
        if not events_to_show:
            st.info("Geen evenementen / No events.")
            return

        for event in events_to_show:
            # Handle Title/Description translations
            title = event['title'].get(lang, event['title'].get('nl', 'Geen titel'))
            desc = event['description'].get(lang, event['description'].get('nl', ''))
            
            # --- FIX: Handle Sector (JSON vs String) ---
            sector_raw = event.get('sector', '')
            if isinstance(sector_raw, dict):
                # If it's a dict (JSON), get the language
                sector = sector_raw.get(lang, sector_raw.get('nl', ''))
            else:
                # If it's a simple string, use it directly
                sector = sector_raw
            
            has_voted = event['id'] in voted_event_ids
            
            # Determine status label
            if is_archive:
                status_label = get_text("status_closed")
            else:
                status_label = get_text("status_voted") if has_voted else get_text("status_not_voted")
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{event['date']} - {title}")
                    st.caption(f"{get_text('lbl_sector')}: {sector}")
                    st.write(desc)
                with col2:
                    st.write(f"**{status_label}**")
                    if st.button(get_text("btn_view_vote"), key=f"btn_{event['id']}", width='stretch'):
                        st.session_state.selected_event = event
                        st.session_state.page = 'detail'
                        st.rerun()

    # Fill the tabs
    with tab_active:
        render_event_list(active_events, is_archive=False)
    
    with tab_archive:
        render_event_list(past_events, is_archive=True)

    # --- RESTORED: BOTTOM NAVIGATION (Admin Access) ---
    st.divider()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: 
        # Home button (disabled since we are here)
        st.button("🏠", width='stretch', disabled=True)
    with c3: 
        # Admin/Settings button
        if st.button("⚙️", width='stretch'):
            st.session_state.page = 'admin'
            st.rerun()