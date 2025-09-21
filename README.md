# 🏥 DrowsyDetect

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Non-invasive daytime drowsiness monitoring for CPAP follow-up**

[🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [🔧 Installation](#-installation) • [📖 Documentation](#-documentation)

</div>

---

## 📋 About

**DrowsyDetect** is an innovative solution for non-invasive monitoring of daytime drowsiness, designed as a key indicator of the severity and effectiveness of CPAP (Continuous Positive Airway Pressure) treatment.

Through recording and analysis of data history, it enables precise longitudinal follow-up. By analyzing in real-time visual biomarkers such as **PERCLOS**, **blink frequency**, and **head movements**, it helps detect vigilance impairment and prevent accident risks, thus complementing traditional clinical monitoring.

### 🎯 Objectives

- **Early detection** of daytime drowsiness
- **Longitudinal follow-up** of CPAP patients
- **Accident prevention** related to fatigue
- **Complement to traditional clinical** monitoring

---

## ✨ Features

### 🔍 Real-time Detection
- **Eye analysis** : Eye Aspect Ratio (EAR) calculation
- **Mouth analysis** : Yawn detection (MAR)
- **Continuous monitoring** : 24/7 vigilance monitoring
- **Smart alerts** : Audio and visual notifications

### 📊 Interactive Dashboard
- **Streamlit interface** modern and intuitive
- **Real-time visualization** of biomarkers
- **Detection history** with timestamping
- **Dynamic vigilance curves**
- **Data export** for clinical analysis

### 🏥 Clinical Integration
- **Patient identification** with unique ID
- **Longitudinal data recording**
- **Automated analysis reports**
- **Professional interface** adapted to medical environment

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam or USB camera
- 4 GB RAM minimum

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/makrame5/DrowsyDetect_CPAP-Therapy-Monitoring.git
cd DrowsyDetect_CPAP-Therapy-Monitoring
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Launch the application**
```bash
# Dashboard version (recommended)
streamlit run dashboard_live.py

# Console version
python main.py
```

### 🎮 Usage

1. **Start monitoring** : Click on "Start video monitoring"
2. **Positioning** : Position yourself in front of the camera
3. **Monitoring** : Monitor real-time indicators
4. **Analysis** : Consult history and vigilance curves

---

## 🔧 Detailed Installation

### Main Dependencies

```txt
opencv-python==4.8.1.78
mediapipe==0.10.7
streamlit==1.28.1
streamlit-echarts==0.4.2
numpy==1.24.3
pandas==2.0.3
scipy==1.11.3
pygame==2.5.2
```

### System Configuration

#### Windows
```bash
# Install dependencies
pip install opencv-python mediapipe streamlit streamlit-echarts numpy pandas scipy pygame

# Download facial detection model
# The shape_predictor_68_face_landmarks.dat file must be present
```

#### Linux/macOS
```bash
# Install system dependencies
sudo apt-get install python3-opencv  # Ubuntu/Debian
brew install opencv                   # macOS

# Python installation
pip install -r requirements.txt
```

---

## 📖 Documentation

### System Architecture

```
DrowsyDetect/
├── 📁 main.py                 # Main console version
├── 📁 dashboard.py            # Static dashboard interface
├── 📁 dashboard_live.py       # Real-time dashboard interface
├── 📁 requirements.txt        # Python dependencies
├── 📁 music.wav              # Alert audio file
├── 📁 shape_predictor_68_face_landmarks.dat  # Detection model
└── 📁 README.md              # Documentation
```

### Detection Algorithms

#### 1. Eye Aspect Ratio (EAR)
```python
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
```

#### 2. Mouth Aspect Ratio (MAR)
```python
def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[2], mouth[10])
    B = distance.euclidean(mouth[4], mouth[8])
    C = distance.euclidean(mouth[0], mouth[6])
    mar = (A + B) / (2.0 * C)
    return mar
```

### Detection Thresholds

| Biomarker | Threshold | Description |
|-----------|-----------|-------------|
| **EAR** | < 0.25 | Eyes closed (sleep) |
| **MAR** | > 0.5 | Yawning (fatigue) |
| **Frames** | 20-35 | Persistence for validation |

---

## 🎨 User Interface

### Main Dashboard
- **Video zone** : Real-time display with detection points
- **Indicators** : Vigilance status (Awake/Drowsy/Sleep)
- **History** : Table of detected events
- **Graphs** : Temporal vigilance curves

### Color Codes
- 🟢 **Green** : Normal awake state
- 🟠 **Orange** : Signs of drowsiness
- 🔴 **Red** : Deep sleep detected

---

## 🔬 Analyzed Biomarkers

### PERCLOS (Percentage of Eyelid Closure)
- **Definition** : Percentage of eyelid closure
- **Calculation** : Based on eye aspect ratio
- **Critical threshold** : < 80% openness

### Blink Frequency
- **Measurement** : Number of blinks per minute
- **Normal** : 15-20 blinks/min
- **Fatigue** : < 10 blinks/min

### Head Movements
- **Detection** : Analysis of facial landmarks
- **Indicators** : Head tilt, rotation
- **Thresholds** : Deviation angles > 15°

---

## 📊 Usage Examples

### Clinical Use Case
```python
# Monitoring a CPAP patient
patient_id = "123456"
session_duration = 8 * 60 * 60  # 8 hours
vigilance_threshold = 70  # Vigilance threshold

# Automatic detection
if vigilance_score < vigilance_threshold:
    trigger_alert("Drowsiness detected")
    log_event(patient_id, "fatigue", timestamp)
```

### Data Export
```python
# Save session data
data = {
    'timestamp': timestamps,
    'ear_values': ear_history,
    'mar_values': mar_history,
    'vigilance_scores': vigilance_history
}
pd.DataFrame(data).to_csv(f'session_{patient_id}.csv')
```

---

## 🛠️ Development

### Code Structure
- **Modularity** : Separate functions for each biomarker
- **Extensibility** : Open architecture for new algorithms
- **Performance** : Optimization for real-time processing
- **Maintainability** : Documented and tested code

### Adding New Biomarkers
```python
def new_biomarker(landmarks):
    # Implementation of new algorithm
    return biomarker_value

# Integration in main loop
if new_biomarker(face_landmarks) > threshold:
    trigger_alert("New biomarker detected")
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the project
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Guidelines
- Follow Python code conventions (PEP 8)
- Add tests for new features
- Document new APIs
- Maintain compatibility with existing versions

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🙏 Acknowledgments

- **MediaPipe** for facial detection
- **OpenCV** for image processing
- **Streamlit** for user interface
- **Open source community** for contributions

---

<div align="center">

**DrowsyDetect** - Intelligent vigilance monitoring

[⭐ Star this project](https://github.com/makrame5/DrowsyDetect_CPAP-Therapy-Monitoring) • [🐛 Report a bug](https://github.com/makrame5/DrowsyDetect_CPAP-Therapy-Monitoring/issues) • [💡 Request a feature](https://github.com/makrame5/DrowsyDetect_CPAP-Therapy-Monitoring/issues)

</div>
