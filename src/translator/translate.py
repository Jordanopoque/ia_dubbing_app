import pysrt
from deep_translator import GoogleTranslator
import sys
import os

# recibir input desde pipeline
input_srt = sys.argv[1]  # output del whisper
output_srt = sys.argv[2]  # output traducido

if not os.path.exists(input_srt):
    raise FileNotFoundError(f"No existe: {input_srt}")

subs = pysrt.open(input_srt, encoding="utf-8")

translator = GoogleTranslator(source='auto', target='es')

for sub in subs:
    if sub.text.strip():
        try:
            sub.text = translator.translate(sub.text)
        except Exception as e:
            print("Error traduciendo:", e)
            sub.text = sub.text  # fallback

os.makedirs(os.path.dirname(output_srt), exist_ok=True)

subs.save(output_srt, encoding="utf-8")

print("Traducción completada:", output_srt)