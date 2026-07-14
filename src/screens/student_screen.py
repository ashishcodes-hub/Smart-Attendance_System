
import streamlit as st
from src.ui.base_layout import style_background_dashbord, style_base_layout
from src.components.header import header_dashbord
from src.database.db import check_teacher_exists, create_student,teacher_login 
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings
from PIL import Image
import numpy as np
from src.database.db  import get_all_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashbord():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1,c2=st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashbord()
    with c2:
        #  st.subheader(f"""Welcome, {student_data['name']}""")
        st.markdown(
            f"""
            <h3 style="color:#3b3737;white-space: nowrap;overflow: hidden;">
                Welcome, {student_data['name']}
            </h3>
            """,
            unsafe_allow_html=True
        )
        if st.button("Logout", key='backhomebtn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun() 

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('You Enrolled Subject')
    
    with c2:
       if st.button('Enroll in subject', type='primary', width='stretch'):
           enroll_dialog()

    with st.spinner('Load your inrolled subject....'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        # sid = log['student_id']
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total" : 0, "attended" : 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] +=1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total":0, "attended":0})
        def unenrollbtn():
            if st.button("Unenroll from the coures", key=f"unenroll_{sid}", type='tertiary', width='stretch'):
                unenroll_student_to_subject(student_id, sid)



        with cols[i % 2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('🔢', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended'])
                ],


                footer_callback= unenrollbtn
            )
    

    st.divider()



def student_screen():
    style_base_layout()
    style_background_dashbord()
    if "student_data" in st.session_state:
        student_dashbord()
        return 
    c1,c2=st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashbord()
    with c2:
        if st.button("Go Back to Home", key='backhomebtn'):
            st.session_state['login_type'] = None
            st.rerun()    
    st.header("Login Using FaceID", text_alignment='center')
    show_registraction = False
    photo_source = st.camera_input("")
    if photo_source:
        img =  np.array(Image.open(photo_source))
        with st.spinner('AI is Scanning....'):
            detected, all_ids, num_faces= predict_attendance(img)
            if num_faces==0:
                st.warning('Face not Found!')
            elif num_faces>1:
                st.warning('Multipuls Faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_student = get_all_student()
                    student = next((s for s in all_student if s['student_id']==student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back! {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! you must be a new Student!')
                    show_registraction = True

    if show_registraction:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter Your Name : ", placeholder="Enter Name : ")
            if st.button('Create Account ', type='primary'):
                if new_name:
                    with st.spinner ('Creating Profile....'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_embedding = encodings[0].tolist()
                            response_data = create_student(new_name, face_embedding = face_embedding)
                        if response_data:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = response_data[0]
                            st.toast(f'Welcome Back! {new_name}')
                else:
                     st.error('Could not Capture your face')
            else:
                st.warning('Please enter name : ')

        