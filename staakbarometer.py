import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- CONFIGURATION ---
st.set_page_config(page_title="De Staak Barometer", page_icon="📊", layout="centered")

# --- SUPABASE SETUP (CRUCIAAL VOOR RLS) ---
# We maken de client aan, maar cachen hem NIET globaal met auth state, 
# om te voorkomen dat gebruikers sessies mixen.
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_supabase()

# --- SESSIE HERSTEL ---
# Dit is de FIX voor je "RLS Error". 
# Bij elke herlading checken we: "Was deze gebruiker ingelogd?" 
# Zo ja, vertel het tegen Supabase zodat auth.uid() gevuld is.
if "session" in st.session_state:
    try:
        supabase.auth.set_session(
            st.session_state.session.access_token, 
            st.session_state.session.refresh_token
        )
    except Exception as e:
        # Als de sessie verlopen is, log uit
        st.warning("Sessie verlopen, log opnieuw in.")
        del st.session_state.session
        del st.session_state.user
        st.rerun()

# --- UI TRANSLATIONS (VOLLEDIG HERSTELD) ---
UI_TRANSLATIONS = {
    "nl": {
        "title": "📊 De Staak Barometer",
        "welcome_msg": "Welkom! Laat uw stem horen. Bent u de stille meerderheid?",
        "username_placeholder": "Email adres...",
        "btn_login": "Inloggen / Registreren",
        "btn_logout": "Uitloggen",
        "btn_back": "← Terug naar overzicht",
        "btn_view_vote": "Bekijk & Stem",
        "btn_confirm": "Stem Bevestigen",
        "sidebar_lang": "Kies Taal / Langue / Language",
        "status_voted": "✅ Gestemd",
        "status_not_voted": "⚪ Nog niet gestemd",
        "login_warning": "Vul een email en wachtwoord in.",
        "success_vote": "Uw mening is geregistreerd! Bedankt.",
        "error_vote_exists": "U heeft al gestemd voor dit event.",
        "header_events": "Recente Stakingsevenementen",
        "sub_events": "Selecteer een evenement om uw mening te geven.",
        "header_position": "Wat is uw positie?",
        "desc_position": "Kies de optie die het beste bij uw situatie past:",
        "chart_title": "Huidige Barometer (Live Data)",
        "opt_strike_agree": "Ik staak en ben akkoord",
        "opt_strike_disagree": "Ik staak en ben niet akkoord",
        "opt_work_agree": "Ik werk en ben akkoord",
        "opt_work_disagree": "Ik werk en ben niet akkoord",
        "lbl_date": "Datum",
        "lbl_sector": "Sector"
    },
    "fr": {
        "title": "📊 Le Baromètre de Grève",
        "welcome_msg": "Bienvenue! Faites entendre votre voix. Êtes-vous la majorité silencieuse?",
        "username_placeholder": "Adresse email...",
        "btn_login": "Se connecter / S'inscrire",
        "btn_logout": "Se déconnecter",
        "btn_back": "← Retour à l'aperçu",
        "btn_view_vote": "Voir & Voter",
        "btn_confirm": "Confirmer le vote",
        "sidebar_lang": "Kies Taal / Langue / Language",
        "status_voted": "✅ Voté",
        "status_not_voted": "⚪ Pas encore voté",
        "login_warning": "Veuillez entrer un email et un mot de passe.",
        "success_vote": "Votre opinion a été enregistrée! Merci.",
        "error_vote_exists": "Vous avez déjà voté pour cet événement.",
        "header_events": "Événements de grève récents",
        "sub_events": "Sélectionnez un événement pour donner votre avis.",
        "header_position": "Quelle est votre position?",
        "desc_position": "Choisissez l'option qui correspond le mieux à votre situation:",
        "chart_title": "Baromètre Actuel (Données en direct)",
        "opt_strike_agree": "Je fais grève et je suis d'accord",
        "opt_strike_disagree": "Je fais grève et je ne suis pas d'accord",
        "opt_work_agree": "Je travaille et je suis d'accord",
        "opt_work_disagree": "Je travaille et je ne suis pas d'accord",
        "lbl_date": "Date",
        "lbl_sector": "Secteur"
    },
    "en": {
        "title": "📊 The Strike Barometer",
        "welcome_msg": "Welcome! Make your voice heard. Are you the silent majority?",
        "username_placeholder": "Email address...",
        "btn_login": "Log In / Register",
        "btn_logout": "Log Out",
        "btn_back": "← Back to overview",
        "btn_view_vote": "View & Vote",
        "btn_confirm": "Confirm Vote",
        "sidebar_lang": "Kies Taal / Langue / Language",
        "status_voted": "✅ Voted",
        "status_not_voted": "⚪ Not voted yet",
        "login_warning": "Please enter an email and password.",
        "success_vote": "Your opinion has been registered! Thank you.",
        "error_vote_exists": "You have already voted for this event.",
        "header_events": "Recent Strike Events",
        "sub_events": "Select an event to share your opinion.",
        "header_position": "What is your position?",
        "desc_position": "Choose the option that fits your situation best:",
        "chart_title": "Current Barometer (Live Data)",
        "opt_strike_agree": "I strike and I agree",
        "opt_strike_disagree": "I strike and I disagree",
        "opt_work_agree": "I work and I agree",
        "opt_work_disagree": "I work and I disagree",
        "lbl_date": "Date",
        "lbl_sector": "Sector"
    }
}

# Keys for the voting options match what we store in DB
VOTE_KEYS = ["opt_strike_agree", "opt_strike_disagree", "opt_work_agree", "opt_work_disagree"]

# --- HELPER FUNCTIONS ---
def get_text(key):
    lang = st.session_state.get('language', 'nl')
    texts = UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS['nl'])
    return texts.get(key, key)

def get_live_events():
    """Haalt events op uit Supabase"""
    try:
        response = supabase.table("events").select("*").order("date", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Connectiefout events: {e}")
        return []

def get_user_votes():
    """Haalt op waar de huidige gebruiker al op gestemd heeft"""
    if 'user' not in st.session_state:
        return []
    try:
        user_id = st.session_state.user.id
        response = supabase.table("votes").select("event_id, choice").eq("user_id", user_id).execute()
        return response.data
    except Exception:
        return []

def get_event_stats(event_id):
    """Haalt de totalen op uit de VIEW"""
    try:
        response = supabase.table("event_results").select("*").eq("event_id", event_id).execute()
        return response.data
    except Exception:
        return []

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'language' not in st.session_state: st.session_state.language = 'nl'
if 'selected_event' not in st.session_state: st.session_state.selected_event = None

# --- AUTH FUNCTION ---
def handle_login(email, password):
    try:
        # Probeer in te loggen
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # CRUCIAAL: Sla de HELE sessie op, niet alleen de user
        st.session_state.session = response.session
        st.session_state.user = response.user
        st.session_state.page = 'home'
        
    except Exception as e:
        # Als inloggen faalt, proberen we te registreren
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user and response.session:
                st.session_state.session = response.session
                st.session_state.user = response.user
                st.session_state.page = 'home'
                st.success("Account aangemaakt en ingelogd!")
            elif response.user and not response.session:
                 st.info("Registratie gelukt! Controleer uw email om te bevestigen.")
            else:
                st.error("Registratie mislukt.")
        except Exception as reg_error:
            st.error(f"Fout: {reg_error}")

# --- PAGES ---

def show_login_page():
    st.markdown(f"<h1 style='text-align: center;'>{get_text('title')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(get_text("welcome_msg"))
        email = st.text_input("Email", placeholder=get_text("username_placeholder"))
        password = st.text_input("Password", type="password", placeholder="*****")
        
        if st.button(get_text("btn_login"), use_container_width=True):
            if email and password:
                handle_login(email, password)
                st.rerun()
            else:
                st.warning(get_text("login_warning"))

def show_home_page():
    # Sidebar
    st.sidebar.markdown(f"**{get_text('sidebar_lang')}**")
    lang_options = ["nl", "fr", "en"]
    # Veilige index lookup
    current_index = 0
    if st.session_state.language in lang_options:
        current_index = lang_options.index(st.session_state.language)
        
    lang = st.sidebar.selectbox("Language", lang_options, index=current_index)
    st.session_state.language = lang
    
    if st.sidebar.button(get_text("btn_logout")):
        supabase.auth.sign_out()
        if 'user' in st.session_state: del st.session_state.user
        if 'session' in st.session_state: del st.session_state.session
        st.session_state.page = 'login'
        st.rerun()

    # Main Content
    st.title(get_text("header_events"))
    st.write(get_text("sub_events"))
    
    events = get_live_events()
    my_votes = get_user_votes()
    voted_event_ids = [v['event_id'] for v in my_votes]

    if not events:
        st.warning("Geen evenementen gevonden in de database.")

    for event in events:
        # JSONB parsen
        title = event['title'].get(lang, event['title'].get('nl', 'Geen titel'))
        desc = event['description'].get(lang, event['description'].get('nl', ''))
        
        has_voted = event['id'] in voted_event_ids
        status_label = get_text("status_voted") if has_voted else get_text("status_not_voted")
        
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(f"{event['date']} - {title}")
                st.caption(f"{get_text('lbl_sector')}: {event['sector']}")
                st.write(desc)
            with c2:
                st.write(f"**{status_label}**")
                if st.button(get_text("btn_view_vote"), key=f"btn_{event['id']}", use_container_width=True):
                    st.session_state.selected_event = event
                    st.session_state.page = 'detail'
                    st.rerun()

def show_detail_page():
    event = st.session_state.selected_event
    lang = st.session_state.language
    
    if st.button(get_text("btn_back")):
        st.session_state.page = 'home'
        st.rerun()

    if event:
        title = event['title'].get(lang, event['title'].get('nl'))
        desc = event['description'].get(lang, event['description'].get('nl'))

        st.title(title)
        st.info(desc)
        
        st.divider()
        st.subheader(get_text("header_position"))
        st.write(get_text("desc_position"))
        
        my_votes = get_user_votes()
        current_choice = next((v['choice'] for v in my_votes if v['event_id'] == event['id']), None)
        
        options_map = {k: get_text(k) for k in VOTE_KEYS}
        reverse_map = {v: k for k, v in options_map.items()}
        
        index = 0
        if current_choice and current_choice in VOTE_KEYS:
            index = VOTE_KEYS.index(current_choice)
            st.success(get_text("status_voted"))

        with st.form("voting_form"):
            selection_label = st.radio("Keuze", list(options_map.values()), index=index)
            submitted = st.form_submit_button(get_text("btn_confirm"))
            
            if submitted:
                selected_key = reverse_map[selection_label]
                user_id = st.session_state.user.id
                
                try:
                    # Insert met de juiste user_id
                    supabase.table("votes").insert({
                        "user_id": user_id,
                        "event_id": event['id'],
                        "choice": selected_key
                    }).execute()
                    
                    st.success(get_text("success_vote"))
                    st.rerun()
                    
                except Exception as e:
                    if "duplicate key" in str(e) or "violates unique constraint" in str(e):
                        st.error(get_text("error_vote_exists"))
                    else:
                        st.error(f"Fout details: {e}")

        # --- GRAFIEK ---
        stats = get_event_stats(event['id'])
        
        if stats:
            st.divider()
            st.markdown(f"### {get_text('chart_title')}")
            
            chart_data = []
            for item in stats:
                label = get_text(item['choice'])
                count = item['vote_count']
                chart_data.append({"Option": label, "Count": count})
            
            df = pd.DataFrame(chart_data)
            st.bar_chart(df, x="Option", y="Count", color="#FF4B4B")
        else:
            st.write("Nog geen stemmen / Pas encore de votes.")

# --- MAIN ---
if 'user' not in st.session_state:
    st.session_state.page = 'login'

if st.session_state.page == 'login':
    show_login_page()
elif st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'detail':
    show_detail_page()