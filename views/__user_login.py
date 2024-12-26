import streamlit as st
import control.db_connection as dbc
import time
from datetime import datetime, timezone
from supabase import AuthApiError
from streamlit_extras.stylable_container import stylable_container


conn = None
if "__conn" not in st.session_state:
    conn = dbc.init_connection()
    st.session_state['__conn'] = conn
else:
    conn = st.session_state['__conn']

# if "ts_start" not in st.session_state.keys():
#     st.session_state["ts_start"] = str(datetime.now(tz=timezone.utc))

curr_user = conn.auth.get_session()
if curr_user:
    st.write(f"## Bem vindo(a), :blue[{curr_user.user.user_metadata["first_name"]}]!")
    with st.container(border=True):
        st.markdown("#### Prossiga para a próxima página ->")

    #### Navigation buttons ###
    with st.container():
        _, _, nav_next_logged = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
        with nav_next_logged:
            st.page_link("views/dash.py", label="Avançar 	:arrow_right:",)

else:
    #######
    st.markdown("##	:bust_in_silhouette: :blue[Login de Usuário]")

    with st.container(border=True):
        # col_login, col_btn = st.columns(spec=[0.9, 0.1]) 
        # with col_login:
        email_user = st.text_input("Email", placeholder="Insira seu email cadastrado", key="_email", )
        pwd_user = st.text_input("Senha",type='password', key="_pwd")
        creds = dict(email=email_user, password=pwd_user)
        btn_login = st.button("Entrar")

        #saving the user data into the session state
        if btn_login:
            try:
                response = conn.auth.sign_in_with_password(credentials=creds)
                # response
                # user_data = conn.auth.get_user.user_metadata
                time.sleep(1)
                # st.session_state['__conn'] = conn
                # st.write(response.user)
                st.success(f"## Bem-vindo(a), :blue[{conn.auth.get_user().user.user_metadata["first_name"]}]!")
                
                #### Navigation buttons ###
                with st.container():
                    _, _, nav_next = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
                    with nav_next:
                        st.page_link("views/dash.py", label="Avançar 	:arrow_right:",)
                
            except AuthApiError as auth_error:
                st.error("Erro ao tentar fazer login. Por favor, tente novamente.")
                auth_error   