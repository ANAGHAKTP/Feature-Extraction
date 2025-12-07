import sys
import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variable to store import error
import_error = None

# Ensure current directory is in path for Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Add parent directory to path to import main.py
    from main import preprocess_image, extract_edges, detect_contours
except ImportError as e:
    import_error = str(e)
    # Define dummy functions so the code doesn't crash immediately on load
    def preprocess_image(img): raise ImportError(import_error)
    def extract_edges(img): raise ImportError(import_error)
    def detect_contours(img): raise ImportError(import_error)

@app.route('/', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    if import_error:
        return jsonify({'status': 'error', 'message': f'Import failed: {import_error}'}), 500
    return jsonify({'status': 'ok', 'message': 'Feature Extraction API is running'}), 200

# Catch-all to debug path issues
@app.route('/<path:subpath>', methods=['GET', 'POST'])
def catch_all(subpath):
    return jsonify({
        'error': 'Path not found by Flask routing',
        'received_path': subpath,
        'method': request.method,
        'url': request.url
    }), 404

# Alias for direct invocation if Vercel passes the file path
@app.route('/api/index.py', methods=['GET', 'POST'])
@app.route('/process', methods=['GET', 'POST'])
def process_route():
    if request.method == 'GET':
        return health_check()
    return process_image()

def encode_image(image):
    """Encode image to base64 string."""
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read image from file
    file_bytes = np.frombuffer(file.read(), np.uint8)
    original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if original_image is None:
        return jsonify({'error': 'Invalid image'}), 400

    try:
        # Process image
        preprocessed_image = preprocess_image(original_image)
        edges = extract_edges(preprocessed_image)
        contours = detect_contours(edges)

        # Create contour image
        contour_image = np.zeros_like(original_image)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

        # Convert to base64
        original_b64 = encode_image(original_image)
        edges_b64 = encode_image(edges)
        contours_b64 = encode_image(contour_image)

        return jsonify({
            'original': f"data:image/png;base64,{original_b64}",
            'edges': f"data:image/png;base64,{edges_b64}",
            'contours': f"data:image/png;base64,{contours_b64}"
        })

    except Exception as e:
        import traceback
        traceback.print_exc() # Print to Vercel logs
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
