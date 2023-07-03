import matplotlib.pylab as pylab
from fastapi import APIRouter
from fastapi import UploadFile, File, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from keras.models import load_model
import os
import librosa
import numpy as np
import tensorflow as tf
import shutil

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/uploader")
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename == '':
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_302_FOUND)
    with open(f"music/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # print(file.content_type)
    if file.content_type not in ["video/mp4", "audio/mpeg", "application/octet-stream", "video/3gpp", "audio/x-m4a"]:
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_302_FOUND)

    name = test_response(f"./music/{file.filename}")
    return RedirectResponse(url="/index?year=" + name, status_code=status.HTTP_302_FOUND)


def test_response(filepath):
    def save_spectrogram_image(spectrogram, output_file, y_axis):
        pylab.figure(figsize=(12, 8))
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        librosa.display.specshow(spectrogram, y_axis=y_axis, x_axis='time', fmax=None, cmap='viridis')
        pylab.savefig(output_file, dpi=300, bbox_inches=None, pad_inches=0)
        pylab.close()

    model = load_model('../src/ai/model.h5')

    y, sr = librosa.load(filepath)

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    save_spectrogram_image(mfcc, f"{os.path.splitext(filepath)[0]+'.png'}", y_axis='linear')
    os.remove(filepath)
    filepath = os.path.splitext(filepath)[0]+'.png'

    image = tf.keras.preprocessing.image.load_img(filepath, target_size=(224, 224))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model.predict(input_arr).argmax(axis=1)
    possibilities = ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]
    predictions = possibilities[predictions[0]]
    os.remove(filepath)
    return "Décennie: " + predictions
    # return best_model.predict(val_dataset).argmax(axis=1)
