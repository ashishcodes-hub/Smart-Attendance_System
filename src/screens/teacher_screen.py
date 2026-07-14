
import streamlit as st
from src.ui.base_layout import style_background_dashbord, style_base_layout
from src.components.header import header_dashbord
from src.database.db import check_teacher_exists, create_teacher,teacher_login, get_teacher_subject,get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photo_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
from datetime import datetime
import pandas as pd
import numpy as np
from src.components.dialog_attnedance_results import attendance_result_dialog




def teacher_screen():
    style_base_layout()
    style_background_dashbord()
    if "teacher_data" in st.session_state:
        teacher_dashbord()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()


def teacher_dashbord():
    teacher_data = st.session_state.teacher_data
    c1,c2=st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashbord()
    with c2:
         st.header(f"""Welcome, {teacher_data['name']}""")
         if st.button("Logout", key='backhomebtn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()    
    
    st.space()
    st.space()
    st.space()


    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
        st.rerun()
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subject' else "tertiary"
        if st.button('Manage Subjects',type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance_records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subject":
        teacher_tab_manage_subject()
    
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('AI  Attendance')
    st.space()
    st.space()
    st.space()

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning('You have not Created any subject yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} -  {s['subject_code']}" : s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1])


    with col1:
        # selected_subject_lable = st.selectbox('Select Subject', options=list(subject_options.keys()))
     st.markdown(
        "<p style='color:black; font-weight:600; '>Select Subject</p>",
        unsafe_allow_html=True
    )

    selected_subject_lable = st.selectbox(
        label="Select Subject",
        options=list(subject_options.keys()),
        label_visibility="collapsed"
    )





    selected_subject_id = subject_options[selected_subject_lable]
    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photo_dialog(selected_subject_id)

    

    st.divider()


   
    if st.session_state.attendance_images:
        st.header("Added Photos")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption= f'Photo {idx+1}')

        st.divider()

    c1, c2,  = st.columns(2)
    has_photos = bool(st.session_state.attendance_images)

    with c1:
        if st.button('Clear all Photos', width='stretch', type='tertiary', icon=':material/delete:', disabled= not has_photos):
            st.session_state.attendance_images = []
            st.rerun()
    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            pass
            with st.spinner('Deep Scanning Classroom Photos....'):
                all_detected_ids = {}
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected,_,_= predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")
                
                enrolled_res = supabase.table('subject_students').select("*, students(* )").eq('subject_id', selected_subject_id).execute()
                enrolled_student = enrolled_res.data
                if not enrolled_student:
                    st.warning('No student enrolled in this course')
                else:
                    
                    results , attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    for node in enrolled_student:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) >0
                        results.append({
                            "Name" : student['name'],
                            "ID" : student['student_id'],
                            "Source" : ".".join(sources) if is_present else "-",
                            "Status" : "✅ Present" if is_present else "❌ Absent"
                        
                        })
                        attendance_to_log.append({
                            'student_id' : student['student_id'],
                            'subject_id' : selected_subject_id,
                            'timestamp' : current_timestamp,
                            'is_present' : bool(is_present)
                        })
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)


    

def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subject ', width='stretch')
    
    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)
    
    # List all subject 
    subject = get_teacher_subject(teacher_id)
    if subject:
        for sub in subject: 
            stats = [
                ("👥", "Students", sub['total_students']),
                ("⏰", "Classes", sub['total_classes']),
            ]
        def share_btn():
            if st.button(f"Share Code :{sub['name']}", key= f"share_{sub['subject_code']}", icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()
        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats = stats,
            footer_callback = share_btn
        )

    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE")               

def teacher_tab_attendance_records():
    st.header('Attendance Records')
    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)
    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time" : datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M%p") if  ts else "N'A",
            "Subject" : r['subjects']['name'],
            "Subject Code" : r['subjects']['subject_code'],
            "is_present" : bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)


    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_count = ('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats']  = (
        "✅"+summary['Present_Count'].astype(str) +' Student'
    )

    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    st.dataframe(display_df, width='stretch', hide_index=True)
                  



def login_teacher(username, password):
     if not username or not password:
         return False
     teacher = teacher_login(username, password)
     if teacher:
         st.session_state.user_role = 'teacher'
         st.session_state.teacher_data = teacher
         st.session_state.is_logged_in = True
         return True
     return False

def teacher_screen_login():
    c1,c2=st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashbord()
    with c2:
         if st.button("Go Back to Home", key='backhomebtn'):
            st.session_state['login_type'] = None
            st.rerun()    

    st.header("Login Using Password", text_alignment='center')

    teacher_username =st.text_input("Enter Username : ", placeholder="Enter Username :")
    teacher_password = st.text_input("Enter Password : ", type='password', placeholder='Enter Password :')

    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button('Login', icon=':material/passkey:', width='stretch'):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="👋")
    
    with btn2:
       if st.button('Register', icon=':material/passkey:', width='stretch', type='primary'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False ,"Fill All Details"
    if check_teacher_exists(teacher_username):
        return False, "Username already exist"
    if teacher_pass != teacher_pass_confirm:
        return False ,"Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected error!"
    


def teacher_screen_register():

    c1,c2=st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashbord()
    with c2:
        if st.button("Go Back to Home", key='backhomebtn'):
            st.session_state['login_type'] = None
            st.rerun()
              

    st.header("Register Your Teacher Profile")


    teacher_username =st.text_input("Enter Username : ", placeholder="Enter Username :")
    teacher_name =st.text_input("Enter Name : ", placeholder="Enter Nmae :")

    teacher_password = st.text_input("Enter Password : ", type='password', placeholder='Enter Password :')
    teacher_password_confirm = st.text_input("Confirm Password : ", type='password', placeholder='Confirm Password :')

   
    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
       if st.button('Login Insted', icon=':material/passkey:', width='stretch'):
           st.session_state.teacher_login_type = 'login'
           st.rerun()

    with btnc2:
       if st.button('Register Now', icon=':material/passkey:', width='stretch', type='primary'):
            success, message = register_teacher(teacher_username, teacher_name,teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
         

