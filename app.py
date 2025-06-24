# import streamlit as st
# import pandas as pd
# import time 
# from datetime import datetime

# ts=time.time()
# date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
# timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")

# from streamlit_autorefresh import st_autorefresh

# count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# if count == 0:
#     st.write("Count is zero")
# elif count % 3 == 0 and count % 5 == 0:
#     st.write("FizzBuzz")
# elif count % 3 == 0:
#     st.write("Fizz")
# elif count % 5 == 0:
#     st.write("Buzz")
# else:
#     st.write(f"Count: {count}")


# df=pd.read_csv("Attendance/Attendance_" + date + ".csv")

# st.dataframe(df.style.highlight_max(axis=0))

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# from datetime import datetime

# # Title & header
# st.set_page_config(page_title="Attendance Logs", layout="wide")
# st.title("📋 Attendance Logs")

# # Load today's log file
# date_today = datetime.today().strftime('%d-%m-%Y')
# csv_path = f"Attendance/Attendance_{date_today}.csv"

# # Check file exists
# if os.path.exists(csv_path):
#     df = pd.read_csv(csv_path)
# else:
#     st.warning("No attendance data found for today!")
#     st.stop()

# # Filters
# col1, col2, col3 = st.columns([3, 2, 2])

# with col1:
#     name_filter = st.text_input("🔍 Search by name")

# with col2:
#     date_filter = st.date_input("📅 Filter by date", datetime.today())
#     date_str = date_filter.strftime('%d-%m-%Y')

# with col3:
#     st.write("")
#     if st.button("🔄 Filter"):
#         file = f"Attendance/Attendance_{date_str}.csv"
#         if os.path.exists(file):
#             df = pd.read_csv(file)
#         else:
#             st.warning("No data for selected date.")
#             st.stop()

# # Filter by name
# if name_filter:
#     df = df[df["NAME"].str.contains(name_filter, case=False)]

# # Show table
# st.dataframe(df, use_container_width=True)

# # Download button
# csv = df.to_csv(index=False).encode('utf-8')
# st.download_button("⬇️ Download CSV", data=csv, file_name="attendance_filtered.csv", mime='text/csv')

# # Bar chart
# if not df.empty:
#     st.subheader("📊 Attendance Count by User")
#     counts = df["NAME"].value_counts().reset_index()
#     counts.columns = ["Name", "Attendance Count"]

#     fig = px.bar(counts, x="Name", y="Attendance Count", color="Name", text="Attendance Count",
#                  labels={"Name": "User", "Attendance Count": "Count"},
#                  template="plotly_white", width=800, height=400)
#     st.plotly_chart(fig, use_container_width=True)

# # Optional logout placeholder
# st.markdown("<hr>", unsafe_allow_html=True)
# st.button("🚪 Logout")

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
from datetime import datetime

# Page config
st.set_page_config(page_title="Smart Attendance System", layout="wide")

# Tabs
tab1, tab2, tab3 = st.tabs(["📸 Take Attendance", "🖼️ Add New Image", "📊 Logs"])

# -----------------------------------------------
# TAB 1 - Take Attendance
# -----------------------------------------------
with tab1:
    st.header("📸 Face Recognition - Take Attendance")
    st.write("Click below to launch the face recognition and mark attendance.")
    
    if st.button("✅ Start Attendance"):
        with st.spinner("Launching attendance system..."):
            subprocess.run(["python", "test.py"])
        st.success("✔️ Attendance process completed.")

# -----------------------------------------------
# TAB 2 - Add New Image (Face Registration)
# -----------------------------------------------
with tab2:
    st.header("🖼️ Register New User")

    st.markdown("---")
    st.subheader("🧑‍💼 Face Registration")

    reg_name = st.text_input("Enter your name to register face")

    if st.button("📷 Register Face"):
        if reg_name.strip():
            st.success(f"Launching webcam to register: {reg_name}")
            subprocess.run(["python", "add_faces.py", reg_name])
        else:
            st.warning("⚠️ Please enter a name before registering.")

# -----------------------------------------------
# TAB 3 - Attendance Logs
# -----------------------------------------------
with tab3:
    st.header("📊 Attendance Logs Viewer")

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

    # Show table
    st.dataframe(df, use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name="attendance_filtered.csv", mime='text/csv')

    # Bar chart
    if not df.empty:
        st.subheader("📈 Attendance Count by User")
        counts = df["NAME"].value_counts().reset_index()
        counts.columns = ["Name", "Attendance Count"]
        fig = px.bar(counts, x="Name", y="Attendance Count", color="Name", text="Attendance Count",
                     labels={"Name": "User", "Attendance Count": "Count"},
                     template="plotly_white", width=800, height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data to display.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("🚪 Logout")
