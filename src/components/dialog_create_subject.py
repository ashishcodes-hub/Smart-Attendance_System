import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teachers_id):
    st.write("Enter the Detail of new subject")
    sub_id = st.text_input("Enter Subject Code", placeholder="subject code")
    sub_name = st.text_input("Enter Subject Name", placeholder="subject name")
    sub_section = st.text_input("Enter Subject Section", placeholder="subject section")

    if st.button("Create Subject Now", type="primary", width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teachers_id)
                st.toast("Subject Succesfully Created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error :{str(e)}")
        else:
            st.warning("Please fill all details")
    