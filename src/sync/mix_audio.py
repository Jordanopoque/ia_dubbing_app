import os
from pydub import AudioSegment

BACKGROUND_AUDIO = r"separated\htdemucs\original_audio\no_vocals.wav"
DUB_AUDIO = r"output\final\final_audio.wav"
OUTPUT = r"output\final\mixed_audio.wav"

if not os.path.exists(BACKGROUND_AUDIO):
    raise FileNotFoundError("Falta no_vocals.wav (Demucs no corrió bien)")

if not os.path.exists(DUB_AUDIO):
    raise FileNotFoundError("Falta final_audio.wav (doblaje no generado)")

background = AudioSegment.from_wav(BACKGROUND_AUDIO)
dub = AudioSegment.from_wav(DUB_AUDIO)

background = background - 8

final_mix = background.overlay(dub)

os.makedirs(r"output\final", exist_ok=True)

final_mix.export(OUTPUT, format="wav")

print("\nAudio mezclado generado.")