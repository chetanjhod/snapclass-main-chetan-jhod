import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects,get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelinens.face_pipeline import predict_attendance
import numpy as np
from datetime import datetime
from src.database.config import supabase
import pandas as pd
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
def teacher_screen():
    if "teacher_data" in st. session_state:
        teacher_dashboard()
        return

    style_background_dashboard()
    style_base_layout()

    if "teacher_page" not in st.session_state:
        st.session_state.teacher_page = "login"

    if st.session_state.teacher_page == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()



def teacher_dashboard():
    style_background_dashboard()
    style_base_layout()

    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2)

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""welcome, {teacher_data['name']}""")
        if st.button(
            "Logout",
            key="home_btn_register"
        ):
            st.session_state['is_loged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
    st.space()





    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take atandance'
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
      type1 = "primary" if st.session_state.current_teacher_tab == 'Take_attendance' else "tertiary"
      if st.button('Take Atandance',type=type1, width='stretch',icon=':material/ar_on_you:'):
          st.session_state.current_teacher_tab = 'Take_attendance'
          st.rerun()

    with tab2:
      type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
      if st.button('manage subjects',type=type2, width='stretch',icon=':material/book_ribbon:'):
          st.session_state.current_teacher_tab = 'manage_subjects'
          st.rerun()

    
    with tab3:
      type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
      if st.button('Attandance records',type=type3,width='stretch',icon=':material/assignment:'):
          st.session_state.current_teacher_tab = 'attendance_records'
          st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "Take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendance")


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []


    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('you havent creat any subject yet! plese create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}



    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
       selected_subject_label = st.selectbox(
        'Select Subject',
        options=list(subject_options.keys())
    )

    with col2:
       if st.button('Add Photos',type='primary',icon=':material/photo_prints:',width='stretch'):
        add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()
   
    if st.session_state.attendance_images:
       st.header('Added Photos')
       gallery_cols = st.columns(4)

       for idx, img in enumerate(st.session_state.attendance_images):
           with gallery_cols[idx % 4]:
              st.image(img, width='stretch', caption=f'Photo {idx+1}')

    c1, c2, c3 = st.columns(3)
    has_photos = bool(st.session_state.attendance_images)
    with c1:
        if st.button('Clear all photos',width='stretch',type='tertiary',icon=':material/delete:',disabled=not has_photos ):
           st.session_state.attendance_images = []
           st.rerun()

    
    with c2:
       if st.button(
        'Run Face Analysis',
        width='stretch',
        type='secondary',
        icon=':material/analytics:',
        disabled=not has_photos
    ):
        with st.spinner('Deep scanning classroom photos...'):
            all_detected_ids = {}

            for idx, img in enumerate(st.session_state.attendance_images):
                img_np = np.array(img.convert('RGB'))
                detected, _, _ = predict_attendance(img_np)

                if detected:
                    for sid in detected.keys():
                        student_id = int(sid)
                        all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

            enrolled_res = (
                supabase.table('subject_students')
                .select("*, student(*)")
                .eq('subject_id', selected_subject_id)
                .execute()
            )
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this course")

            else:
                results = []
                attendance_to_log = []

                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                for node in enrolled_students:
                    student = node["student"]
                    sources = all_detected_ids.get(int(student["student_id"]), [])
                    is_present = len(sources) > 0

                    results.append({
                        "Name": student["name"],
                        "ID": student["student_id"],
                        "Source": ", ".join(sources) if is_present else "--",
                        "Status": "✅ Present" if is_present else "❌ Absent"
                    })

                    attendance_to_log.append({
                        "student_id": student["student_id"],
                        "subject_id": selected_subject_id,
                        "timestamp": current_timestamp,
                        "is_present": is_present
                    })

            st.session_state.face_attendance_results = (pd.DataFrame(results),attendance_to_log)
            st.rerun()
    if  st.session_state.get("face_attendance_results") is not None:
        st.divider()
        df_results, logs = st.session_state.face_attendance_results
        attendance_result_dialog(df_results, logs)

    with c3:
        if st.button(
               'Use Voice Attendance',
                type='primary',
                width='stretch',
                icon=':material/mic:'
                 ):
            voice_attendance_dialog(selected_subject_id)
    
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns(2)

    with col1:
        st.header("Manage Subjects", width="stretch")

    with col2:
        if st.button("Create New Subject", width="stretch"):
          create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "students", sub["total_students"]),
                ("🕰️", "classes", sub["total_classes"]),
            ]
            
        def share_btn():
            st.markdown ("<br>",unsafe_allow_html=True)
            if st.button(f"Share Code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
             share_subject_dialog(sub['name'],sub['subject_code'])
            st.space()


        subject_card(
           name=sub['name'],
           code=sub['subject_code'],
           section=sub['section'],
           stats=stats,
           footer_callback=share_btn
        )
    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE")    


def teacher_tab_attendance_records():
    st.header("Atandance record")

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
           "ts_group": ts.split("T")[0] if ts else None,
           "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
           "Subject": r['subjects']['name'],
           "Subject Code": r['subjects']['subject_code'],
           "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)


    summary = (
    df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
      .agg(
          Present_Count=('is_present', 'sum'),
          Total_Count=('is_present', 'count')
      )
      .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + " Students"
    )
    display_df = (
                   summary.sort_values(by='ts_group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                   )

    st.table(display_df)
    
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

    c1, c2 = st.columns(2)

    with c1:
    
        header_dashboard()

    with c2:
        if st.button(
            "⬅ Go back to Home",
            key="home_btn_login"
        ):
            st.session_state['login_type'] = None
            st.rerun()
    st.header("Login Using Password")
    st.space()

    teacher_username=st.text_input(
        "ENTER USERNAME",
        placeholder="johny"
    )
    teacher_pass=st.text_input(
        "ENTER PASSWORD",
        type="password",
        placeholder="Enter password"
    )

    st.divider()
    btn1, btn2 = st.columns(2)

    with btn1:
      if  st.button(
            "Login",
            icon="🔐",
            use_container_width=True
        ):
        teacher = teacher_login(teacher_username,teacher_pass)
        if teacher:
            st.session_state.teacher_data = teacher
            st.toast("welcome back👋")
            st.rerun()
        else:
            st.error("invalid username and password")

    with btn2:
        if st.button(
            "Register Instead",
            type="primary",
            icon="📝",
            use_container_width=True
        ):
            st.session_state.teacher_page = "register"
            st.rerun()

    footer_dashboard()

def register_teacher (teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False, "all fileds are requird!"
    if check_teacher_exists(teacher_username):
         return False, "username alrady taken"
    if teacher_pass != teacher_pass_confirm:
        return False ,"password doesn't match"
    
    try:
        create_teacher (teacher_username, teacher_pass, teacher_name)
        return True, "sucessfully created! login now"
    except Exception as e:
        return False, "unexpected Error!"

            
def teacher_screen_register():

    c1, c2 = st.columns(2)

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "⬅ Go back to Home",
            key="home_btn_register"
        ):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Ragister your teacher screen")
    st.space
    st.space

    teacher_username =st.text_input(
        "ENTER USERNAME",
        placeholder="johnydubay"
    )

    teacher_name = st.text_input(
        "ENTER NAME",
        placeholder="johny dubay"
    )

    teacher_pass = st.text_input(
        "CREATE PASSWORD",
        type="password",
        placeholder="Create password"
    )
    teacher_pass_confirm = st.text_input(
        "CONFORM YOUR PASSWORD",
        type="password",
        placeholder="Enter password"
    )
    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button(
            "Register",
            type="primary",
            icon="📝",
            use_container_width=True
            ):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_page = "login"
                st.rerun()
            else:
                st.error(message)
    with btn2:
        if st.button(
            "Back to Login",
            use_container_width=True
        ):
            st.session_state.teacher_page = "login"
            st.rerun()
