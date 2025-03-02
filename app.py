# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from werkzeug.utils import secure_filename

print("TensorFlow version:", tf.__version__)

# Initialize Flask app
app = Flask(__name__)

# Load trained models
vegetable_model = load_model('vegetable.h5', compile=False)
fruit_model = load_model('fruit.h5', compile=False)

# Load precaution data
try:
    veg_precautions = pd.read_excel('veg.xlsx')
    fruit_precautions = pd.read_excel('fruit.xlsx')
except Exception as e:
    print("Error loading Excel files:", e)
    veg_precautions = None
    fruit_precautions = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    caution = None  # Default value to prevent errors

    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('predict.html', caution="No file part in the request.")

        f = request.files['image']
        plant = request.form.get('plant')  # Get plant type (vegetable/fruit)

        if f.filename == '':
            return render_template('predict.html', caution="No image selected.")

        if plant not in ['vegetable', 'fruit']:
            return render_template('predict.html', caution="Invalid plant selection.")

        # Ensure uploads directory exists
        basepath = os.path.dirname(__file__)
        upload_folder = os.path.join(basepath, 'dataset')
        os.makedirs(upload_folder, exist_ok=True)

        # Save file
        file_path = os.path.join(upload_folder, secure_filename(f.filename))
        f.save(file_path)

        # Preprocess image
        img = image.load_img(file_path, target_size=(128, 128))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        # Make prediction
        if plant == 'vegetable':
            preds = np.argmax(vegetable_model.predict(x), axis=-1)
            caution = veg_precautions.iloc[preds[0]]['Precautions'] if veg_precautions is not None else "Precaution data not available."
        else:  # plant == 'fruit'
            preds = np.argmax(fruit_model.predict(x), axis=-1)
            caution = fruit_precautions.iloc[preds[0]]['Precautions'] if fruit_precautions is not None else "Precaution data not available."

    return render_template('predict.html', caution=caution)  # Always return a response

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
