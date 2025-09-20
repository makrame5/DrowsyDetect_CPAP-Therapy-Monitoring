import cv2
import numpy as np
import mediapipe as mp
from pygame import mixer
import time
from scipy.spatial import distance

mixer.init()
mixer.music.load("music.wav")

eye_thresh = 0.25
mar_thresh = 0.5
frame_check = 20
frame_check1 = 35

# Indices Mediapipe pour les yeux et la bouche (468 points)
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]
MOUTH_IDX = [78, 308, 13, 14, 17, 82, 87, 317, 314, 402, 317, 324]

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[2], mouth[10])
    B = distance.euclidean(mouth[4], mouth[8])
    C = distance.euclidean(mouth[0], mouth[6])
    mar = (A + B) / (2.0 * C)
    return mar

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)
flag = 0
mouth_flag = 0
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        continue
    frame = cv2.resize(frame, (450, 320))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape
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
            print(flag)
            if mouth_flag >= frame_check1:
                cv2.putText(frame, "Attention signe de fatigue! Reposez-vous", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            mouth_flag = 0
        if ear < eye_thresh:
            flag += 1
            print(flag)
            if flag >= frame_check:
                cv2.putText(frame, "****************ALERT!****************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "****************ALERT!****************", (10, 315),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                mixer.music.play()
        else:
            flag = 0
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.release()