from flask import Flask, request, render_template_string
import os
import shutil
import zipfile
from yt_dlp import YoutubeDL
from pydub import AudioSegment

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html>
<head>
    <title>Mashup Generator</title>
</head>
<body>
    <h2>Mashup Generator</h2>
    <form method="post">
        Singer Name: <input type="text" name="singer" required><br><br>
        Number of Videos (>10): <input type="number" name="num_videos" required><br><br>
        Duration (sec >20): <input type="number" name="duration" required><br><br>
        Email ID: <input type="email" name="email" required><br><br>
        <button type="submit">Generate Mashup</button>
    </form>
</body>
</html>
"""

def download_videos(singer, n):
    os.makedirs("videos", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'videos/%(id)s.%(ext)s',
        'quiet': True,
        'postprocessors': [],
        'noplaylist': True,
        'concurrent_fragment_downloads': 1
    }

    with YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch{n}:{singer} songs"
        ydl.download([query])


    with YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch{n}:{singer} songs"
        ydl.download([query])

def convert_and_trim(duration):
    os.makedirs("audios", exist_ok=True)
    audio_files = []

    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)

        try:
            audio = AudioSegment.from_file(video_path)
            trimmed = audio[:duration * 1000]

            audio_name = os.path.splitext(file)[0] + ".mp3"
            audio_path = os.path.join("audios", audio_name)

            trimmed.export(audio_path, format="mp3")
            audio_files.append(audio_path)

        except Exception as e:
            print("Skipping file:", file, e)

    return audio_files

def merge_audios(audio_files, output_file):
    final_audio = AudioSegment.empty()
    for file in audio_files:
        final_audio += AudioSegment.from_mp3(file)
    final_audio.export(output_file, format="mp3")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form["singer"]
        num_videos = int(request.form["num_videos"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        if num_videos <= 10 or duration <= 20:
            return "Invalid input. Number of videos must be >10 and duration >20 seconds."

        try:
            download_videos(singer, num_videos)
            audio_files = convert_and_trim(duration)

            output_file = "mashup.mp3"
            merge_audios(audio_files, output_file)

            zip_name = "mashup.zip"
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                zipf.write(output_file)

            shutil.rmtree("videos", ignore_errors=True)
            shutil.rmtree("audios", ignore_errors=True)

            return f"""
            <h3>Mashup generated successfully!</h3>
            <p>Your mashup ZIP is ready.</p>
            <p>Email feature can be demonstrated separately as per assignment.</p>
            """

        except Exception as e:
            return f"<h3>Error occurred</h3><pre>{str(e)}</pre>"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

