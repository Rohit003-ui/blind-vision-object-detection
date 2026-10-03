# Blind Vision – Real-Time Object Detection for Visually Impaired Users

A real-time computer vision application designed to assist visually impaired users by detecting objects through a webcam and providing spoken audio feedback.

The system uses **OpenCV and SSD MobileNet** for real-time object detection and **Python text-to-speech** to announce detected objects. A **Flask backend** connects the computer vision system with a modern web-based interface.

## Features

* Real-time object detection using a webcam
* SSD MobileNet V3 object detection model
* OpenCV-based computer vision processing
* Detection confidence scores
* Bounding boxes around detected objects
* Text-to-speech audio feedback
* Enable/disable audio feedback
* Live detection status
* Browser-based user interface
* Flask REST API
* Asynchronous camera capture and object detection
* Responsive frontend interface

## How It Works

The application follows this workflow:

```text
Webcam
   ↓
OpenCV Frame Capture
   ↓
SSD MobileNet Object Detection
   ↓
Detected Objects + Confidence
   ↓
Bounding Boxes on Live Video
   ↓
Text-to-Speech
   ↓
Audio Feedback to User
```

The webcam continuously captures frames. OpenCV processes these frames using the SSD MobileNet model. When an object is detected, the application identifies the object and calculates its confidence score.

For example:

```text
Person detected
Bottle detected
Chair detected
Car detected
```

The detected object is displayed on the live video stream and can also be announced using text-to-speech.

## Technologies Used

### Backend

* Python
* Flask
* OpenCV
* SSD MobileNet V3
* pyttsx3
* NumPy

### Frontend

* HTML5
* CSS3
* JavaScript

### Computer Vision

* OpenCV DNN module
* SSD MobileNet V3 Large COCO
* COCO object classes

## Project Structure

```text
blind-vision-object-detection/
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── img.png
│
├── backend/
│   ├── app.py
│   ├── detector.py
│   ├── requirements.txt
│   ├── coco.names
│   ├── frozen_inference_graph.pb
│   └── ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt
│
├── run_server.py
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/blind-vision-object-detection.git
```

Move into the project directory:

```bash
cd blind-vision-object-detection
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

## Running the Application

Start the Flask server from the project root:

```bash
python run_server.py
```

The application will start at:

```text
http://localhost:5000
```

The browser can then be used to access the Blind Vision interface.

## Using the Application

1. Connect a webcam to the computer.
2. Start the Flask application.
3. Open the application in a browser.
4. Start live detection.
5. The webcam stream will appear in the detection section.
6. Detected objects will be displayed with bounding boxes.
7. Detection confidence scores will be shown.
8. Audio feedback can be enabled or disabled using the audio control.

## Object Detection Model

The project uses the **SSD MobileNet V3 Large COCO** object detection model through OpenCV's DNN module.

The model uses:

* `frozen_inference_graph.pb` – trained model weights
* `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt` – model configuration
* `coco.names` – object class names

The detection threshold used by the application is approximately:

```text
0.45
```

Only detections above the configured confidence threshold are considered.

## Real-Time Processing

The backend uses separate processing threads for:

* Webcam frame capture
* Object detection
* Text-to-speech processing

This helps prevent the object detection process and audio feedback from unnecessarily blocking the live video stream.

The application also uses a speech cooldown mechanism to reduce repeated announcements of the same object.

## Flask API

The backend provides several API endpoints.

| Endpoint               | Method | Purpose                            |
| ---------------------- | ------ | ---------------------------------- |
| `/api/video_feed`      | GET    | Provides the live camera stream    |
| `/api/start_detection` | POST   | Starts camera detection            |
| `/api/stop_detection`  | POST   | Stops camera detection             |
| `/api/toggle_audio`    | POST   | Enables or disables audio feedback |
| `/api/status`          | GET    | Returns current detection status   |
| `/api/contact`         | POST   | Handles contact form submissions   |

## Accessibility Purpose

The main goal of this project is to explore how computer vision can be used to provide environmental awareness for visually impaired users.

Instead of requiring the user to continuously look at a screen, detected objects can be communicated through audio feedback.

This project is intended as a **prototype and educational computer vision application**, not as a certified assistive device or safety-critical system.

## Limitations

* Detection accuracy depends on lighting and camera quality.
* The system requires a webcam.
* The available object classes depend on the COCO-trained model.
* Real-time performance depends on the computer's hardware.
* Text-to-speech behavior depends on the operating system and available speech engine.
* The prototype should not be relied upon as the sole navigation or safety system for visually impaired users.

## Future Improvements

Possible improvements include:

* Distance estimation for detected objects
* Object tracking across video frames
* Obstacle proximity warnings
* Voice commands
* GPS and navigation assistance
* Mobile application support
* Support for additional trained object classes
* Edge-device deployment
* Improved detection performance
* Multi-language audio feedback

## Learning Outcomes

Through this project, I worked with:

* Real-time computer vision
* OpenCV DNN
* Object detection
* SSD MobileNet
* Flask API development
* Python multithreading
* Webcam streaming
* Text-to-speech integration
* HTML, CSS and JavaScript
* Frontend-backend integration

## Author

**Rohit M.**

Computer Science & Engineering Student

* GitHub: https://github.com/Rohit003-ui
* LinkedIn: https://linkedin.com/in/rohit-m28022005/

## License

This project is intended for educational and portfolio purposes.
