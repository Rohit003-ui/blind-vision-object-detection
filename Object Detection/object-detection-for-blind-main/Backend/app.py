import os
import sys
from flask import Flask, Response, jsonify, request, send_from_directory

# Ensure backend directory is in path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from detector import ObjectDetector

# Path to frontend directory
frontend_dir = os.path.abspath(os.path.join(backend_dir, '..', '..', 'frontend'))

app = Flask(__name__, static_folder=frontend_dir)

# Simple CORS handling middleware
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# Initialize Detector
detector = ObjectDetector(backend_dir=backend_dir)

# --- Frontend Serving Routes ---
@app.route('/')
def serve_index():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(frontend_dir, filename)

# --- API Endpoints ---
@app.route('/api/video_feed')
def video_feed():
    return Response(
        detector.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/api/start_detection', methods=['POST', 'OPTIONS'])
def start_detection():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    success = detector.start_camera()
    return jsonify({
        "success": success,
        "message": "Camera started" if success else "Failed to open camera"
    })

@app.route('/api/stop_detection', methods=['POST', 'OPTIONS'])
def stop_detection():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    detector.stop_camera()
    return jsonify({
        "success": True,
        "message": "Camera stopped"
    })

@app.route('/api/toggle_audio', methods=['POST', 'OPTIONS'])
def toggle_audio():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json(silent=True) or {}
    enabled = data.get('enabled', None)
    current_state = detector.toggle_audio(enabled)
    return jsonify({
        "success": True,
        "audio_enabled": current_state
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(detector.get_status())

@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name', 'Anonymous')
    email = data.get('email', '')
    message = data.get('message', '')
    
    print(f"[Contact Form Received] Name: {name}, Email: {email}, Message: {message}")
    
    return jsonify({
        "success": True,
        "message": f"Thank you, {name}! Your message has been received."
    })

if __name__ == '__main__':
    print(f"Starting OpenCV Blind Vision Backend Server...")
    print(f"Serving frontend from: {frontend_dir}")
    print(f"Server accessible at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
