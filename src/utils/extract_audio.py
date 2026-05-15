import subprocess
import os
import sys

VIDEO_INPUT = sys.argv[1]  # 👈 viene del pipeline

AUDIO_OUTPUT = r"assets\audio\original_audio.wav"

os.makedirs(r"assets\audio", exist_ok=True)

command = [
    "ffmpeg",
    "-y",
    "-i",
    VIDEO_INPUT,
    AUDIO_OUTPUT
]

print("\nExtrayendo audio...\n")

subprocess.run(command, check=True)

print("\nAudio extraido.")