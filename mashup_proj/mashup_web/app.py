from flask import Flask, request, render_template_string
import os

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

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form["singer"]
        num_videos = int(request.form["num_videos"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        if num_videos <= 10 or duration <= 20:
            return "Invalid input. num_videos must be >10 and duration >20."

        return f"""
        <h3>Mashup Request Received</h3>
        <p>Singer: {singer}</p>
        <p>Number of videos: {num_videos}</p>
        <p>Clip duration: {duration} seconds</p>
        <p>Email: {email}</p>
        <p>Your mashup is being processed and will be delivered via email.</p>
        """

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
