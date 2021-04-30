import json
import subprocess
import os

from flask import Flask, render_template, request
import pathlib
import requests

# App config.
DEBUG = True
app = Flask(__name__)

jsonFile = "tests.json"


@app.route("/", methods=["GET", "POST"])
def results():
    title = "Tests"
    file_data = ""
    submission_successful = False
    if request.method == "POST":
        print(request.form)
        with open(jsonFile, "w+") as f:
            json.dump(request.form, f)
        submission_successful = True

        filepath = ".run_traffic_elasticsearch.bat"
        p = subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print(p.returncode)  # is 0 if success

    try:
        with open(jsonFile) as f:
            file_data = json.load(f)
            f.close()
    except:
        file_data = "could not read file"
    return render_template('index.html', data=file_data, submission=submission_successful)


if __name__ == "__main__":
    app.run()
