import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def render_header():
    """
    Toont het logo linksboven en zorgt voor witruimte.
    """
    logo_file = "src/assets/logo.png"
    logo_base64 = get_base64_of_bin_file(logo_file)

    if logo_base64:
        # CSS TRUCJE:
        # 1. .logo-container: Plakt het plaatje vast linksboven.
        # 2. .block-container: Geeft de hele app extra witruimte bovenaan (padding-top)
        #    zodat de titel niet achter het logo verdwijnt op mobiel.
        st.markdown(
            f"""
            <style>
                .logo-container {{
                    position: fixed;
                    top: 1rem;
                    left: 1rem;
                    z-index: 99999;
                    width: 60px; /* Pas grootte aan naar wens */
                }}
                /* Dit zorgt dat de tekst niet onder het logo verdwijnt */
                .block-container {{
                    padding-top: 5rem !important; 
                }}
                /* Verberg standaard header elementen indien nodig */
                header[data-testid="stHeader"] {{
                    background-color: transparent;
                }}
            </style>
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" style="width: 100%;">
            </div>
            """,
            unsafe_allow_html=True
        )