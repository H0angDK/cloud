from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    if not data or 'coordinates' not in data:
        return jsonify({'error': 'No coordinates provided'}), 400
    
    # Simulate processing coordinates and calculating speed
    speed = random.uniform(30, 120)  # Random speed between 30 and 120 km/h
    
    return jsonify({
        'coordinates': data['coordinates'],
        'speed': round(speed, 2),
        'unit': 'km/h'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 