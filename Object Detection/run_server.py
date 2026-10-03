import os
import sys
import webbrowser
import time
import threading

# Path setup
root_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root_dir, 'object-detection-for-blind-main', 'Backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import app

def open_browser():
    time.sleep(1.5)
    print("Opening web app in browser: http://localhost:5000")
    webbrowser.open("http://localhost:5000")

if __name__ == '__main__':
    print("==================================================")
    print(" OpenCV Blind Vision - Full Stack Server")
    print("==================================================")
    print(f"Backend Path: {backend_dir}")
    print("Serving Application on: http://localhost:5000")
    print("Press Ctrl+C to stop the server.")
    print("--------------------------------------------------")

    # Auto open browser thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Flask Server
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
