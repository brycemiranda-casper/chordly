import librosa
import soundfile as sf
import numpy as np

def preprocess(input_wav, output_wav="processed.wav"):
    # 1. Load audio (sr=None preserves the original sampling rate if preferred)
    audio, sr = librosa.load(input_wav, sr=44100, mono=True)
    
    # 2. Normalize volume (scales audio to between -1.0 and 1.0)
    # This is a standard preprocessing step for Machine Learning
    audio = librosa.util.normalize(audio)
    
    # 3. Optional: Trim leading/trailing silence
    audio, _ = librosa.effects.trim(audio)

    # 4. Save with a specific subtype to keep file size down (PCM_16)
    sf.write(output_wav, audio, sr, subtype='PCM_16')
    
    print(f"Processed audio saved as {output_wav} at {sr}Hz")

if __name__ == "__main__":
    preprocess("test_mic.wav")