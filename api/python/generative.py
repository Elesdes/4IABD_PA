import librosa
import soundfile as sf
import tensorflow as tf
from fastapi import APIRouter, FileResponse

router = APIRouter()
generator = tf.keras.models.load_model('./models/generator.h5')
noise_dim = 100
file_path = '../temp/reconstructed.wav'


@router.get('/generate/{label}')
def generate(label: str):
    if label is "1950":
        label = tf.constant([[0]])
    elif label is "1960":
        label = tf.constant([[1]])
    elif label is "1970":
        label = tf.constant([[2]])
    elif label is "1980":
        label = tf.constant([[3]])
    elif label is "1990":
        label = tf.constant([[4]])
    elif label is "2000":
        label = tf.constant([[5]])

    noise = tf.random.normal([1, noise_dim])

    generated_mfcc = generator([noise, label], training=False)
    generated_mfcc = (generated_mfcc + 1) / 2.0
    generated_mfcc = tf.image.resize(generated_mfcc, [3600, 2400])
    generated_mfcc = tf.reduce_mean(generated_mfcc, axis=-1)
    generated_mfcc = tf.squeeze(generated_mfcc, axis=0)
    generated_mfcc = generated_mfcc.numpy()

    mel_spectrogram = librosa.feature.inverse.mfcc_to_mel(generated_mfcc)
    stft_spectrogram = librosa.feature.inverse.mel_to_stft(mel_spectrogram)

    audio = librosa.griffinlim(stft_spectrogram)

    sf.write(file_path, audio, 44100)
    return FileResponse(file_path, media_type='audio/wav', filename='output.wav')
