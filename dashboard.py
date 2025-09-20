import streamlit as st
import datetime
import pandas as pd
from streamlit_echarts import st_echarts

# --- HEADER ---
st.set_page_config(page_title="Health Drowsiness Detection", layout="wide")

# Top bar
with st.container():
    st.markdown("""
        <div style='background-color:#1976D2; padding: 1rem 2rem; border-radius: 10px 10px 0 0; display: flex; align-items: center;'>
            <span style='font-size:2rem; margin-right:1rem;'>🏥</span>
            <span style='font-size:1.5rem; color:white; font-family:Roboto;'>Health Drowsiness Detection</span>
            <span style='flex:1'></span>
            <span style='color:white; font-size:1.1rem; margin-right:2rem;'>Dashboard | Patients | Settings</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color:#E3EAF5; padding: 0.5rem 2rem; border-radius: 0 0 10px 10px; display: flex; align-items: center;'>
            <span style='font-size:1.1rem; color:#1976D2; font-family:Roboto;'>Patient ID: <b>123456</b></span>
            <span style='flex:1'></span>
            <span style='font-size:1.1rem; color:#1976D2; font-family:Roboto;'>
                Date/Heure: <b id="datetime"></b>
            </span>
        </div>
        <script>
        function updateDateTime() {
            document.getElementById('datetime').innerText = new Date().toLocaleString();
        }
        setInterval(updateDateTime, 1000);
        updateDateTime();
        </script>
    """, unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([2, 1], gap="large")

# --- ZONE CENTRALE ---
with col1:
    st.markdown("""
        <div style='background:#fff; border-radius:20px; box-shadow:0 2px 8px #0001; padding:2rem; margin-bottom:1rem;'>
            <h3 style='color:#1976D2; font-family:Roboto;'>Surveillance vidéo en direct</h3>
            <div style='display:flex; flex-direction:column; align-items:center;'>
                <div style='background:#F5F7FA; border-radius:16px; width:420px; height:320px; display:flex; align-items:center; justify-content:center; border:2px solid #E3EAF5;'>
                    <span style='color:#B0B0B0;'>[Flux vidéo ici]</span>
                </div>
                <div style='margin-top:1rem; font-size:1.2rem; font-weight:bold; color:#4CAF50;'>🟢 ÉVEILLÉ</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- PANNEAU LATÉRAL ---
with col2:
    st.markdown("""
        <div style='background:#fff; border-radius:20px; box-shadow:0 2px 8px #0001; padding:1.5rem; margin-bottom:1.5rem;'>
            <h4 style='color:#1976D2; font-family:Roboto;'>Historique des détections</h4>
    """, unsafe_allow_html=True)
    # Historique factice
    data = pd.DataFrame({
        'Heure': [datetime.datetime.now().strftime('%H:%M:%S')]*3,
        'Alerte': ['🟢 ÉVEILLÉ', '🟠 SOMNOLENT', '🔴 SOMMEIL PROFOND']
    })
    st.dataframe(data, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='background:#fff; border-radius:20px; box-shadow:0 2px 8px #0001; padding:1.5rem;'>
            <h4 style='color:#1976D2; font-family:Roboto;'>Courbe de vigilance</h4>
    """, unsafe_allow_html=True)
    # Courbe factice
    option = {
        "xAxis": {"type": "category", "data": ["10:00", "10:05", "10:10", "10:15", "10:20"]},
        "yAxis": {"type": "value"},
        "series": [{
            "data": [100, 80, 60, 40, 20],
            "type": "line",
            "smooth": True,
            "lineStyle": {"color": "#1976D2", "width": 3},
            "areaStyle": {"color": "#E3EAF5"}
        }],
        "tooltip": {"trigger": "axis"},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True}
    }
    st_echarts(option, height="200px")
    st.markdown("</div>", unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
    <style>
    body, .stApp { background: #F5F7FA !important; font-family: Roboto, Arial, sans-serif; }
    .stDataFrame thead tr th { background: #E3EAF5 !important; color: #1976D2 !important; }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    import os
    os.system("streamlit run dashboard.py")
