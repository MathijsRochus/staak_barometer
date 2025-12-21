import streamlit as st
from supabase import create_client, Client

# Singleton pattern: maar 1 connectie
def init_supabase() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_supabase()