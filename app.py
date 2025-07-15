from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def index():
    job_file = "latest_jobs.txt"
    if not os.path.exists(job_file):
        return "<h2>No job results available yet. Please wait for the first scheduled run.</h2>"

    with open(job_file, "r") as f:
        jobs = f.readlines()

    template = """
    <html>
    <head><title>Daily Job Results</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>🧠 Daily Job Digest</h1>
        <ul>
            {% for job in jobs %}
                <li><a href="{{ job.strip() }}" target="_blank">{{ job.strip() }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(template, jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)
