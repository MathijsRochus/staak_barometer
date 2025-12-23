import streamlit as st
from src.utils.text import get_text
from src.backend.service import login_user, register_user, reset_password

def render_login():
    # --- LOGO & TITEL SECTIE ---
    
    # AANGEPAST: We gebruiken [2, 1, 2] verhouding. 
    # Dit maakt de middelste kolom smaller (20% van totaal) en precies in het midden.
    c1, c2, c3 = st.columns([2, 1, 2]) 
    
    with c2:
        # Probeer het logo te tonen. 
        # Zorg dat src/assets/logo.png bestaat, anders vangt 'try' dit op.
        try:
            # AANGEPAST: We gebruiken width='stretch' in plaats van fixed width.
            # Omdat de kolom nu smal en gecentreerd is, staat het logo nu ook in het midden.
            st.image("src/assets/logo.png", width=150)
        except Exception:
            # Fallback als het plaatje ontbreekt (bv. tijdens development)
            st.markdown("<h1 style='text-align: center;'>📊</h1>", unsafe_allow_html=True)
        
    # De titel eronder (zonder de 📊 emoji, want we hebben nu een logo)
    title_clean = get_text('title').replace('📊 ', '')
    st.markdown(f"<h1 style='text-align: center;'>{title_clean}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- FORMULIER SECTIE ---
    # We gebruiken weer kolommen om het formulier niet te breed te maken op desktop
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(get_text("welcome_msg"))
        
        # Tabs voor Login vs Registratie
        tab1, tab2 = st.tabs([get_text("tab_login"), get_text("tab_register")])
        
        # --- TAB 1: INLOGGEN ---
        with tab1:
            with st.form("login_form"):
                email_l = st.text_input("Email", key="login_email")
                pass_l = st.text_input("Password", type="password", key="login_pass")
                submitted_l = st.form_submit_button(get_text("btn_login"), width='stretch')
                
                if submitted_l:
                    if email_l and pass_l:
                        result = login_user(email_l, pass_l)
                        if result["success"]:
                            # Sessie opslaan in state
                            st.session_state.session = result["session"]
                            st.session_state.user = result["user"]
                            st.session_state.page = 'home'
                            st.rerun()
                        else:
                            st.error(get_text("err_login_failed"))
                    else:
                        st.warning(get_text("login_warning"))
            
            # Wachtwoord Reset Sectie (buiten de form, in een expander)
            st.write("") # Klein beetje witruimte
            with st.expander(get_text("lnk_forgot_pwd")):
                reset_email = st.text_input("Email voor reset", key="reset_email")
                if st.button(get_text("btn_reset")):
                    if reset_email:
                        reset_password(reset_email)
                        st.success(get_text("msg_reset_sent"))
                    else:
                        st.warning("Vul een emailadres in.")

        # --- TAB 2: REGISTREREN ---
        with tab2:
            with st.form("register_form"):
                email_r = st.text_input("Email", key="reg_email")
                pass_r1 = st.text_input("Password", type="password", key="reg_p1")
                # Het tweede wachtwoord veld ter bevestiging
                pass_r2 = st.text_input(get_text("lbl_password_confirm"), type="password", key="reg_p2")
                
                submitted_r = st.form_submit_button(get_text("btn_register"), width='stretch')
                
                if submitted_r:
                    # 1. Check of velden gevuld zijn
                    if not email_r or not pass_r1:
                        st.warning(get_text("login_warning"))
                    # 2. Check of wachtwoorden matchen
                    elif pass_r1 != pass_r2:
                        st.error(get_text("msg_pwd_mismatch"))
                    # 3. Probeer te registreren via backend
                    else:
                        result = register_user(email_r, pass_r1)
                        if result["success"]:
                            # Als auto-confirm aan staat (of sessie direct terugkomt)
                            if result.get("session"):
                                st.session_state.session = result["session"]
                                st.session_state.user = result["user"]
                                st.session_state.page = 'home'
                                st.success("Account aangemaakt! U wordt ingelogd.")
                                st.rerun()
                            else:
                                st.success("Account aangemaakt! Controleer uw email om te bevestigen.")
                        else:
                            st.error(result["message"])