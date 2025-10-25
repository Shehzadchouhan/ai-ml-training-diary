import streamlit as st
import subprocess
import os
import base64

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Jarvis AI Assistant", page_icon="🤖", layout="centered")

# -----------------------------
# Background GIF Setup
# -----------------------------
def add_bg_from_local(gif_file):
    with open(gif_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    background_code = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/gif;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stHeader"] {{background: rgba(0,0,0,0);}}
    [data-testid="stSidebar"] {{background: rgba(0,0,0,0.5);}}
    </style>
    """
    st.markdown(background_code, unsafe_allow_html=True)

# Call background function
add_bg_from_local("gui1.gif")

# -----------------------------
# Page Title
# -----------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:white;'>🧠 Jarvis AI Assistant</h1>
    <h4 style='text-align:center; color:#ddd;'>Voice-Activated Smart Assistant</h4>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Control Panel
# -----------------------------
st.markdown("<h3 style='color:#00BFFF;'>🎙️ Control Panel</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

if col1.button("▶️ Start Jarvis"):
    st.info("Jarvis is starting... Please wait.")
    try:
        subprocess.Popen(
            ["python", "C:\\Jarvis_last\\backend\\agent.py", "console"],
            shell=True
        )
        st.success("✅ Jarvis started successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

if col2.button("⏹ Stop Jarvis"):
    st.warning("🛑 Stopping Jarvis...")
    try:
        os.system("taskkill /f /im python.exe")
        st.success("✅ Jarvis stopped successfully!")
    except Exception as e:
        st.error(f"Error stopping Jarvis: {e}")

# -----------------------------
# Log Output Section
# -----------------------------
st.markdown("<h3 style='color:#00BFFF;'>💬 Jarvis Output</h3>", unsafe_allow_html=True)

log_file = "jarvis_logs.txt"

if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        logs = f.read()
    st.text_area("Console Output", logs, height=300)
else:
    st.info("No logs yet — start Jarvis to see live output.")

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:#bbb;'>
    Created by <b>Mohd. Shehzad</b> | Powered by <b>Streamlit</b>
    </p>
    """,
    unsafe_allow_html=True
)
