import yt_dlp
from pathlib import Path

# URL con video de mejor calidad (TED Talk, muy recomendable)
url = 'https://www.youtube.com/watch?v=ZXsQAXx_ao0'

ydl_opts = {
    'format': '22+bestaudio/best',  # 720p + best audio
    'outtmpl': 'test_video.%(ext)s',
    'quiet': False,
    'no_warnings': False,
    'socket_timeout': 30,
    'retries': 3,
    'fragment_retries': 3,
    'merge_output_format': 'mp4',
}

print("Iniciando descarga de prueba...")
print(f"URL: {url}\n")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    print(f"\nDescarga completada: {info.get('title')}")
except Exception as e:
    print(f"Error: {e}")
