import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/tickets"
LOGS_URL = "http://127.0.0.1:8000/logs"

st.set_page_config(page_title="Smart-Support Orchestrator", page_icon="🎫", layout="wide")
st.title("🎫 Smart-Support Ticket Routing Engine")

# --- UI Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚨 Flash-Flood Simulator")
    if st.button("🌊 Simulate Ticket Storm", type="primary"):
        storm_text = "MAJOR OUTAGE: The production database is completely down and no one can log in!"
        for i in range(1, 16):
            requests.post(API_URL, json={"id": f"STORM-UI-{i:02d}", "text": storm_text})
        st.success("Storm Dispatched! Watch the logs...")

with col2:
    st.subheader("🖥️ Live Worker Terminal")
    
    # Auto-refreshing logic for the logs
    if st.button("🔄 Refresh Logs"):
        pass # Streamlit reruns the script on any button click!
        
    try:
        # Fetch logs from FastAPI
        response = requests.get(LOGS_URL)
        if response.status_code == 200:
            logs = response.json().get("logs", [])
            if logs:
                # Format logs with line breaks
                log_text = "\n".join(logs)
                # Display in a dark code block
                st.code(log_text, language="bash")
            else:
                st.code("Waiting for worker logs...", language="bash")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is FastAPI running?")