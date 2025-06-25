# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import subprocess
# from datetime import datetime

# # Page config
# st.set_page_config(page_title="Smart Attendance System", layout="wide")

# # Tabs
# tab1, tab2, tab3 = st.tabs(["📸 Take Attendance", "🖼️ Add New Image", "📊 Logs"])

# # -----------------------------------------------
# # TAB 1 - Take Attendance
# # -----------------------------------------------
# with tab1:
#     st.header("📸 Face Recognition - Take Attendance")
#     st.write("Click below to launch the face recognition and mark attendance.")
    
#     if st.button("✅ Start Attendance"):
#         with st.spinner("Launching attendance system..."):
#             subprocess.run(["python", "test.py"])
#         st.success("✔️ Attendance process completed.")

# # -----------------------------------------------
# # TAB 2 - Add New Image (Face Registration)
# # -----------------------------------------------
# with tab2:
#     st.header("🖼️ Register New User")

#     st.markdown("---")
#     st.subheader("🧑‍💼 Face Registration")

#     reg_name = st.text_input("Enter your name to register face")

#     if st.button("📷 Register Face"):
#         if reg_name.strip():
#             st.success(f"Launching webcam to register: {reg_name}")
#             subprocess.run(["python", "add_faces.py", reg_name])
#         else:
#             st.warning("⚠️ Please enter a name before registering.")

# # -----------------------------------------------
# # TAB 3 - Attendance Logs
# # -----------------------------------------------
# with tab3:
#     st.header("📊 Attendance Logs Viewer")

#     # Load today's file
#     date_today = datetime.today().strftime('%d-%m-%Y')
#     csv_path = f"Attendance/Attendance_{date_today}.csv"

#     # Filters
#     col1, col2, col3 = st.columns([3, 2, 2])
#     with col1:
#         name_filter = st.text_input("🔍 Search by name")

#     with col2:
#         date_filter = st.date_input("📅 Filter by date", datetime.today())
#         date_str = date_filter.strftime('%d-%m-%Y')

#     with col3:
#         st.write("")
#         if st.button("🔄 Filter"):
#             file = f"Attendance/Attendance_{date_str}.csv"
#             if os.path.exists(file):
#                 csv_path = file
#             else:
#                 st.warning("⚠️ No data for selected date.")
#                 st.stop()

#     # Load filtered CSV
#     if os.path.exists(csv_path):
#         df = pd.read_csv(csv_path)
#     else:
#         st.warning("⚠️ No attendance data found!")
#         st.stop()

#     # Name filtering
#     if name_filter:
#         df = df[df["NAME"].str.contains(name_filter, case=False)]

#     # Show table
#     st.dataframe(df, use_container_width=True)

#     # Download button
#     csv = df.to_csv(index=False).encode('utf-8')
#     st.download_button("⬇️ Download CSV", data=csv, file_name="attendance_filtered.csv", mime='text/csv')

#     # Bar chart
#     if not df.empty:
#         st.subheader("📈 Attendance Count by User")
#         counts = df["NAME"].value_counts().reset_index()
#         counts.columns = ["Name", "Attendance Count"]
#         fig = px.bar(counts, x="Name", y="Attendance Count", color="Name", text="Attendance Count",
#                      labels={"Name": "User", "Attendance Count": "Count"},
#                      template="plotly_white", width=800, height=400)
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No data to display.")

#     st.markdown("<hr>", unsafe_allow_html=True)
#     st.button("🚪 Logout")
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
from datetime import datetime


st.set_page_config(
    page_title="Smart Attendance System",
    layout="wide",
    page_icon="👥",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 20px;
            border-radius: 8px 8px 0 0;
            background-color: #f0f2f6;
            transition: all 0.2s;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4a8cff;
            color: white;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 8px 16px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stDataFrame {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stAlert {
            border-radius: 8px;
        }
        .css-1cpxqw2 {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div style="text-align:center; margin-bottom:30px;">
        <h1 style="color:#4a8cff;">👥 Smart Attendance System</h1>
        <p style="color:#666; font-size:16px;">Automated face recognition for attendance tracking</p>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["📸 Take Attendance", "🖼️ Register New User", "📊 Attendance Logs"])

#TAB2
with tab1:
    st.header("Take Attendance")
    st.markdown("""
    <div style="background:#f8f9fa; padding:20px; border-radius:10px; margin-bottom:20px;">
        <h3 style="color:#4a8cff;">Instructions</h3>
        <p style="color:black;">Click the button below to launch the face recognition system and mark attendance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("✅ Start Attendance", key="start_attendance", 
                    help="Click to begin face recognition process"):
            with st.spinner("🔍 Launching attendance system. Please wait..."):
                subprocess.run(["python", "test.py"])
            st.success("✔️ Attendance process completed successfully!")
            st.balloons()

#TAB2
with tab2:
    st.header("Register New User")
    
    with st.expander("ℹ️ Registration Instructions", expanded=True):
        st.markdown("""
        1. Enter the user's full name in the text field below
        2. Click the 'Register Face' button
        3. The system will launch your webcam to capture facial data
        """)
    
    with st.container():
        st.subheader("User Information")
        reg_name = st.text_input("Full Name", 
                                placeholder="Enter the name to register",
                                key="reg_name_input")
        
        if st.button("📷 Register Face", 
                    key="register_face",
                    disabled=not reg_name.strip(),
                    help="Enter a name above to enable this button"):
            if reg_name.strip():
                with st.spinner(f"📸 Launching webcam to register: {reg_name}..."):
                    subprocess.run(["python", "add_faces.py", reg_name])
                st.success(f"✅ Successfully registered {reg_name}!")
            else:
                st.warning("⚠️ Please enter a valid name before registering.")

# -----------------------------------------------
# TAB 3 - Attendance Logs
# -----------------------------------------------
# -----------------------------------------------
# TAB 3 - Attendance Logs
# -----------------------------------------------
# -----------------------------------------------
# TAB 3 - Attendance Logs
# -----------------------------------------------
with tab3:
    st.header("📊 Attendance Logs Viewer")

    # Custom CSS for dark table
    st.markdown("""
    <style>
        .stDataFrame div[data-testid="stDataFrameContainer"] {
            background-color: black !important;
            color: white !important;
        }
        .stDataFrame table {
            color: white !important;
        }
        .stDataFrame thead tr th {
            background-color: #333 !important;
            color: white !important;
        }
        .stDataFrame tbody tr td {
            background-color: #222 !important;
            color: white !important;
        }
        .stDataFrame tbody tr:nth-child(even) td {
            background-color: #1a1a1a !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load today's file
    date_today = datetime.today().strftime('%d-%m-%Y')
    csv_path = f"Attendance/Attendance_{date_today}.csv"

    # Filters
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        name_filter = st.text_input("🔍 Search by name")

    with col2:
        date_filter = st.date_input("📅 Filter by date", datetime.today())
        date_str = date_filter.strftime('%d-%m-%Y')

    with col3:
        st.write("")
        if st.button("🔄 Filter"):
            file = f"Attendance/Attendance_{date_str}.csv"
            if os.path.exists(file):
                csv_path = file
            else:
                st.warning("⚠️ No data for selected date.")
                st.stop()

    # Load filtered CSV
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        st.warning("⚠️ No attendance data found!")
        st.stop()

    # Name filtering
    if name_filter:
        df = df[df["NAME"].str.contains(name_filter, case=False)]

    # Show table with dark theme
    st.dataframe(df.style.set_properties(**{
        'background-color': '#000000',
        'color': 'white',
        'border-color': '#444'
    }), use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name="attendance_filtered.csv", mime='text/csv')

    # Visualization Section
    if not df.empty:
        # Create tabs for different chart types
        chart_tab1, chart_tab2 = st.tabs(["📊 Bar Chart", "📈 Line Chart"])
        
        with chart_tab1:
            st.subheader("Attendance Count by User")
            counts = df["NAME"].value_counts().reset_index()
            counts.columns = ["Name", "Attendance Count"]
            fig_bar = px.bar(counts, x="Name", y="Attendance Count", color="Name", 
                           text="Attendance Count",
                           labels={"Name": "User", "Attendance Count": "Count"},
                           template="plotly_white")
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with chart_tab2:
            st.subheader("Attendance Over Time")
            
            # Convert TIME column to datetime and extract hour
            try:
                df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
                df['Hour'] = df['TIME'].dt.hour
                
                # Create line chart
                fig_line = px.line(df.groupby('Hour').size().reset_index(name='Count'),
                                 x='Hour', y='Count',
                                 title='Attendance by Hour of Day',
                                 markers=True)
                fig_line.update_xaxes(title='Hour of Day', 
                                    tickvals=list(range(24)),
                                    range=[0, 23])
                fig_line.update_yaxes(title='Number of Attendances')
                st.plotly_chart(fig_line, use_container_width=True)
                
                # Additional time-based analysis
                df['Date'] = pd.to_datetime(df['TIME']).dt.date
                daily_counts = df.groupby('Date').size().reset_index(name='Count')
                fig_daily = px.line(daily_counts,
                                  x='Date', y='Count',
                                  title='Daily Attendance Trend',
                                  markers=True)
                st.plotly_chart(fig_daily, use_container_width=True)
                
            except Exception as e:
                st.warning(f"Could not create time-based charts: {str(e)}")
    else:
        st.info("No data to display.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("🚪 Logout")