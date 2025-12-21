import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="De Staak Barometer", page_icon="📊", layout="centered")

# --- UI TRANSLATIONS (Interface Text) ---
# This dictionary maps UI keys to text in Dutch (nl), French (fr), and English (en).
UI_TRANSLATIONS = {
    "nl": {
        "title": "📊 De Staak Barometer",
        "welcome_msg": "Welkom! Laat uw stem horen. Bent u de stille meerderheid?",
        "username_placeholder": "Typ uw naam...",
        "btn_login": "Inloggen",
        "btn_logout": "Uitloggen",
        "btn_back": "← Terug naar overzicht",
        "btn_view_vote": "Bekijk & Stem",
        "btn_confirm": "Stem Bevestigen",
        "sidebar_lang": "Kies Taal / Langue / Language",
        "status_voted": "✅ Gestemd",
        "status_not_voted": "⚪ Nog niet gestemd",
        "login_warning": "Vul alstublieft een naam in.",
        "success_vote": "Uw mening is geregistreerd! Bedankt.",
        "header_events": "Recente Stakingsevenementen",
        "sub_events": "Selecteer een evenement om uw mening te geven.",
        "header_position": "Wat is uw positie?",
        "desc_position": "Kies de optie die het beste bij uw situatie past:",
        "chart_title": "Huidige Barometer (Simulatie)",
        # Vote Options
        "opt_strike_agree": "Ik staak en ben akkoord",
        "opt_strike_disagree": "Ik staak en ben niet akkoord",
        "opt_work_agree": "Ik werk en ben akkoord",
        "opt_work_disagree": "Ik werk en ben niet akkoord",
        # Labels
        "lbl_date": "Datum",
        "lbl_sector": "Sector"
    },
    "fr": {
        "title": "📊 Le Baromètre de Grève",
        "welcome_msg": "Bienvenue! Faites entendre votre voix. Êtes-vous la majorité silencieuse?",
        "username_placeholder": "Entrez votre nom...",
        "btn_login": "Se connecter",
        "btn_logout": "Se déconnecter",
        "btn_back": "← Retour à l'aperçu",
        "btn_view_vote": "Voir & Voter",
        "btn_confirm": "Confirmer le vote",
        "sidebar_lang": "Kies Taal / Langue / Language",
        "status_voted": "✅ Voté",
        "status_not_voted": "⚪ Pas encore voté",
        "login_warning": "Veuillez entrer un nom.",
        "success_vote": "Votre opinion a été enregistrée! Merci.",
        "header_events": "Événements de grève récents",
        "sub_events": "Sélectionnez un événement pour donner votre avis.",
        "header_position": "Quelle est votre position?",
        "desc_position": "Choisissez l'option qui correspond le mieux à votre situation:",
        "chart_title": "Baromètre Actuel (Simulation)",
        # Vote Options
        "opt_strike_agree": "Je fais grève et je suis d'accord",
        "opt_strike_disagree": "Je fais grève et je ne suis pas d'accord",
        "opt_work_agree": "Je travaille et je suis d'accord",
        "opt_work_disagree": "Je travaille et je ne suis pas d'accord",
        # Labels
        "lbl_date": "Date",
        "lbl_sector": "Secteur"
    },
    "en": {
        "title": "📊 The Strike Barometer",
        "welcome_msg": "Welcome! Make your voice heard. Are you the silent majority?",
        "username_placeholder": "Type your name...",
        "btn_login": "Log In",
        "btn_logout": "Log Out",
        "btn_back": "← Back to overview",
        "btn_view_vote": "View & Vote",
        "btn_confirm": "Confirm Vote",
        "sidebar_lang": "Kies Taal / Langue / Language",
        "status_voted": "✅ Voted",
        "status_not_voted": "⚪ Not voted yet",
        "login_warning": "Please enter a name.",
        "success_vote": "Your opinion has been registered! Thank you.",
        "header_events": "Recent Strike Events",
        "sub_events": "Select an event to share your opinion.",
        "header_position": "What is your position?",
        "desc_position": "Choose the option that fits your situation best:",
        "chart_title": "Current Barometer (Simulation)",
        # Vote Options
        "opt_strike_agree": "I strike and I agree",
        "opt_strike_disagree": "I strike and I disagree",
        "opt_work_agree": "I work and I agree",
        "opt_work_disagree": "I work and I disagree",
        # Labels
        "lbl_date": "Date",
        "lbl_sector": "Sector"
    }
}

# --- EVENT DATA (Simulating DB Records) ---
# Here we simulate that every language version is a separate record.
# 'event_id' is the common key linking them together.
ALL_EVENTS = [
    # Event 1: National Strike (Dec 16)
    {"event_id": 1, "lang": "nl", "date": "2024-12-16", "title": "Nationale Staking", "sector": "Algemeen", "description": "Algemene actiedag tegen besparingsmaatregelen."},
    {"event_id": 1, "lang": "fr", "date": "2024-12-16", "title": "Grève Nationale", "sector": "Général", "description": "Journée d'action générale contre les mesures d'austérité."},
    {"event_id": 1, "lang": "en", "date": "2024-12-16", "title": "National Strike", "sector": "General", "description": "General action day against austerity measures."},

    # Event 2: Non-Profit (Nov 07)
    {"event_id": 2, "lang": "nl", "date": "2024-11-07", "title": "Betoging Non-Profit", "sector": "Zorg", "description": "Protest voor betere loon- en werkvoorwaarden."},
    {"event_id": 2, "lang": "fr", "date": "2024-11-07", "title": "Manif Non-Marchand", "sector": "Soins", "description": "Manifestation pour de meilleurs salaires et conditions de travail."},
    {"event_id": 2, "lang": "en", "date": "2024-11-07", "title": "Non-Profit Protest", "sector": "Care", "description": "Protest for better wages and working conditions."},

    # Event 3: Cleaning (Oct 01)
    {"event_id": 3, "lang": "nl", "date": "2024-10-01", "title": "Staking Schoonmaak", "sector": "Diensten", "description": "Actie voor respect en betere lonen."},
    {"event_id": 3, "lang": "fr", "date": "2024-10-01", "title": "Grève Nettoyage", "sector": "Services", "description": "Action pour le respect et de meilleurs salaires."},
    {"event_id": 3, "lang": "en", "date": "2024-10-01", "title": "Cleaning Strike", "sector": "Services", "description": "Action for respect and better pay."}
]

# Keys for the voting options
VOTE_KEYS = [
    "opt_strike_agree",
    "opt_strike_disagree",
    "opt_work_agree",
    "opt_work_disagree"
]

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'votes' not in st.session_state:
    st.session_state.votes = {}  # Format: {event_id: vote_key_string}
if 'language' not in st.session_state:
    st.session_state.language = 'nl' # Default language
if 'selected_event_id' not in st.session_state:
    st.session_state.selected_event_id = None

# --- HELPER FUNCTIONS ---

def get_text(key):
    """Retrieves the UI text for a specific key in the selected language."""
    lang = st.session_state.language
    return UI_TRANSLATIONS[lang].get(key, key)

def get_events_for_current_language():
    """Simulates a DB query: SELECT * FROM events WHERE lang = current_lang"""
    lang = st.session_state.language
    # Filter the big list based on the active language
    return [e for e in ALL_EVENTS if e['lang'] == lang]

def get_event_details(event_id):
    """Finds the specific event record for the current language and ID."""
    lang = st.session_state.language
    # Search for the event with matching ID and Language
    found = next((e for e in ALL_EVENTS if e['event_id'] == event_id and e['lang'] == lang), None)
    return found

# --- NAVIGATION FUNCTIONS ---
def navigate_to_home():
    st.session_state.page = 'home'

def navigate_to_event(event_id):
    st.session_state.selected_event_id = event_id
    st.session_state.page = 'detail'

def logout_user():
    st.session_state.page = 'login'
    st.session_state.username = ''

# --- UI COMPONENTS (Sidebar) ---
def render_sidebar():
    st.sidebar.markdown(f"**{get_text('sidebar_lang')}**")
    
    lang_options = ["nl", "fr", "en"]
    selected_lang = st.sidebar.selectbox(
        "Language",
        lang_options,
        index=lang_options.index(st.session_state.language),
        label_visibility="collapsed"
    )
    st.session_state.language = selected_lang

    if st.session_state.username:
        st.sidebar.markdown("---")
        st.sidebar.write(f"User: **{st.session_state.username}**")
        if st.sidebar.button(get_text("btn_logout")):
            logout_user()
            st.rerun()

# --- PAGES ---

def show_login_page():
    st.markdown(f"<h1 style='text-align: center;'>{get_text('title')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(get_text("welcome_msg"))
        username_input = st.text_input("Username", placeholder=get_text("username_placeholder"), label_visibility="collapsed")
        
        if st.button(get_text("btn_login"), use_container_width=True):
            if username_input:
                st.session_state.username = username_input
                navigate_to_home()
                st.rerun()
            else:
                st.warning(get_text("login_warning"))

def show_home_page():
    st.title(get_text("header_events"))
    st.write(get_text("sub_events"))
    
    # Get the events filtered by the selected language
    visible_events = get_events_for_current_language()
    
    for event in visible_events:
        # Check vote status using the event_id (which is shared across languages)
        has_voted = event['event_id'] in st.session_state.votes
        status_label = get_text("status_voted") if has_voted else get_text("status_not_voted")
        
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"{event['date']} - {event['title']}")
                st.caption(f"{get_text('lbl_sector')}: {event['sector']}")
                st.write(event['description'])
            with col2:
                st.write(f"**{status_label}**")
                if st.button(get_text("btn_view_vote"), key=f"btn_{event['event_id']}", use_container_width=True):
                    navigate_to_event(event['event_id'])
                    st.rerun()

def show_detail_page():
    event_id = st.session_state.selected_event_id
    
    # Fetch the event details in the correct language
    event = get_event_details(event_id)
    
    if st.button(get_text("btn_back")):
        navigate_to_home()
        st.rerun()

    if event:
        st.title(event['title'])
        st.markdown(f"**{get_text('lbl_date')}:** {event['date']} | **{get_text('lbl_sector')}:** {event['sector']}")
        st.info(event['description'])
        
        st.divider()
        
        st.subheader(get_text("header_position"))
        st.write(get_text("desc_position"))

        # Get current vote key (e.g., 'opt_strike_agree')
        current_vote_key = st.session_state.votes.get(event_id)
        
        # Translate options for display
        options_display = [get_text(k) for k in VOTE_KEYS]
        
        # Determine index of current vote
        current_index = 0
        if current_vote_key in VOTE_KEYS:
            current_index = VOTE_KEYS.index(current_vote_key)

        with st.form("voting_form"):
            selection = st.radio(
                "Radio",
                options_display,
                index=current_index,
                label_visibility="collapsed"
            )
            
            submitted = st.form_submit_button(get_text("btn_confirm"))
            
            if submitted:
                # Map back to key
                selected_index = options_display.index(selection)
                selected_key = VOTE_KEYS[selected_index]
                
                # Save vote using the generic event_id
                st.session_state.votes[event_id] = selected_key
                st.success(get_text("success_vote"))
                
        # --- VISUALIZATION ---
        if event_id in st.session_state.votes:
            st.divider()
            st.markdown(f"### {get_text('chart_title')}")
            
            # Dummy Data
            data = {
                "Option": options_display,
                "Count": [35, 5, 40, 20] 
            }
            df = pd.DataFrame(data)
            st.bar_chart(df, x="Option", y="Count", color="#FF4B4B")
    else:
        st.error("Event not found for this language.")

# --- MAIN EXECUTION ---

render_sidebar()

if st.session_state.page == 'login':
    show_login_page()
elif st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'detail':
    show_detail_page()