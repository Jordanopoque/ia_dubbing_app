import os
import pysrt

from pydub import AudioSegment

# =========================
# CONFIG
# =========================

SRT_PATH = (
    r"output\translated\transcription_es.srt"
)

TEMP_DIR = r"output\temp_audio"

FINAL_OUTPUT = (
    r"output\final\final_audio.wav"
)

# =========================
# CREAR SILENCIO BASE
# =========================

final_audio = AudioSegment.silent(duration=0)

# =========================
# LEER SRT
# =========================

subs = pysrt.open(
    SRT_PATH,
    encoding="utf-8"
)

# =========================
# PROCESAR CADA AUDIO
# =========================

for i, sub in enumerate(subs):

    audio_path = os.path.join(
        TEMP_DIR,
        f"{i}.wav"
    )

    clip = AudioSegment.from_wav(audio_path)

    # tiempo inicio en ms
    start_time = (
        sub.start.hours * 3600000
        + sub.start.minutes * 60000
        + sub.start.seconds * 1000
        + sub.start.milliseconds
    )

    current_duration = len(final_audio)

    # insertar silencio
    if start_time > current_duration:

        silence = AudioSegment.silent(
            duration=start_time - current_duration
        )

        final_audio += silence

    # agregar clip
    final_audio += clip

    print(f"Sincronizado {i}.wav")

# =========================
# EXPORTAR
# =========================

os.makedirs(
    r"output\final",
    exist_ok=True
)

final_audio.export(
    FINAL_OUTPUT,
    format="wav"
)

print("\nAudio final generado.")