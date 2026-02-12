from flask import Flask, request, render_template_string
import os
import shutil
import zipfile
import smtplib
from email.message import EmailMessage

# Heavy libs (work locally, Railway demo mode will skip execution)
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
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch{n}:{singer} songs"
        ydl.download([query])

def convert_and_trim(duration):
    os.makedirs("audios", exist_ok=True)
    audio_files = []

    for file in os.listdir("videos"):
        path = os.path.join("videos", file)
        audio = AudioSegment.from_file(path)
        trimmed = audio[:duration * 1000]

        out_path = os.path.join("audios", os.path.splitext(file)[0] + ".mp3")
        trimmed.export(out_path, format="mp3")
        audio_files.append(out_path)

    return audio_files

def merge_audios(audio_files, output_file):
    final_audio = AudioSegment.empty()
    for f in audio_files:
        final_audio += AudioSegment.from_mp3(f)
    final_audio.export(output_file, format="mp3")

def send_email_with_zip(receiver_email, zip_path):
    sender_email = "your_email@gmail.com"        # change this
    sender_password = "your_app_password_here"  # change this

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Your mashup is ready. Please find the zip attached.")

    with open(zip_path, "rb") as f:
        data = f.read()
        msg.add_attachment(data, maintype="application", subtype="zip", filename="mashup.zip")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form["singer"]
        num_videos = int(request.form["num_videos"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        if num_videos <= 10 or duration <= 20:
            return "Invalid input. num_videos must be >10 and duration >20."

        # Detect Railway environment (no ffmpeg support)
        is_railway = os.environ.get("RAILWAY_ENVIRONMENT") is not None

        try:
            if is_railway:
                # Demo mode for Railway
                zip_name = "mashup.zip"
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    zipf.writestr("demo.txt", f"Mashup for {singer} would be generated here.")
            else:
                # Full pipeline (Local)
                download_videos(singer, num_videos)
                audio_files = convert_and_trim(duration)

                output_file = "mashup.mp3"
                merge_audios(audio_files, output_file)

                zip_name = "mashup.zip"
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    zipf.write(output_file)

                # Email (optional demo)
                # send_email_with_zip(email, zip_name)

                shutil.rmtree("videos")
                shutil.rmtree("audios")

            return f"""
            <h3>Mashup Generated Successfully!</h3>
            <p>Singer: {singer}</p>
            <p>Videos: {num_videos}</p>
            <p>Duration: {duration} sec</p>
            <p>Email: {email}</p>
            <p><b>Note:</b> Full mashup works locally. Railway runs in demo mode.</p>
            """

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
