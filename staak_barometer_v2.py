import streamlit as st
import pandas as pd
import altair as alt
import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="StaakBarometer",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- UI TRANSLATIONS ---
UI_TRANSLATIONS = {
    "nl": {
        "welcome": "Welkom",
        "login_prompt": "Kies een naam om te beginnen",
        "btn_login": "Ga naar Barometer",
        "feed_title": "Aankomende Stakingen",
        "btn_vote": "Stem Nu",
        "btn_results": "Resultaten",
        "voted": "Gestemd",
        "vote_title": "Uw positie",
        "vote_instr": "Kies de optie die bij u past:",
        "confirm": "Stem Bevestigen",
        "success": "Uw stem is geregistreerd.",
        "back": "Terug",
        "admin": "Beheer",
        "opt_s_a": "Ik staak & ben AKKOORD",
        "opt_s_d": "Ik staak & ben NIET akkoord",
        "opt_w_a": "Ik werk & ben AKKOORD",
        "opt_w_d": "Ik werk & ben NIET akkoord"
    },
    "fr": {
        "welcome": "Bienvenue",
        "login_prompt": "Choisissez un nom pour commencer",
        "btn_login": "Entrer",
        "feed_title": "Événements à venir",
        "btn_vote": "Voter",
        "btn_results": "Résultats",
        "voted": "Voté",
        "vote_title": "Votre position",
        "vote_instr": "Choisissez l'option qui vous correspond :",
        "confirm": "Confirmer",
        "success": "Votre vote a été enregistré.",
        "back": "Retour",
        "admin": "Admin",
        "opt_s_a": "Je fais grève & D'ACCORD",
        "opt_s_d": "Je fais grève & PAS d'accord",
        "opt_w_a": "Je travaille & D'ACCORD",
        "opt_w_d": "Je travaille & PAS d'accord"
    },
    "en": {
        "welcome": "Welcome",
        "login_prompt": "Choose a name to start",
        "btn_login": "Enter Barometer",
        "feed_title": "Upcoming Events",
        "btn_vote": "Vote Now",
        "btn_results": "Results",
        "voted": "Voted",
        "vote_title": "Your Position",
        "vote_instr": "Select the option that fits you:",
        "confirm": "Confirm Vote",
        "success": "Your vote has been recorded.",
        "back": "Back",
        "admin": "Admin",
        "opt_s_a": "I strike & AGREE",
        "opt_s_d": "I strike & DISAGREE",
        "opt_w_a": "I work & AGREE",
        "opt_w_d": "I work & DISAGREE"
    }
}

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Poppins:wght@500;700&display=swap');

    /* GLOBAL VARIABLES */
    :root {
        --mint: #A8E6CF;
        --dark: #1a1523;
        --dark-light: #2d2438;
        --bg: #f8fafc;
    }

    /* GENERAL OVERRIDES */
    .stApp {
        background-color: var(--bg);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: var(--dark) !important;
    }

    /* CARD STYLING */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        padding: 1rem;
    }

    /* BUTTONS */
    .stButton button {
        border-radius: 0.75rem;
        font-weight: 600;
        border: none;
        transition: transform 0.1s;
    }
    .stButton button:hover {
        transform: scale(1.02);
    }
    
    /* Primary Button (Mint Green) */
    button[kind="primary"] {
        background-color: var(--mint) !important;
        color: var(--dark) !important; /* Fixed: Dark text on Green background */
        font-weight: 700;
        border: 1px solid #91dcb8 !important;
    }

    /* Secondary Button */
    button[kind="secondary"] {
        background-color: white;
        color: var(--dark);
        border: 1px solid #e2e8f0;
    }

    /* HEADER */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 2rem;
    }
    .brand-text {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: var(--dark);
        margin-top: 0.5rem;
    }

    /* STATUS PILLS */
    .status-pill {
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.2rem 0.5rem;
        border-radius: 99px;
        text-transform: uppercase;
    }
    .status-open { background-color: var(--mint); color: var(--dark); }
    .status-voted { background-color: var(--dark); color: white; }

</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'language' not in st.session_state: st.session_state.language = 'nl'
if 'username' not in st.session_state: st.session_state.username = ''
if 'selected_event' not in st.session_state: st.session_state.selected_event = None
if 'votes' not in st.session_state: st.session_state.votes = {} 

# --- DATA (Multi-language) ---
ALL_EVENTS = [
    # Event 1
    {"id": 1, "lang": "en", "date": "13 JAN", "sector": "Transport", "title": "Rail Strike", "desc": "National strike by railway staff.", "results": [10, 5, 45, 15]},
    {"id": 1, "lang": "nl", "date": "13 JAN", "sector": "Vervoer", "title": "Spoorstaking", "desc": "Nationale staking bij het spoor.", "results": [10, 5, 45, 15]},
    {"id": 1, "lang": "fr", "date": "13 JAN", "sector": "Transports", "title": "Grève SNCB", "desc": "Grève nationale des chemins de fer.", "results": [10, 5, 45, 15]},
    
    # Event 2
    {"id": 2, "lang": "en", "date": "16 DEC", "sector": "General", "title": "National Action", "desc": "Protest against budget cuts.", "results": [35, 5, 40, 20]},
    {"id": 2, "lang": "nl", "date": "16 DEC", "sector": "Algemeen", "title": "Nationale Actiedag", "desc": "Protest tegen besparingen.", "results": [35, 5, 40, 20]},
    {"id": 2, "lang": "fr", "date": "16 DEC", "sector": "Général", "title": "Action Nationale", "desc": "Protestation contre l'austérité.", "results": [35, 5, 40, 20]},
]

# --- HELPERS ---
def get_text(key):
    return UI_TRANSLATIONS[st.session_state.language].get(key, key)

def get_filtered_events():
    return [e for e in ALL_EVENTS if e['lang'] == st.session_state.language]

# --- SVG LOGO ---
def render_logo(size=60):
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none">
        <path d="M70 25C60 25 55 30 55 35C55 40 60 42 70 45C85 50 90 60 90 75C90 90 75 100 55 100C35 100 25 90 25 75H40C40 85 45 88 55 88C65 88 75 82 75 75C75 68 70 65 60 62C45 58 40 48 40 35C40 20 55 10 70 10C85 10 90 20 90 25H70Z" fill="#1a1523"/>
        <path d="M70 10V22" stroke="#A8E6CF" stroke-width="3"/> 
        <path d="M85 15L78 25" stroke="#A8E6CF" stroke-width="3"/>
        <path d="M55 15L62 25" stroke="#A8E6CF" stroke-width="3"/>
        <path d="M65 38 L70 14 L73 16 L68 40 Z" fill="#A8E6CF"/>
    </svg>
    """

def render_sidebar():
    with st.sidebar:
        st.write("⚙️ Language / Taal")
        lang = st.selectbox("Language", ["nl", "fr", "en"], index=["nl", "fr", "en"].index(st.session_state.language), label_visibility="collapsed")
        st.session_state.language = lang
        
        if st.session_state.username:
            st.divider()
            st.write(f"👤 {st.session_state.username}")
            if st.button("Logout"):
                st.session_state.username = ''
                st.session_state.page = 'login'
                st.rerun()

# --- PAGES ---

def page_login():
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; margin-top:50px; margin-bottom:30px;">
        {render_logo(100)}
        <h1 style="margin-top:20px;">StaakBarometer</h1>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"**{get_text('welcome')}**")
        username = st.text_input(get_text("login_prompt"), placeholder="Jean Dupont...")
        
        if st.button(get_text("btn_login"), type="primary", use_container_width=True):
            if username.strip():
                st.session_state.username = username
                st.session_state.page = 'feed'
                st.rerun()
            else:
                st.warning("Please enter a name.")

def page_feed():
    st.markdown(f"""
    <div class="header-container">
        {render_logo(50)}
        <div class="brand-text">staakbarometer</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {get_text('feed_title')}")
    
    events = get_filtered_events()
    
    for event in events:
        has_voted = event['id'] in st.session_state.votes
        
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.caption(f"{event['sector'].upper()}")
                st.markdown(f"**{event['title']}**")
            with c2:
                st.markdown(f"**{event['date']}**")
            
            st.write(event['desc'])
            
            if has_voted:
                st.markdown(f'<span class="status-pill status-voted">✓ {get_text("voted")}</span>', unsafe_allow_html=True)
                if st.button(f"{get_text('btn_results')}", key=f"res_{event['id']}", use_container_width=True):
                    st.session_state.selected_event = event
                    st.session_state.page = 'results'
                    st.rerun()
            else:
                st.markdown(f'<span class="status-pill status-open">{get_text("btn_vote")}</span>', unsafe_allow_html=True)
                if st.button(f"→ {get_text('btn_vote')}", key=f"vote_{event['id']}", type="primary", use_container_width=True):
                    st.session_state.selected_event = event
                    st.session_state.page = 'vote'
                    st.rerun()
    
    st.divider()
    # Bottom Nav
    c1, c2, c3 = st.columns([1,1,1])
    with c1: st.button("🏠", use_container_width=True, disabled=True)
    with c3: 
        if st.button("⚙️", use_container_width=True):
            st.session_state.page = 'admin'
            st.rerun()

def page_vote():
    evt = st.session_state.selected_event
    
    if st.button(f"← {get_text('back')}"):
        st.session_state.page = 'feed'
        st.rerun()
        
    st.progress(50)
    st.caption(f"{evt['date']} • {evt['sector']}")
    st.title(evt['title'])
    
    st.markdown(f"### {get_text('vote_title')}")
    st.write(get_text('vote_instr'))
    
    # Voting Buttons
    if st.button(f"🔴 {get_text('opt_s_a')}", use_container_width=True): register_vote(evt['id'], 0)
    if st.button(f"🟠 {get_text('opt_s_d')}", use_container_width=True): register_vote(evt['id'], 1)
    if st.button(f"🔵 {get_text('opt_w_a')}", use_container_width=True): register_vote(evt['id'], 2)
    if st.button(f"🟢 {get_text('opt_w_d')}", use_container_width=True): register_vote(evt['id'], 3)

def register_vote(evt_id, choice):
    st.session_state.votes[evt_id] = choice
    st.session_state.page = 'results'
    st.rerun()

def page_results():
    evt = st.session_state.selected_event
    if st.button(f"← {get_text('back')}"):
        st.session_state.page = 'feed'
        st.rerun()
        
    st.title(evt['title'])
    st.success(f"✓ {get_text('success')}")
    
    data = pd.DataFrame({
        'Option': [get_text('opt_s_a'), get_text('opt_s_d'), get_text('opt_w_a'), get_text('opt_w_d')],
        'Votes': evt['results'],
        'Color': ['#dc2626', '#ea580c', '#2563eb', '#16a34a']
    })
    
    c = alt.Chart(data).mark_bar(cornerRadius=5).encode(
        x=alt.X('Option', axis=None),
        y=alt.Y('Votes', title=None),
        color=alt.Color('Color', scale=None),
        tooltip=['Option', 'Votes']
    ).properties(height=250)
    
    st.altair_chart(c, use_container_width=True)

def page_admin():
    # --- ADMIN CSS FIXES ---
    # We inject specific CSS just for this page to handle the dark mode contrast
    st.markdown("""
    <style>
        /* Force App Background to Dark for Admin */
        .stApp { background-color: #1a1523 !important; }
        
        /* White text for Headings */
        h1, h2, h3, p, label, span { color: white !important; }
        
        /* Fix Input Fields (Dark background, White text) */
        .stTextInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] > div { 
            background-color: #2d2438 !important; 
            color: white !important; 
            border: 1px solid #444 !important; 
        }
        
        /* Fix Dropdown options */
        ul[data-baseweb="menu"] {
            background-color: #2d2438 !important;
        }
        li[data-baseweb="option"] {
            color: white !important;
        }

        /* Fix Card Background in Admin */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #2d2438 !important;
            border-color: #444 !important;
        }
        
        /* Fix Button Visibility in Admin */
        button[kind="secondary"] {
            background-color: #444 !important;
            color: white !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button(get_text("back")):
            st.session_state.page = 'feed'
            st.rerun()
    with c2:
        st.markdown(f"<h3 style='margin-top:0'>{get_text('admin')} Panel</h3>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**Create Event**")
        st.text_input("Title", placeholder="Event Title...")
        c1, c2 = st.columns(2)
        with c1: st.date_input("Date")
        with c2: st.selectbox("Sector", ["General", "Transport", "Health"])
        
        # Primary button handles its own color via previous global CSS, 
        # but we ensure it pops against the dark bg
        st.button("Save Draft", type="primary", use_container_width=True)

# --- MAIN EXECUTION ---
render_sidebar()

if st.session_state.page == 'login':
    page_login()
elif st.session_state.page == 'feed':
    page_feed()
elif st.session_state.page == 'vote':
    page_vote()
elif st.session_state.page == 'results':
    page_results()
elif st.session_state.page == 'admin':
    page_admin()