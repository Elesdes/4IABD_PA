# In this code, an API endpoint "/uploader" is defined using the FastAPI library.
# It allows users to upload an audio file. The uploaded file is then processed,
# and its music content is transformed into a spectrogram image.
# This image is then processed by a pre-trained model to make a prediction about the decade the music came from.
# After processing, both the audio file and the image file are deleted for housekeeping.
# If an error occurs (for example, a file with no name or a non-MP3 file is uploaded),
# the user is redirected to an "/unauthorized" page.


# Importing the necessary libraries for the project
import matplotlib.pylab as pylab
from fastapi import UploadFile, File, status, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from keras.models import load_model
import os
import librosa
import numpy as np
import tensorflow as tf
import shutil

# Creating an instance of APIRouter
router = APIRouter()

# Setting up Jinja2 template engine to use "templates" directory
templates = Jinja2Templates(directory="templates")


# Endpoint for uploading files. It only accepts files as input.
@router.post("/uploader")
async def create_upload_file(file: UploadFile = File(...)):
    # If no filename is provided, redirect to "/unauthorized"
    if file.filename == '':
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_302_FOUND)

    # Save the uploaded file into the "music" directory
    with open(f"music/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Only mp3 files are allowed, delete others and redirect to "/unauthorized"
    if not file.filename.endswith('.mp3'):
        os.remove(f"./music/{file.filename}")
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_302_FOUND)

    # Process the file and redirect to "/index" with a parameter indicating the predicted year
    name = test_response(f"./music/{file.filename}")
    return RedirectResponse(url="/index?year=" + name, status_code=status.HTTP_302_FOUND)


# Function to process the file and predict the year
def test_response(filepath):
    # Helper function to save the spectrogram image of an audio file
    def save_spectrogram_image(spectrogram, output_file, y_axis):
        pylab.figure(figsize=(12, 8))
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        librosa.display.specshow(spectrogram, y_axis=y_axis, x_axis='time', fmax=None, cmap='viridis')
        pylab.savefig(output_file, dpi=300, bbox_inches=None, pad_inches=0)
        pylab.close()

    # Load pre-trained model
    model = load_model('../src/ai/model.h5')

    # Load audio file with librosa
    y, sr = librosa.load(filepath)

    # Extract MFCC (Mel-Frequency Cepstral Coefficients) from the audio file
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    # Save the MFCC as an image
    save_spectrogram_image(mfcc, f"{os.path.splitext(filepath)[0] + '.png'}", y_axis='linear')

    # Delete original audio file
    os.remove(filepath)

    # Prepare for image classification
    filepath = os.path.splitext(filepath)[0] + '.png'

    # Load image and convert it to an array
    image = tf.keras.preprocessing.image.load_img(filepath, target_size=(224, 224))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)

    # Wrap the array into another array
    input_arr = np.array([input_arr])

    # Make prediction using the trained model
    predictions = model.predict(input_arr).argmax(axis=1)

    # List of possible predictions (decades)
    possibilities = ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]

    # Get the predicted year from the list
    predictions = possibilities[predictions[0]]

    # Delete the spectrogram image
    os.remove(filepath)

    # Return the prediction
    return "Décennie: " + predictions
