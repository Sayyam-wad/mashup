from flask import Flask, request, render_template_string
import os
import time
import re

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

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form.get("singer", "").strip()
        num_videos = int(request.form.get("num_videos", 0))
        duration = int(request.form.get("duration", 0))
        email = request.form.get("email", "").strip()

        if not singer:
            return "Singer name is required."

        if num_videos <= 10:
            return "Number of videos must be greater than 10."

        if duration <= 20:
            return "Duration must be greater than 20 seconds."

        if not is_valid_email(email):
            return "Invalid email address."

        # Simulate processing
        time.sleep(2)

        return f"""
        <h3>Mashup request received successfully</h3>
        <p><b>Singer:</b> {singer}</p>
        <p><b>Number of Videos:</b> {num_videos}</p>
        <p><b>Clip Duration:</b> {duration} seconds</p>
        <p><b>Email:</b> {email}</p>
        <p>Your mashup is being processed and will be delivered shortly.</p>
        """

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
