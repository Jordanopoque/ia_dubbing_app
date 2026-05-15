import yt_dlp
import json

url = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

ydl_opts = {
    'quiet': False,
    'no_warnings': False,
    'extract_flat': False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    print(f"Total de formatos: {len(info.get('formats', []))}")
    print("\nFormatos disponibles (video+audio):")
    
    count = 0
    for fmt in info.get('formats', []):
        has_video = fmt.get('vcodec') != 'none'
        has_audio = fmt.get('acodec') != 'none'
        height = fmt.get('height', 0)
        
        if has_video and has_audio:
            print(f"  ID: {fmt['format_id']}, Height: {height}p, Vcodec: {fmt.get('vcodec')}, Acodec: {fmt.get('acodec')}")
            count += 1
    
    print(f"\nTotal formatos con video+audio: {count}")
    
except Exception as e:
    print(f"Error: {e}")
