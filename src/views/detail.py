import streamlit as st
import pandas as pd
import altair as alt  # <--- NEW IMPORT
from src.utils.text import get_text
from src.backend.service import get_user_votes, vote_for_event, get_event_stats

# De vote option keys
VOTE_KEYS = ["opt_strike_agree", "opt_strike_disagree", "opt_work_agree", "opt_work_disagree"]

def render_detail():
    # 1. security check
    event = st.session_state.get('selected_event')
    if not event:
        st.session_state.page = 'home'
        st.rerun()
        return

    lang = st.session_state.language
    user = st.session_state.user

    # 2. back button
    if st.button(get_text("btn_back")):
        st.session_state.page = 'home'
        st.rerun()

    # 3. Show event details
    title = event['title'].get(lang, event['title'].get('nl'))
    desc = event['description'].get(lang, event['description'].get('nl'))
    
    # Sector logic
    raw_sector = event['sector']
    if isinstance(raw_sector, dict):
        sector_display = raw_sector.get(lang, raw_sector.get('nl', ''))
    else:
        sector_display = str(raw_sector)

    st.title(title)
    st.markdown(f"**{get_text('lbl_date')}:** {event['date']} | **{get_text('lbl_sector')}:** {sector_display}")
    st.info(desc)
    
    st.divider()

    # 4. vote logic
    st.subheader(get_text("header_position"))
    st.write(get_text("desc_position"))

    # fetch current user's votes
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

    # 5. Show bar chart when voted
    if current_choice:
        render_chart(event['id'])

def render_chart(event_id):
    """Hulpfunctie om de grafiek te tekenen met custom kleuren en labels."""
    stats = get_event_stats(event_id)
    
    if stats:
        st.divider()
        st.markdown(f"### {get_text('chart_title')}")
        
        chart_data = []
        
        # KLEURENPALET: Een verloop van donkerrood naar licht (zoals het logo)
        # Pas deze hex-codes aan als je ze nog dichter bij je logo wilt.
        color_map = {
            "opt_strike_agree": "#991b1b",    # Donkerrood (Darkest)
            "opt_strike_disagree": "#dc2626", # Rood (Medium)
            "opt_work_agree": "#fb923c",      # Oranje/Zalm (Light)
            "opt_work_disagree": "#fed7aa"    # Bleek (Pale)
        }
        
        for item in stats:
            key = item['choice']
            label = get_text(key)
            count = item['vote_count']
            
            # Kies de kleur op basis van de optie-sleutel
            color = color_map.get(key, "#FF4B4B")
            
            chart_data.append({
                "Option": label, 
                "Count": count,
                "Color": color  # We voegen de specifieke kleur toe aan de data
            })
        
        df = pd.DataFrame(chart_data)
        
        # --- ALTAIR CHART DEFINITIE ---
        
        # 1. De Basis (Assen en Data)
        base = alt.Chart(df).encode(
            x=alt.X('Option', axis=alt.Axis(labelAngle=0, title=None)), # Labels horizontaal
            y=alt.Y('Count', axis=None), # Verberg Y-as cijfers (want we zetten ze erboven)
            tooltip=['Option', 'Count']
        )

        # 2. De Balken (Met onze custom 'Color' kolom)
        bars = base.mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            color=alt.Color('Color', scale=None) # 'scale=None' zegt: gebruik de hex code letterlijk
        )
        
        # 3. De Cijfers (Tekst boven de balk)
        text = base.mark_text(
            align='center',
            baseline='bottom',
            dy=-5,            # Schuif 5 pixels omhoog
            fontSize=14,
            fontWeight='bold',
            color='#1E1E1E'   # Donkere tekst voor leesbaarheid
        ).encode(
            text='Count'
        )
        
        # 4. Combineer en toon
        st.altair_chart(bars + text, width='stretch')
        
    else:
        st.write("Nog geen stemmen.")
        