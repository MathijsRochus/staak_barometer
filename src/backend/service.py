import streamlit as st
from src.backend.client import supabase

def get_active_events():
    """Fetches events for the public page (active only)."""
    try:
        # Filter on is_active=True
        response = supabase.table("events").select("*").eq("is_active", True).order("date", desc=True).execute()
        return response.data
    except Exception as e:
        # st.error(f"Supabase Error: {e}") 
        return []

def get_all_events():
    """Fetches ALL events for the Admin (active and inactive)."""
    try:
        response = supabase.table("events").select("*").order("date", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Admin Fetch Error: {e}")
        return []

def update_event_status(event_id, new_status):
    """Direct update for the is_active toggle."""
    try:
        supabase.table("events").update({"is_active": new_status}).eq("id", event_id).execute()
        return True
    except Exception as e:
        st.error(f"Status update error: {e}")
        return False

def create_event(date, sector_json, title_json, desc_json, active=True):
    """Creates an event. Maps the 'active' argument to the 'is_active' column."""
    supabase.table("events").insert({
        "date": str(date),
        "sector": sector_json,
        "title": title_json,
        "description": desc_json,
        "is_active": active  # <--- Changed column name
    }).execute()

def update_event(event_id, date, sector_json, title_json, desc_json):
    """Updates an existing event."""
    supabase.table("events").update({
        "date": str(date),
        "sector": sector_json,
        "title": title_json,
        "description": desc_json
    }).eq("id", event_id).execute()

# --- EXISTING FUNCTIONS (Unchanged logic) ---
def get_user_votes(user_id):
    try:
        response = supabase.table("votes").select("event_id, choice").eq("user_id", user_id).execute()
        return response.data
    except Exception:
        return []

def vote_for_event(user_id, event_id, choice):
    supabase.table("votes").insert({
        "user_id": user_id,
        "event_id": event_id,
        "choice": choice
    }).execute()

def get_event_stats(event_id):
    try:
        response = supabase.table("event_results").select("*").eq("event_id", event_id).execute()
        return response.data
    except Exception:
        return []

def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"success": True, "user": response.user, "session": response.session}
    except Exception as e:
        return {"success": False, "message": str(e)}

def register_user(email, password):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user:
            return {"success": True, "user": response.user, "session": response.session}
        return {"success": False, "message": "Registration failed."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def reset_password(email):
    try:
        supabase.auth.reset_password_for_email(email)
        return True
    except Exception as e:
        print(f"Reset error: {e}")
        return False