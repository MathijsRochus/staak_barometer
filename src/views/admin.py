import streamlit as st
import datetime
import math
from src.backend.service import create_event, get_all_events, update_event, update_event_status

def render_admin():
    # --- CONFIG ---
    if 'admin_lang' not in st.session_state:
        st.session_state.admin_lang = 'en'
    
    # State management
    if 'admin_mode' not in st.session_state: st.session_state.admin_mode = 'list'
    if 'edit_event_data' not in st.session_state: st.session_state.edit_event_data = None
    
    # Pagination State
    if 'admin_page_idx' not in st.session_state: st.session_state.admin_page_idx = 0
    if 'admin_rows_per_page' not in st.session_state: st.session_state.admin_rows_per_page = 10

    # --- HEADER & NAVIGATION ---
    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if st.button("← Back"):
            st.session_state.page = 'home'
            st.rerun()
    with c2:
         st.markdown(f"<h2 style='text-align: center;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    with c3:
        pass # Language button removed as requested

    st.divider()

    # --- ROUTING ---
    if st.session_state.admin_mode == 'list':
        render_list_view()
    else:
        render_form_view()

def toggle_status_callback(event_id, current_val):
    """Callback to update DB directly when toggle changes."""
    new_status = not current_val
    update_event_status(event_id, new_status)
    status_text = 'Active' if new_status else 'Inactive'
    st.toast(f"Status changed to {status_text}")

def render_list_view():
    # --- TOP ACTIONS ---
    c1, c2 = st.columns([5, 2])
    with c1:
        st.markdown("### All Events")
    with c2:
        if st.button("➕ Create New Event", type="primary", use_container_width=True):
            st.session_state.edit_event_data = None
            st.session_state.admin_mode = 'form'
            st.rerun()
    
    st.markdown("---")

    # --- FETCH DATA ---
    all_events = get_all_events()
    if not all_events:
        st.info("No events found.")
        return

    # --- FILTER & SORT UI ---
    col_search, col_filter, col_sort, col_size = st.columns([2, 1, 1.5, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search", placeholder="Title or Sector...", key="admin_search").lower()
    
    with col_filter:
        filter_status = st.selectbox("Status", ["All", "Active", "Inactive"], key="admin_filter_status")
    
    with col_sort:
        sort_option = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Title (A-Z)", "Title (Z-A)"], key="admin_sort")
        
    with col_size:
        # Update session state directly when this changes
        rpp = st.selectbox("Rows", [5, 10, 25, 50], index=1, key="admin_rpp_select")
        st.session_state.admin_rows_per_page = rpp

    # --- APPLY LOGIC ---
    
    # 1. Filtering
    filtered_events = []
    for e in all_events:
        # Search Text
        t_nl = e['title'].get('nl', '').lower()
        s_val = e.get('sector', '')
        if isinstance(s_val, dict): s_val = s_val.get('nl', '')
        s_val = str(s_val).lower()
        
        text_match = (search_query in t_nl) or (search_query in s_val)
        
        # Filter Status
        is_active = e.get('is_active', True)
        status_match = True
        if filter_status == "Active" and not is_active: status_match = False
        if filter_status == "Inactive" and is_active: status_match = False
        
        if text_match and status_match:
            filtered_events.append(e)

    # 2. Sorting
    if "Date" in sort_option:
        reverse = "Newest" in sort_option
        filtered_events.sort(key=lambda x: x['date'], reverse=reverse)
    elif "Title" in sort_option:
        reverse = "Z-A" in sort_option
        filtered_events.sort(key=lambda x: x['title'].get('nl', '').lower(), reverse=reverse)

    # 3. Pagination Logic
    total_items = len(filtered_events)
    page_size = st.session_state.admin_rows_per_page
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
    
    # Ensure current page is valid (e.g. if we filtered down to fewer pages)
    if st.session_state.admin_page_idx >= total_pages:
        st.session_state.admin_page_idx = max(0, total_pages - 1)
        
    current_page = st.session_state.admin_page_idx
    start_idx = current_page * page_size
    end_idx = start_idx + page_size
    
    visible_events = filtered_events[start_idx:end_idx]

    # --- TABLE HEADER ---
    st.markdown("###") # Spacer
    h1, h2, h3, h4, h5 = st.columns([1.2, 3, 2, 1.5, 1])
    h1.markdown("**Date**")
    h2.markdown("**Title (NL)**")
    h3.markdown("**Sector**")
    h4.markdown("**Live Status**")
    h5.markdown("**Action**")
    st.markdown("---")

    # --- TABLE ROWS ---
    if not visible_events:
        st.warning("No events match your filters.")
    
    for event in visible_events:
        c1, c2, c3, c4, c5 = st.columns([1.2, 3, 2, 1.5, 1])
        
        # 1. Date
        c1.write(event['date'])
        
        # 2. Title
        title = event['title'].get('nl', 'No title')
        c2.write(title)
        
        # 3. Sector
        sec_raw = event.get('sector', '')
        sector_show = sec_raw.get('nl', '') if isinstance(sec_raw, dict) else str(sec_raw)
        c3.write(sector_show)
        
        # 4. Status Toggle
        is_active = event.get('is_active', True)
        c4.toggle(
            "Active" if is_active else "Inactive", 
            value=is_active, 
            key=f"toggle_{event['id']}",
            on_change=toggle_status_callback,
            args=(event['id'], is_active)
        )
        
        # 5. Edit
        if c5.button("✏️", key=f"btn_edit_{event['id']}"):
            st.session_state.edit_event_data = event
            st.session_state.admin_mode = 'form'
            st.rerun()

    # --- PAGINATION CONTROLS ---
    st.markdown("---")
    p1, p2, p3 = st.columns([1, 2, 1])
    
    with p1:
        if current_page > 0:
            if st.button("Previous", use_container_width=True):
                st.session_state.admin_page_idx -= 1
                st.rerun()

    with p2:
        st.markdown(f"<p style='text-align: center; line-height: 2.3;'>Page <b>{current_page + 1}</b> of <b>{total_pages}</b> ({total_items} events)</p>", unsafe_allow_html=True)

    with p3:
        if current_page < total_pages - 1:
            if st.button("Next", use_container_width=True):
                st.session_state.admin_page_idx += 1
                st.rerun()

def render_form_view():
    event_data = st.session_state.edit_event_data
    is_edit = event_data is not None
    
    st.subheader("Edit Event" if is_edit else "New Event")
    
    if st.button("Cancel", key="cancel_edit"):
        st.session_state.admin_mode = 'list'
        st.rerun()

    def get_val(key, default=""): 
        return event_data.get(key, default) if is_edit else default
    
    def get_json(field, lang):
        if not is_edit: return ""
        val = event_data.get(field, {})
        if isinstance(val, str) and field == 'sector': return val if lang == 'nl' else ""
        return val.get(lang, "") if isinstance(val, dict) else ""

    with st.form("admin_form"):
        col_d, col_empty = st.columns(2)
        
        default_date = datetime.date.today()
        if is_edit and event_data.get('date'):
            try: default_date = datetime.datetime.strptime(event_data['date'], '%Y-%m-%d').date()
            except: pass
            
        with col_d:
            date_val = st.date_input("Date", value=default_date)

        st.markdown("#### 1. Sector (Translated)")
        sc1, sc2, sc3 = st.columns(3)
        s_nl = sc1.text_input("Sector NL", value=get_json("sector", "nl"))
        s_fr = sc2.text_input("Sector FR", value=get_json("sector", "fr"))
        s_en = sc3.text_input("Sector EN", value=get_json("sector", "en"))

        st.markdown("#### 2. Title (Translated)")
        tc1, tc2, tc3 = st.columns(3)
        t_nl = tc1.text_input("Title NL", value=get_json("title", "nl"))
        t_fr = tc2.text_input("Title FR", value=get_json("title", "fr"))
        t_en = tc3.text_input("Title EN", value=get_json("title", "en"))

        st.markdown("#### 3. Description (Translated)")
        dc1, dc2, dc3 = st.columns(3)
        d_nl = dc1.text_area("Description NL", value=get_json("description", "nl"), height=100)
        d_fr = dc2.text_area("Description FR", value=get_json("description", "fr"), height=100)
        d_en = dc3.text_area("Description EN", value=get_json("description", "en"), height=100)

        submitted = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
        
        if submitted:
            sector_json = {"nl": s_nl, "fr": s_fr, "en": s_en}
            title_json = {"nl": t_nl, "fr": t_fr, "en": t_en}
            desc_json = {"nl": d_nl, "fr": d_fr, "en": d_en}
            
            try:
                if is_edit:
                    update_event(event_data['id'], date_val, sector_json, title_json, desc_json)
                    st.success("Event updated!")
                else:
                    create_event(date_val, sector_json, title_json, desc_json, active=True)
                    st.success("Event created!")
                
                st.session_state.admin_mode = 'list'
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")