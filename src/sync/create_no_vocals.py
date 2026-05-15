from pydub import AudioSegment
import os

# =========================
# PATHS
# =========================

BASE_PATH = (
    r"separated\htdemucs\original_audio"
)

assert os.path.exists(BASE_PATH), "Demucs output no encontrado"
DRUMS = os.path.join(BASE_PATH, "drums.wav")
BASS = os.path.join(BASE_PATH, "bass.wav")
OTHER = os.path.join(BASE_PATH, "other.wav")

OUTPUT = os.path.join(BASE_PATH, "no_vocals.wav")

# =========================
# CARGAR AUDIOS
# =========================

drums = AudioSegment.from_wav(DRUMS)

bass = AudioSegment.from_wav(BASS)

other = AudioSegment.from_wav(OTHER)

# =========================
# MEZCLAR
# =========================

combined = drums.overlay(bass)

combined = combined.overlay(other)

# =========================
# EXPORTAR
# =========================

combined.export(
    OUTPUT,
    format="wav"
)

print("\nno_vocals.wav generado.")