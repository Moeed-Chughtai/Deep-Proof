from flask import Flask, request, jsonify
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from efficientnet.tfkeras import EfficientNetB0
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the model
model = tf.keras.models.load_model(r'C:\Users\moeed\Documents\1 Programming\Deep-Proof\backend\tmp_checkpoint\best_model.keras')

# Load EfficientNetB0 model for preprocessing
efficient_net = EfficientNetB0(weights='imagenet', include_top=False, pooling='max')
input_size = 128

def preprocess_image(image):
    image = cv2.resize(image, (input_size, input_size))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'video' not in request.files:
        app.logger.debug("No video file provided in request")
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    
    app.logger.debug("Received video file:", video_file.filename)
    app.logger.debug("File size:", len(video_file.read()))
    
    video_file.seek(0)

    # Save the uploaded video to a temporary file
    video_path = './temp_video.mp4'
    video_file.save(video_path)

    cap = cv2.VideoCapture(video_path)
    predictions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        image = preprocess_image(frame)
        pred = model.predict(image)
        predictions.append(float(pred[0][0]))
    
    cap.release()
    os.remove(video_path)
    
    return jsonify({'predictions': predictions})


if __name__ == '__main__':
    app.run(debug=True)
