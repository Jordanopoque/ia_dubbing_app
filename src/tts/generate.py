import os
import subprocess
import pysrt
import sys

# =========================
# INPUTS DINÁMICOS
# =========================

srt_path = sys.argv[1]
output_dir = sys.argv[2]

PIPER_PATH = r"C:\piper\piper.exe"
MODEL_PATH = r"C:\piper\models\es_AR-daniela-high.onnx"

# =========================
# VALIDACIÓN
# =========================

if not os.path.exists(srt_path):
    raise FileNotFoundError(f"No existe SRT: {srt_path}")

if not os.path.exists(PIPER_PATH):
    raise FileNotFoundError("No se encontró piper.exe")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("No se encontró el modelo ONNX")

os.makedirs(output_dir, exist_ok=True)

subs = pysrt.open(srt_path, encoding="utf-8")

# =========================
# GENERACIÓN TTS
# =========================

for i, sub in enumerate(subs):

    text = sub.text.replace("\n", " ").strip()

    if not text:
        print(f"⚠️ Texto vacío en índice {i}, se omite")
        continue

    output_file = os.path.join(output_dir, f"{i}.wav")

    command = [
        PIPER_PATH,
        "--model", MODEL_PATH,
        "--output_file", output_file
    ]

    print(f"\nGenerando: {output_file}")
    print(f"Texto: {text}")

    # =========================
    # EJECUTAR PIPER
    # =========================

    result = subprocess.run(
        command,
        input=text,
        text=True,
        encoding="utf-8",
        capture_output=True
    )

    # =========================
    # ERROR PIPE
    # =========================

    if result.returncode != 0:
        print("❌ ERROR en Piper:")
        print(result.stderr)
        continue

    # =========================
    # VALIDAR ARCHIVO GENERADO
    # =========================

    if not os.path.exists(output_file):
        print(f"❌ No se generó archivo: {output_file}")
        continue

    if os.path.getsize(output_file) < 1000:
        print(f"⚠️ Archivo corrupto o vacío: {output_file}")
        continue

print("\nTTS COMPLETADO")