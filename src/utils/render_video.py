import subprocess
import os
import sys

VIDEO_INPUT = sys.argv[1]  # 👈 ahora dinámico

AUDIO_INPUT = r"output\final\mixed_audio.wav"

OUTPUT_VIDEO = r"output\final\dubbed_video.mp4"

os.makedirs(r"output\final", exist_ok=True)

command = [
    "ffmpeg",
    "-y",
    "-i", VIDEO_INPUT,
    "-i", AUDIO_INPUT,
    "-c:v", "copy",
    "-map", "0:v:0",
    "-map", "1:a:0",
    OUTPUT_VIDEO
]

print("\nRenderizando video final...\n")

subprocess.run(command)

print("\nVideo doblado generado.")