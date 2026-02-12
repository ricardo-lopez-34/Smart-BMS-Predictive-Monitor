import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="Pro-BMS Analytics", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .status-card { padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'data_log' not in st.session_state:
    st.session_state.data_log = pd.DataFrame(columns=['Timestamp', 'Voltage', 'Temp', 'SoC'])

st.sidebar.title("🛠️ BMS Control")
refresh_speed = st.sidebar.slider("Data Interval (s)", 1, 10, 2)
alert_temp = st.sidebar.number_input("Max Temp (°C)", value=48)

st.title("Enterprise Smart BMS Dashboard")
st.caption(f"Sync Status: Active | Local Time: {datetime.now().strftime('%H:%M:%S')}")

placeholder = st.empty()

for _ in range(100):
    v = round(np.random.uniform(3.7, 4.2), 2)
    t = round(np.random.uniform(25.0, 55.0), 1)
    s = round((v - 3.2) / (4.2 - 3.2) * 100, 1)
    
    entry = pd.DataFrame([[datetime.now().strftime('%H:%M:%S'), v, t, s]], columns=st.session_state.data_log.columns)
    st.session_state.data_log = pd.concat([st.session_state.data_log, entry]).tail(15)

    with placeholder.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Battery Voltage", f"{v}V", delta="Cell 1")
        c2.metric("System Temp", f"{t}°C", delta_color="inverse")
        c3.metric("State of Charge", f"{s}%")
        c4.metric("State of Health", "99.1%")

        if t > alert_temp:
            st.markdown(f'<div class="status-card" style="background-color: #e74c3c;">🚨 CRITICAL: OVERHEATING DETECTED ({t}°C)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-card" style="background-color: #2ecc71;">🔋 SYSTEM STATUS: OPTIMAL</div>', unsafe_allow_html=True)

        g1, g2 = st.columns([2, 1])
        with g1:
            fig = px.line(st.session_state.data_log, x='Timestamp', y=['Voltage', 'Temp'], title="Real-time Telemetry Stream")
            st.plotly_chart(fig, use_container_width=True)
        with g2:
            gauge = go.Figure(go.Indicator(mode="gauge+number", value=s, title={'text': "Current SoC"},
                                           gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#2ecc71"}}))
            st.plotly_chart(gauge, use_container_width=True)
            
    time.sleep(refresh_speed)
