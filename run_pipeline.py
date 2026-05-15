import os
import subprocess


def run_pipeline(video_path):
    import subprocess

    def run(cmd):
        print(f"> {cmd}")
        subprocess.run(cmd, shell=True, check=True)

    run(f"python main.py \"{video_path}\"")
    run("python src/translator/translate.py output/transcription.srt output/translated/transcription_es.srt")
    run("python src/tts/generate.py output/translated/transcription_es.srt output/temp_audio")
    run("python src/sync/sync_audio.py")
    run(f"python src/utils/extract_audio.py \"{video_path}\"")
    run("demucs assets/audio/original_audio.wav")
    run("python src/sync/create_no_vocals.py")
    run("python src/sync/mix_audio.py")
    run(f"python src/utils/render_video.py \"{video_path}\"")

    print("PIPELINE COMPLETADO")