import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
from pydub import AudioSegment
import numpy as np

MODEL_NAME = "motheecreator/Deepfake-audio-detection"

# Load model and feature extractor once at import
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_NAME)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model.eval()

def load_audio_as_np(file_path, target_sr=16000):
    # Load with pydub (auto-detects format)
    audio = AudioSegment.from_file(file_path)
    # Convert to mono and target sample rate
    audio = audio.set_channels(1).set_frame_rate(target_sr)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)
    return samples, target_sr

def detect_ai_audio(file_path: str) -> (bool, str):
    samples, sample_rate = load_audio_as_np(file_path)
    inputs = feature_extractor(samples, sampling_rate=sample_rate, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        pred = torch.argmax(logits, dim=-1).item()
        score = torch.softmax(logits, dim=-1).squeeze().tolist()
    if pred == 1:
        # 1 = AI (Fake)
        description = (
            f"Detected as AI-generated audio with confidence {score[1]*100:.1f}%. "
            "The model identified patterns typical of synthetic voices, such as unnatural prosody, lack of background noise, or digital artifacts."
        )
        return True, description
    else:
        # 0 = Human (Real)
        description = (
            f"Detected as human audio with confidence {score[0]*100:.1f}%. "
            "The model found natural speech patterns, background noise, and intonation consistent with real human recordings."
        )
        return False, description