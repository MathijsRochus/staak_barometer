import streamlit as st
from src.backend.client import supabase

def get_all_events():
    """Fetches ALL events, both past and future, ordered by date."""
    try:
        # We select * to ensure we get everything. 
        # The filtering happens in the frontend (home.py) or via specific queries if needed later.
        response = supabase.table("events").select("*").order("date", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Supabase Error: {e}") 
        return []

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

def create_event(date, sector, title_json, desc_json):
    supabase.table("events").insert({
        "date": str(date),
        "sector": sector,
        "title": title_json,
        "description": desc_json
    }).execute()

# Auth functions (kept as provided previously)
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
        return {"success": False, "message": "Registratie niet gelukt."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def reset_password(email):
    try:
        supabase.auth.reset_password_for_email(email)
        return True
    except Exception as e:
        print(f"Reset error: {e}")
        return False