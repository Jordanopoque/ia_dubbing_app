import whisper
import sys

video_path = sys.argv[1]  # 👈 recibe el archivo desde pipeline

model = whisper.load_model("base")

result = model.transcribe(video_path)

segments = result["segments"]

output_path = f"output/transcription.srt"

with open(output_path, "w", encoding="utf-8") as f:

    def format_time(seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

    for i, segment in enumerate(segments, start=1):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        f.write(f"{i}\n")
        f.write(f"{format_time(start)} --> {format_time(end)}\n")
        f.write(f"{text}\n\n")