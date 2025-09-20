import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
import pandas as pd
from streamlit_echarts import st_echarts

# --- PARAMS ---
eye_thresh = 0.25
mar_thresh = 0.5
frame_check = 20
frame_check1 = 35


# --- MEDIAPIPE ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)


# --- FONCTIONS ---

# Indices Mediapipe pour les yeux et la bouche (468 points)
# Left eye: [33, 160, 158, 133, 153, 144]
# Right eye: [362, 385, 387, 263, 373, 380]
# Mouth: [78, 308, 13, 14, 17, 82, 87, 317, 314, 402, 317, 324]
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]
MOUTH_IDX = [78, 308, 13, 14, 17, 82, 87, 317, 314, 402, 317, 324]

def eye_aspect_ratio(eye):
    from scipy.spatial import distance
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    from scipy.spatial import distance
    A = distance.euclidean(mouth[2], mouth[10])
    B = distance.euclidean(mouth[4], mouth[8])
    C = distance.euclidean(mouth[0], mouth[6])
    mar = (A + B) / (2.0 * C)
    return mar

# --- STREAMLIT UI ---
st.set_page_config(page_title="Health Drowsiness Detection", layout="wide")

# Header
st.markdown("""
    <div style='background-color:#1976D2; padding: 1rem 2rem; border-radius: 10px 10px 0 0; display: flex; align-items: center;'>
        <span style='font-size:2rem; margin-right:1rem;'>🏥</span>
        <span style='font-size:1.5rem; color:white; font-family:Roboto;'>Health Drowsiness Detection</span>
        <span style='flex:1'></span>
        <span style='color:white; font-size:1.1rem; margin-right:2rem;'>Dashboard | Patients | Settings</span>
    </div>
""", unsafe_allow_html=True)
st.markdown(f"""
    <div style='background-color:#E3EAF5; padding: 0.5rem 2rem; border-radius: 0 0 10px 10px; display: flex; align-items: center;'>
        <span style='font-size:1.1rem; color:#1976D2; font-family:Roboto;'>Patient ID: <b>123456</b></span>
        <span style='flex:1'></span>
        <span style='font-size:1.1rem; color:#1976D2; font-family:Roboto;'>
            Date/Heure: <b>{time.strftime('%d/%m/%Y %H:%M:%S')}</b>
        </span>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

# --- Variables d'état ---
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'vigilance' not in st.session_state:
    st.session_state['vigilance'] = []

# --- ZONE CENTRALE ---
with col1:
    st.markdown("""
        <div style='background:#fff; border-radius:20px; box-shadow:0 2px 8px #0001; padding:2rem; margin-bottom:1rem;'>
            <h3 style='color:#1976D2; font-family:Roboto;'>Surveillance vidéo en direct</h3>
    """, unsafe_allow_html=True)
    run = st.button("Démarrer la surveillance vidéo")
    video_placeholder = st.empty()
    status_placeholder = st.empty()
    if run:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            status_placeholder.error("Caméra non accessible (cv2.VideoCapture(0) a échoué). Vérifiez que la webcam n'est pas utilisée par une autre application et que les autorisations sont accordées.")
        else:
            flag = 0
            mouth_flag = 0
            vigilance_score = 100
            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    status_placeholder.error("Caméra non accessible (lecture impossible). Vérifiez la connexion de la webcam.")
                    break
                frame = cv2.resize(frame, (640, 480))  # Taille intermédiaire
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)
                status = "🟢 ÉVEILLÉ"
                color = "#4CAF50"
                if results.multi_face_landmarks:
                    face_landmarks = results.multi_face_landmarks[0]
                    h, w, _ = frame.shape
                    # Récupérer les points des yeux et de la bouche
                    leftEye = np.array([[int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)] for i in LEFT_EYE_IDX])
                    rightEye = np.array([[int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)] for i in RIGHT_EYE_IDX])
                    mouth = np.array([[int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)] for i in MOUTH_IDX])
                    leftEAR = eye_aspect_ratio(leftEye)
                    rightEAR = eye_aspect_ratio(rightEye)
                    mar = mouth_aspect_ratio(mouth)
                    ear = (leftEAR + rightEAR) / 2.0
                    # Dessiner les points
                    for pt in leftEye:
                        cv2.circle(frame, tuple(pt), 2, (0,255,0), -1)
                    for pt in rightEye:
                        cv2.circle(frame, tuple(pt), 2, (0,255,0), -1)
                    for pt in mouth:
                        cv2.circle(frame, tuple(pt), 2, (255,0,0), -1)
                    if mar > mar_thresh:
                        mouth_flag += 1
                        if mouth_flag >= frame_check1:
                            status = "🟠 SOMNOLENT"
                            color = "#FFA000"
                            st.session_state['history'].append({
                                'Heure': time.strftime('%H:%M:%S'),
                                'Alerte': status
                            })
                            vigilance_score = max(vigilance_score-10, 0)
                    else:
                        mouth_flag = 0
                    if ear < eye_thresh:
                        flag += 1
                        if flag >= frame_check:
                            status = "🔴 SOMMEIL PROFOND"
                            color = "#D32F2F"
                            st.session_state['history'].append({
                                'Heure': time.strftime('%H:%M:%S'),
                                'Alerte': status
                            })
                            vigilance_score = max(vigilance_score-20, 0)
                    else:
                        flag = 0
                st.session_state['vigilance'].append(vigilance_score)
                # Affichage vidéo
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)  # Affiche en largeur max
                status_placeholder.markdown(f"<div style='margin-top:1rem; font-size:1.2rem; font-weight:bold; color:{color};'>{status}</div>", unsafe_allow_html=True)
                if st.button("Arrêter", key=f"stop_{time.time_ns()}"):
                    break
            cap.release()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANNEAU LATÉRAL ---
with col2:
    st.markdown("""
        <div style='background:#fff; border-radius:20px; box-shadow:0 2px 8px #0001; padding:1.5rem; margin-bottom:1.5rem;'>
            <h4 style='color:#1976D2; font-family:Roboto;'>Historique des détections</h4>
    """, unsafe_allow_html=True)
    # Historique réel
    if st.session_state['history']:
        data = pd.DataFrame(st.session_state['history'])
        st.dataframe(data, hide_index=True)
    else:
        st.info("Aucun événement détecté pour l'instant.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='background:#fff; border-radius:20px; box-shadow:0 2px 8px #0001; padding:1.5rem;'>
            <h4 style='color:#1976D2; font-family:Roboto;'>Courbe de vigilance</h4>
    """, unsafe_allow_html=True)
    # Courbe réelle
    if st.session_state['vigilance']:
        option = {
            "xAxis": {"type": "category", "data": [str(i) for i in range(len(st.session_state['vigilance']))]},
            "yAxis": {"type": "value"},
            "series": [{
                "data": st.session_state['vigilance'],
                "type": "line",
                "smooth": True,
                "lineStyle": {"color": "#1976D2", "width": 3},
                "areaStyle": {"color": "#E3EAF5"}
            }],
            "tooltip": {"trigger": "axis"},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True}
        }
        st_echarts(option, height="200px")
    else:
        st.info("Aucune donnée de vigilance pour l'instant.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
    <style>
    body, .stApp { background: #F5F7FA !important; font-family: Roboto, Arial, sans-serif; }
    .stDataFrame thead tr th { background: #E3EAF5 !important; color: #1976D2 !important; }
    </style>
""", unsafe_allow_html=True)
