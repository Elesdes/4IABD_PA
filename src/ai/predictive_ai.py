import librosa
import matplotlib.pyplot as plt
import os
import io
import tensorflow as tf

def prediction_ai(audio_file):
    y, sr = librosa.load(audio_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    fig, ax = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(mfcc, x_axis='time', sr=sr, ax=ax)
    ax.axis('off')

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    png_byte_stream = buf.getvalue()

    model = tf.keras.models.load_model("../src/ai/model.h5")
    prediction = model.predict(png_byte_stream).argmax(axis=1)
    return prediction