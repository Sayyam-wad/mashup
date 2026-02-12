import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def download_videos(singer, n):
    os.makedirs("videos", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'quiet': False
    }

    with YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch{n}:{singer} songs"
        ydl.download([query])

def convert_and_trim(duration):
    os.makedirs("audios", exist_ok=True)
    audio_files = []

    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)
        print("Processing:", file)

        audio = AudioSegment.from_file(video_path)
        trimmed = audio[:duration * 1000]

        audio_name = os.path.splitext(file)[0] + ".mp3"
        audio_path = os.path.join("audios", audio_name)

        trimmed.export(audio_path, format="mp3")
        audio_files.append(audio_path)

    return audio_files

def merge_audios(audio_files, output_file):
    print("Merging audio files...")
    final_audio = AudioSegment.empty()

    for file in audio_files:
        final_audio += AudioSegment.from_mp3(file)

    final_audio.export(output_file, format="mp3")
    print("Final mashup saved as:", output_file)

def main():
    if len(sys.argv) != 5:
        print("Usage: python 102303147.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    try:
        print("Downloading videos...")
        download_videos(singer, num_videos)

        print("Converting to audio and trimming...")
        audio_files = convert_and_trim(duration)

        print("Merging trimmed audios...")
        merge_audios(audio_files, output_file)

        print("Mashup created successfully ✅")

    except Exception as e:
        print("❌ Error occurred:", str(e))

    finally:
        if os.path.exists("videos"):
            shutil.rmtree("videos")
        if os.path.exists("audios"):
            shutil.rmtree("audios")

if __name__ == "__main__":
    main()
