import cv2
import pyttsx3
import threading
import time
import os
import queue

class ObjectDetector:
    def __init__(self, backend_dir=None):
        if backend_dir is None:
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.class_file = os.path.join(backend_dir, 'coco.names')
        self.config_path = os.path.join(backend_dir, 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
        self.weights_path = os.path.join(backend_dir, 'frozen_inference_graph.pb')
        
        self.class_names = []
        if os.path.exists(self.class_file):
            with open(self.class_file, 'rt') as f:
                self.class_names = [line.strip() for line in f.read().strip().split('\n') if line.strip()]
        
        self.net = None
        self.init_model()
        
        self.cap = None
        self.is_running = False
        self.audio_enabled = True
        self.threshold = 0.45
        
        self.current_detections = []
        self.last_spoken = {}
        self.speech_cooldown = 4.0  # seconds between repeating the same object
        
        # Audio Queue and Worker Thread
        self.speech_queue = queue.Queue()
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        # Threaded Camera Frame Capture State
        self.latest_frame = None
        self.frame_lock = threading.Lock()
        self.capture_thread = None
        
        # Async Detection Overlay State
        self.latest_bboxes = []
        self.detection_thread = None
        
        self.lock = threading.Lock()

    def init_model(self):
        if os.path.exists(self.weights_path) and os.path.exists(self.config_path):
            try:
                self.net = cv2.dnn_DetectionModel(self.weights_path, self.config_path)
                self.net.setInputSize(320, 320)
                self.net.setInputScale(1.0 / 127.5)
                self.net.setInputMean((127.5, 127.5, 127.5))
                self.net.setInputSwapRB(True)
                print("[Detector] Model loaded successfully.")
            except Exception as e:
                print(f"[Detector] Error loading DNN model: {e}")
                self.net = None

    def _speech_worker(self):
        try:
            tts_engine = pyttsx3.init()
            tts_engine.setProperty('rate', 160)
        except Exception as e:
            print(f"[Detector] Could not initialize pyttsx3: {e}")
            tts_engine = None

        while True:
            text = self.speech_queue.get()
            if text is None:
                break
            if self.audio_enabled and tts_engine:
                try:
                    tts_engine.say(text)
                    tts_engine.runAndWait()
                except Exception as e:
                    print(f"[Detector] Speech error: {e}")
            self.speech_queue.task_done()

    def speak_async(self, text):
        now = time.time()
        if text in self.last_spoken:
            if now - self.last_spoken[text] < self.speech_cooldown:
                return
        self.last_spoken[text] = now
        if self.audio_enabled:
            # Drain queue if too long to avoid lagging behind
            if self.speech_queue.qsize() > 2:
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except queue.Empty:
                    pass
            self.speech_queue.put(text)

    def _capture_worker(self):
        """Continuously grab frames from camera to prevent hardware queue lag."""
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                with self.frame_lock:
                    self.latest_frame = frame
            else:
                time.sleep(0.01)

    def _detection_worker(self):
        """Run AI detection asynchronously to avoid slowing down frame streaming."""
        while self.is_running:
            frame_to_process = None
            with self.frame_lock:
                if self.latest_frame is not None:
                    frame_to_process = self.latest_frame.copy()

            if frame_to_process is not None and self.net:
                try:
                    class_ids, confs, bbox = self.net.detect(frame_to_process, confThreshold=self.threshold)
                    detected_names = []
                    boxes = []
                    
                    if len(class_ids) != 0:
                        for class_id, confidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                            if 0 < class_id <= len(self.class_names):
                                name = self.class_names[class_id - 1]
                                label = f"{name.upper()} {int(confidence * 100)}%"
                                det_info = {
                                    "name": name,
                                    "confidence": round(float(confidence) * 100, 1)
                                }
                                detected_names.append(det_info)
                                boxes.append((box, label, name))
                                
                                # Trigger speech
                                self.speak_async(f"{name} detected")
                                
                    with self.lock:
                        self.current_detections = detected_names
                        self.latest_bboxes = boxes
                except Exception as e:
                    print(f"[Detector] Async detection error: {e}")
            
            # Run detection ~15 times a second to save CPU while keeping high accuracy
            time.sleep(0.06)

    def start_camera(self):
        with self.lock:
            if self.is_running and self.cap and self.cap.isOpened():
                return True

            print("[Detector] Initializing high-speed camera capture...")
            # Try DirectShow (CAP_DSHOW) on Windows first for ultra-fast startup (<200ms)
            if os.name == 'nt':
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(0)

            if not self.cap or not self.cap.isOpened():
                print("[Detector] CAP_DSHOW failed, falling back to default VideoCapture(0)...")
                self.cap = cv2.VideoCapture(0)

            if self.cap and self.cap.isOpened():
                # Fast hardware capture configuration
                self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                
                self.is_running = True
                
                # Start frame capture thread
                self.capture_thread = threading.Thread(target=self._capture_worker, daemon=True)
                self.capture_thread.start()
                
                # Start async AI detection thread
                self.detection_thread = threading.Thread(target=self._detection_worker, daemon=True)
                self.detection_thread.start()

                print("[Detector] Camera initialized instantly!")
                return True
            else:
                print("[Detector] Failed to open camera.")
                self.cap = None
                self.is_running = False
                return False

    def stop_camera(self):
        with self.lock:
            self.is_running = False
            if self.cap:
                self.cap.release()
                self.cap = None
            self.latest_frame = None
            self.latest_bboxes = []
            self.current_detections = []
            print("[Detector] Camera stopped.")

    def toggle_audio(self, enabled=None):
        if enabled is None:
            self.audio_enabled = not self.audio_enabled
        else:
            self.audio_enabled = bool(enabled)
        return self.audio_enabled

    def generate_frames(self):
        if not self.is_running:
            if not self.start_camera():
                return

        jpeg_params = [int(cv2.IMWRITE_JPEG_QUALITY), 75]

        while self.is_running:
            frame = None
            with self.frame_lock:
                if self.latest_frame is not None:
                    frame = self.latest_frame.copy()

            if frame is None:
                time.sleep(0.01)
                continue

            # Overlay bounding boxes from latest detection thread
            with self.lock:
                boxes = list(self.latest_bboxes)

            for box, label, name in boxes:
                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, label, (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Fast JPEG encode
            ret, buffer = cv2.imencode('.jpg', frame, jpeg_params)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Target ~30 FPS output
            time.sleep(0.02)

        self.stop_camera()

    def get_status(self):
        with self.lock:
            return {
                "is_running": self.is_running,
                "audio_enabled": self.audio_enabled,
                "detections": self.current_detections,
                "total_detected": len(self.current_detections)
            }

