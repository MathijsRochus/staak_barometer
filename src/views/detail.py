import streamlit as st
import pandas as pd
from src.utils.text import get_text
from src.backend.service import get_user_votes, vote_for_event, get_event_stats

# De sleutels voor de stemopties
VOTE_KEYS = ["opt_strike_agree", "opt_strike_disagree", "opt_work_agree", "opt_work_disagree"]

def render_detail():
    # 1. Veiligheidscheck
    event = st.session_state.get('selected_event')
    if not event:
        st.session_state.page = 'home'
        st.rerun()
        return

    lang = st.session_state.language
    user = st.session_state.user

    # 2. Terug knop
    if st.button(get_text("btn_back")):
        st.session_state.page = 'home'
        st.rerun()

    # 3. Details tonen
    title = event['title'].get(lang, event['title'].get('nl'))
    desc = event['description'].get(lang, event['description'].get('nl'))
    
    # Sector logica: check of het JSON is of oude text
    raw_sector = event['sector']
    if isinstance(raw_sector, dict):
        sector_display = raw_sector.get(lang, raw_sector.get('nl', ''))
    else:
        sector_display = str(raw_sector)

    st.title(title)
    st.markdown(f"**{get_text('lbl_date')}:** {event['date']} | **{get_text('lbl_sector')}:** {sector_display}")
    st.info(desc)
    
    st.divider()

    # 4. Stem Logica
    st.subheader(get_text("header_position"))
    st.write(get_text("desc_position"))

    # Huidige stem ophalen
    my_votes = get_user_votes(user.id)
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
            try:
                vote_for_event(user.id, event['id'], selected_key)
                st.success(get_text("success_vote"))
                st.rerun()
            except Exception as e:
                if "duplicate key" in str(e) or "violates unique constraint" in str(e):
                    st.error(get_text("error_vote_exists"))
                else:
                    st.error(f"Fout: {e}")

    # 5. Grafiek tonen (ALLEEN als er al gestemd is)
    if current_choice:
        render_chart(event['id'])

def render_chart(event_id):
    """Hulpfunctie om de grafiek te tekenen"""
    stats = get_event_stats(event_id)
    
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
        st.write("Nog geen stemmen.")