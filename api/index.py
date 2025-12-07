import sys
import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path to import main.py
from main import preprocess_image, extract_edges, detect_contours

app = Flask(__name__)
CORS(app)

def encode_image(image):
    """Encode image to base64 string."""
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/process', methods=['POST'])
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
