from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

app = FastAPI()

# Load the pre-trained TensorFlow model
try:
    model = tf.keras.models.load_model("/opt/render/project/src/best_model.h5")
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading the model: {e}")

class ImageInput(BaseModel):
    image: str

@app.post("/predict/")
async def predict_image(image_input: ImageInput):
    # Convert the base64 image string to an image
    image_data = base64.b64decode(image_input.image)
    image = Image.open(io.BytesIO(image_data))

    # Preprocess the image
    image = image.resize((224, 224))  # Resize to the input shape of the model
    image = np.array(image) / 255.0  # Normalize the image

    # Predict the image
    predictions = model.predict(np.expand_dims(image, axis=0))

    # Get the predicted class
    predicted_class = np.argmax(predictions, axis=1)[0]

    return {"predicted_class": predicted_class}
