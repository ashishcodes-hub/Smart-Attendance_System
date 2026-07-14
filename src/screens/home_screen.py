import streamlit as st

from src.ui.base_layout import style_base_layout, style_background_home
from src.components.header import header_home


def home_screen():
    style_background_home()
    style_base_layout() 
    header_home()
    col1, col2 = st.columns(2)
    with col1:
        st.header("I ' m Student")
        if st.button("Student Portal", type='primary', icon=':material/arrow_outward:', icon_position='right'):
           st.session_state['login_type'] = 'student'
           st.rerun()
    with col2: 
        st.header("I ' m Teacher") 
        if st.button("Teacher Portal",type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    