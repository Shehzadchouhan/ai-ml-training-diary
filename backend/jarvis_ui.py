import streamlit as st
import subprocess
import os

# here is run commond:-
# streamlit run jarvis_ui.py
# ----------------------------------

st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---- HEADER ----
st.markdown("""
    <div style="text-align:center; padding:10px;">
        <h2>🤖 Jarvis - Voice AI Assistant</h2>
    </div>
""", unsafe_allow_html=True)

# ---- GIF (50% WIDTH + CENTER) ----
col = st.columns([1,2,1])[1]   # center column
with col:
    st.image("gui4.gif", width=300)   # adjust width as needed


# ---- BUTTONS SECTION (CENTERED) ----
cols = st.columns([1,1,1,1,1])  # five equal columns
with cols[1]:  # middle column
    if st.button("▶ Start Jarvis"):
        st.info("Jarvis is starting... Please wait.")
        try:
            subprocess.Popen(
                ["python", "C:\\Jarvis_last\\backend\\agent.py", "console"],
                shell=True
            )
            st.success("✅ Jarvis started successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

with cols[3]:  # next to middle
    if st.button("⏹ Stop Jarvis"):
        st.warning("🛑 Stopping Jarvis...")
        try:
            os.system("taskkill /f /im python.exe")
            st.success("✅ Jarvis stopped successfully!")
        except Exception as e:
            st.error(f"Error stopping Jarvis: {e}")

# ---- FOOTER ----
st.markdown("""
    <div style="text-align:center; margin-top:40px; opacity:0.7;">
      contact with Mohd Shehzad
        <br>
        <a href="https://www.linkedin.com/in/shehzad23">LinkedIN</a> &nbsp; | &nbsp;
        <a href="https://github.com/ShehzadChouhan">Github Source</a>
    </div>
""", unsafe_allow_html=True)

