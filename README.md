# 🖐️ Hand Gesture Recognition System

A real-time hand gesture recognition system that controls your computer using hand gestures detected through your webcam. Built with Python, OpenCV, and MediaPipe.

---

## ✨ Features

| Gesture | Action |
|---|---|
| 👍 Thumbs Up | Volume Up |
| 👎 Thumbs Down | Volume Down |
| 🤏 Pinch (thumb + index) | Take Screenshot |
| ✌️ Peace Sign | Play / Pause Media |
| ✋ Open Palm (move up/down) | Adjust Brightness |

---

## 🛠️ Tech Stack

- **Python 3.x**
- **OpenCV** – Webcam capture and frame rendering
- **MediaPipe** – Hand landmark detection
- **PyAutoGUI** – Keyboard/system action automation
- **screen-brightness-control** *(optional)* – Precise brightness control

---

## 📋 Prerequisites

- Python 3.7 or higher
- A working webcam
- Windows / Linux / macOS

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/hand-gesture-recognition.git
   cd hand-gesture-recognition
   ```

2. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe pyautogui
   ```

3. ***(Optional)* Install brightness control**
   ```bash
   pip install screen-brightness-control
   ```

---

## ▶️ Usage

```bash
python main.py
```

- Allow webcam access when prompted.
- Perform gestures in front of the camera.
- Press **`ESC`** to exit.

---

## 🎮 Gesture Guide

### 👍 Volume Up
Keep your **thumb pointing upward** with the rest of the fingers closed.

### 👎 Volume Down
Point your **thumb downward** with the rest of the fingers closed.

### 🤏 Screenshot (Pinch)
Bring your **thumb tip and index finger tip close together** (within ~40px on screen).  
Screenshot is saved as `screenshot_<timestamp>.png` in the project directory.

### ✌️ Peace Sign → Play/Pause
Extend your **index and middle fingers** while keeping ring and pinky folded.

### ✋ Open Palm → Brightness
Extend **index, middle, and ring fingers**. Move your hand **up** to increase brightness, **down** to decrease it.

---

## ⚙️ Configuration

You can tweak these values in `main.py`:

| Parameter | Default | Description |
|---|---|---|
| `max_num_hands` | `1` | Number of hands to track |
| `min_detection_confidence` | `0.75` | Hand detection threshold |
| `min_tracking_confidence` | `0.75` | Hand tracking threshold |
| `cooldown` | `1.2s` | Delay between repeated actions |

---

## 📁 Project Structure

```
hand-gesture-recognition/
│
├── main.py          # Main application entry point
└── README.md        # Project documentation
```

---

## 🔧 Troubleshooting

**Webcam not detected**  
Make sure no other application is using the webcam. Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`.

**Brightness control not working**  
`screen-brightness-control` may not support all hardware. The app will fall back to keyboard brightness keys automatically.

**Gestures triggering incorrectly**  
Ensure good lighting and keep your hand clearly visible within the camera frame.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [MediaPipe](https://mediapipe.dev/) by Google for hand landmark detection
- [OpenCV](https://opencv.org/) for real-time video processing
