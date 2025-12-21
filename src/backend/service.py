import streamlit as st
from src.backend.client import supabase

def get_live_events():
    try:
        response = supabase.table("events").select("*").order("date", desc=True).execute()
        return response.data
    except Exception as e:
        # Tijdlijke DEBUG regel: toon de error in de app
        st.error(f"Supabase Error: {e}") 
        return []

def get_user_votes(user_id):
    try:
        response = supabase.table("votes").select("event_id, choice").eq("user_id", user_id).execute()
        return response.data
    except Exception:
        return []

def vote_for_event(user_id, event_id, choice):
    # Gooit een error als het mislukt, die vangen we in de View op
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

# Nieuwe functie voor admin later
def create_event(date, sector, title_json, desc_json):
    supabase.table("events").insert({
        "date": str(date),
        "sector": sector,
        "title": title_json,
        "description": desc_json
    }).execute()


    # ... (Bestaande imports zoals supabase)


def login_user(email, password):
    """Probeert alleen in te loggen."""
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "success": True,
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

def register_user(email, password):
    """Probeert alleen te registreren."""
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        # Check of auto-confirm aan of uit staat bij Supabase
        if response.user:
            return {
                "success": True, 
                "user": response.user, 
                "session": response.session # Kan None zijn als confirm email AAN staat
            }
        return {"success": False, "message": "Registratie niet gelukt."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def reset_password(email):
    """Stuurt een password reset mail."""
    try:
        # Dit stuurt een mailtje via Supabase
        supabase.auth.reset_password_for_email(email)
        return True
    except Exception as e:
        print(f"Reset error: {e}")
        return False
    """
    Probeert in te loggen. Als dat faalt, probeert hij te registreren.
    Geeft een dictionary terug met status info.
    """
    # 1. Probeer Login
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "success": True,
            "user": response.user,
            "session": response.session,
            "message": "Login successful"
        }
    except Exception as login_error:
        # 2. Login mislukt? Probeer Registratie (Auto-signup)
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            
            # Check of we direct een sessie hebben (Auto-confirm staat UIT in Supabase)
            if response.user and response.session:
                return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,
                    "is_new_user": True,
                    "message": "Registration successful"
                }
            elif response.user and not response.session:
                return {
                    "success": False,
                    "message": "Registratie gelukt! Check uw email om te bevestigen."
                }
            else:
                return {
                    "success": False,
                    "message": "Registratie mislukt."
                }
        except Exception as reg_error:
            # Zowel login als registratie mislukt
            return {
                "success": False,
                "message": f"Fout: {reg_error}"
            }