# Correct code
import uvicorn
from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

app = FastAPI()

# Load the model with the correct local file path
# loaded_model = load_model('best_model.h5')

model_path = os.path.abspath('best_model.h5')
print(model_path)

# Load the model with the correct absolute file path
loaded_model = load_model(model_path)
loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

classes = {
    0: 'Normal',
    1: 'Tuberculosis'
}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read image file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Resize image
    image_resized = cv2.resize(image, (128, 128))
    
    # Convert to RGB and normalize
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    image_normalized = image_rgb / 255.0
    
    # Expand dimensions
    image_expanded = np.expand_dims(image_normalized, axis=0)
    
    # Make prediction
    prediction = loaded_model.predict(image_expanded)
    predicted_class_prob = prediction[0][0]
    
    if predicted_class_prob >= 0.5:
        predicted_class = 1
    else:
        predicted_class = 0
    
    predicted_class = classes[predicted_class]
    
    return {"Prediction": predicted_class}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Image Classification API"}
    


